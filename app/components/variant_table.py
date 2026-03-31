"""Interactive DataTable for variant display with row selection."""

from __future__ import annotations

from dash import dash_table, html


def create_variant_table() -> html.Div:
    """Create the variant data table with selectable rows."""
    return html.Div(
        html.Div(
            [
                html.Div("Data", className="section-label"),
                html.H4(
                    "Variant Table",
                    id="heading-variant-table",
                    className="section-title",
                    style={"fontSize": "17px"},
                ),
                html.P(
                    "Select rows to update the plot. All variants are selected by default.",
                    id="table-hint",
                    className="table-hint",
                ),
                dash_table.DataTable(
                    id="variant-table",
                    columns=[],
                    data=[],
                    row_selectable="multi",
                    selected_rows=[],
                    page_size=50,
                    sort_action="native",
                    filter_action="native",
                    style_table={"overflowX": "auto"},
                    style_cell={
                        "textAlign": "left",
                        "padding": "9px 14px",
                        "fontSize": "13px",
                        "fontFamily": "'JetBrains Mono', ui-monospace, monospace",
                        "border": "none",
                    },
                    style_header={
                        "backgroundColor": "#213448",
                        "color": "rgba(255,255,255,0.9)",
                        "fontWeight": "600",
                        "fontSize": "11px",
                        "fontFamily": "'JetBrains Mono', ui-monospace, monospace",
                        "textTransform": "uppercase",
                        "letterSpacing": "0.06em",
                        "border": "none",
                    },
                    style_data_conditional=[
                        {
                            "if": {"row_index": "odd"},
                            "backgroundColor": "#f7f6f4",
                        },
                        {
                            "if": {"state": "selected"},
                            "backgroundColor": "rgba(84, 119, 146, 0.08)",
                            "border": "none",
                        },
                    ],
                    style_filter={
                        "backgroundColor": "#f7f6f4",
                        "border": "none",
                        "fontSize": "12px",
                    },
                ),
            ],
            className="table-card",
        ),
        id="variant-table-section",
        style={"display": "none"},
        className="mt-4",
    )
