"""Tests for DataTable component."""

from fasthtml.common import to_xml

from faststrap import DataTable


def test_data_table_renders_sortable_headers_and_pagination():
    data = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
    ]

    table = DataTable(
        data,
        sortable=True,
        sort="name",
        direction="asc",
        pagination=True,
        page=1,
        per_page=1,
        total_rows=2,
        endpoint="/users",
    )
    html = to_xml(table)

    assert 'aria-sort="ascending"' in html
    assert "sort=name" in html
    assert "direction=desc" in html
    assert "page=2" in html


def test_data_table_search_input():
    data = [{"name": "Alice"}]
    table = DataTable(
        data,
        searchable=True,
        search="al",
        endpoint="/users",
    )
    html = to_xml(table)

    assert 'type="search"' in html
    assert 'name="q"' in html
    assert 'value="al"' in html


def test_data_table_export_params_helper():
    params = DataTable.export_params(
        sort="name",
        direction="desc",
        search="al",
        filters={"team": "ops", "active": True, "empty": None},
        include_pagination=True,
        page=2,
        per_page=50,
    )
    assert params["sort"] == "name"
    assert params["direction"] == "desc"
    assert params["q"] == "al"
    assert params["team"] == "ops"
    assert params["active"] == "true"
    assert "empty" not in params
    assert params["page"] == 2
    assert params["per_page"] == 50
