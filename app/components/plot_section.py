"""Plot section: interactive Plotly chart + download buttons."""

from __future__ import annotations

from dash import dcc, html


def create_plot_section() -> html.Div:
    """Create the plot area with download buttons."""
    return html.Div(
        html.Div(
            [
                # Header row
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div("Results", className="section-label"),
                                html.H4(
                                    "VAF Over Time",
                                    id="heading-vaf-plot",
                                    className="section-title",
                                    style={"fontSize": "17px", "marginBottom": "0"},
                                ),
                            ],
                        ),
                        # Export buttons
                        html.Div(
                            [
                                html.Button(
                                    ["\u2193 ", html.Span("PDF Report", id="btn-download-pdf-text")],
                                    id="btn-download-pdf",
                                    className="btn-export",
                                ),
                                html.Button(
                                    ["\u2193 ", html.Span("Excel", id="btn-download-excel-text")],
                                    id="btn-download-excel",
                                    className="btn-export",
                                ),
                                html.Button(
                                    ["\u2193 ", html.Span("TSV Data", id="btn-download-tsv-text")],
                                    id="btn-download-tsv",
                                    className="btn-export",
                                ),
                            ],
                            style={"display": "flex", "gap": "8px", "flexWrap": "wrap"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "flex-end",
                        "marginBottom": "20px",
                        "flexWrap": "wrap",
                        "gap": "12px",
                    },
                ),
                # Plot
                dcc.Loading(
                    dcc.Graph(
                        id="vaf-plot",
                        config={
                            "displayModeBar": True,
                            "toImageButtonOptions": {
                                "format": "svg",
                                "filename": "vaf_overtime",
                            },
                        },
                        style={"borderRadius": "10px"},
                    ),
                    type="default",
                    color="#2BB5A6",
                ),
                # Download components
                dcc.Download(id="download-pdf"),
                dcc.Download(id="download-excel"),
                dcc.Download(id="download-tsv"),
            ],
            className="results-card",
        ),
        id="plot-section",
        style={"display": "none"},
        className="mt-4",
    )
