"""Dynamic timepoint add/remove callbacks."""

from __future__ import annotations

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback_context, dcc, html, no_update, ALL, MATCH


def _make_timepoint_card(index: int) -> html.Div:
    """Create a timepoint card for dynamic insertion."""
    return html.Div(
        html.Div(
            [
                html.Span(
                    f"Timepoint {index}",
                    id={"type": "tp-label", "index": index},
                    className="tp-badge",
                ),
                dbc.Input(
                    type="date",
                    id={"type": "tp-date", "index": index},
                    className="tp-date-input",
                    style={"width": "160px"},
                ),
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
                html.Div(
                    id={"type": "tp-status", "index": index},
                    style={"minWidth": "120px"},
                ),
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


def register(app: dash.Dash) -> None:
    """Register upload management callbacks."""

    @app.callback(
        Output("timepoint-container", "children"),
        Output("tp-next-index", "data"),
        Input("btn-add-timepoint", "n_clicks"),
        Input({"type": "tp-remove", "index": ALL}, "n_clicks"),
        State("timepoint-container", "children"),
        State("tp-next-index", "data"),
        prevent_initial_call=True,
    )
    def manage_timepoints(add_clicks, remove_clicks, current_children, next_idx):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update

        trigger = ctx.triggered[0]["prop_id"]

        if "btn-add-timepoint" in trigger:
            new_card = _make_timepoint_card(next_idx)
            current_children = current_children or []
            return current_children + [new_card], next_idx + 1

        if "tp-remove" in trigger:
            current_children = current_children or []
            if len(current_children) <= 2:
                return no_update, no_update

            import json
            triggered_id = json.loads(trigger.split(".")[0])
            remove_idx = triggered_id["index"]

            new_children = []
            for child in current_children:
                card_props = child.get("props", {}) if isinstance(child, dict) else {}
                card_id = card_props.get("id", {})
                if isinstance(card_id, dict) and card_id.get("index") == remove_idx:
                    continue
                if hasattr(child, "id") and isinstance(child.id, dict) and child.id.get("index") == remove_idx:
                    continue
                new_children.append(child)

            return new_children, no_update

        return no_update, no_update

    @app.callback(
        Output({"type": "tp-status", "index": MATCH}, "children"),
        Input({"type": "tp-upload", "index": MATCH}, "filename"),
        prevent_initial_call=True,
    )
    def update_file_status(filename):
        if filename:
            return html.Span(
                f"\u2713 {filename}",
                className="file-badge",
            )
        return no_update
