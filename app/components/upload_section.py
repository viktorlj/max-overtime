"""Upload section: sample ID input, dynamic timepoint cards, analyze button."""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html


def _create_timepoint_card(index: int) -> html.Div:
    """Create a single timepoint upload card."""
    return html.Div(
        html.Div(
            [
                # Timepoint badge
                html.Span(
                    f"Timepoint {index}",
                    id={"type": "tp-label", "index": index},
                    className="tp-badge",
                ),
                # Date input
                dbc.Input(
                    type="date",
                    id={"type": "tp-date", "index": index},
                    className="tp-date-input",
                    style={"width": "160px"},
                ),
                # Upload zone
                dcc.Upload(
                    id={"type": "tp-upload", "index": index},
                    children=html.Div(
                        [
                            html.Span("\u2191 ", className="upload-zone-icon"),
                            html.Span(
                                "Drop file or click to browse",
                                id={"type": "tp-upload-text", "index": index},
                                className="upload-zone-text",
                            ),
                        ],
                        style={"display": "flex", "alignItems": "center", "justifyContent": "center"},
                    ),
                    className="upload-zone",
                    style={},
                    multiple=False,
                ),
                # Status
                html.Div(
                    id={"type": "tp-status", "index": index},
                    style={"minWidth": "120px"},
                ),
                # Remove button
                html.Button(
                    "\u00d7",
                    id={"type": "tp-remove", "index": index},
                    className="btn-remove-tp",
                ),
            ],
            style={
                "display": "flex",
                "alignItems": "center",
                "gap": "12px",
                "flexWrap": "wrap",
            },
        ),
        className="tp-card",
        id={"type": "tp-card", "index": index},
    )


def create_upload_section() -> html.Div:
    """Create the full upload section."""
    return html.Div(
        html.Div(
            [
                # Section header
                html.Div("Data Input", className="section-label"),
                html.H3(
                    "Upload Variant Files",
                    className="section-title",
                    id="heading-upload",
                ),
                html.P(
                    "Configure timepoints and upload one variant file per timepoint.",
                    className="section-subtitle",
                    id="heading-upload-sub",
                ),

                # Sample ID
                html.Div(
                    [
                        html.Label(
                            "Sample ID",
                            htmlFor="input-sample-id",
                            id="label-sample-id",
                            className="label-sample-id",
                        ),
                        dbc.Input(
                            id="input-sample-id",
                            type="text",
                            placeholder="e.g. AML_2024_001",
                            className="input-sample-id",
                            style={"maxWidth": "360px"},
                        ),
                    ],
                    style={"marginBottom": "24px"},
                ),

                # Timepoint cards
                html.Div(
                    [
                        _create_timepoint_card(1),
                        _create_timepoint_card(2),
                    ],
                    id="timepoint-container",
                ),

                dcc.Store(id="tp-next-index", data=3),

                # Action buttons
                html.Div(
                    [
                        html.Button(
                            "+ Add timepoint",
                            id="btn-add-timepoint",
                            className="btn-add-tp",
                        ),
                        html.Button(
                            "Run Analysis",
                            id="btn-analyze",
                            className="btn-analyze",
                        ),
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "gap": "16px",
                        "marginTop": "24px",
                    },
                ),

                # Error alert
                dbc.Alert(
                    id="upload-error-alert",
                    is_open=False,
                    className="alert-clinical mt-3",
                    dismissable=True,
                ),
            ],
            className="card-clinical",
            style={"padding": "32px"},
        ),
        id="upload-section",
    )
