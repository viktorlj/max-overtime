"""Main analysis pipeline: parse → merge → store."""

from __future__ import annotations

import base64
import json

import dash
from dash import Input, Output, State, callback_context, no_update, ALL
import polars as pl

from src.parsers.common import parse_file
from src.processing.merge import merge_timepoints
from src.i18n import t


def register(app: dash.Dash) -> None:
    """Register the processing pipeline callback."""

    @app.callback(
        Output("store-merged-data", "data"),
        Output("store-sample-name", "data"),
        Output("plot-section", "style"),
        Output("variant-table-section", "style"),
        Output("upload-error-alert", "children"),
        Output("upload-error-alert", "is_open"),
        Input("btn-analyze", "n_clicks"),
        State({"type": "tp-upload", "index": ALL}, "contents"),
        State({"type": "tp-upload", "index": ALL}, "filename"),
        State({"type": "tp-date", "index": ALL}, "value"),
        State({"type": "tp-label", "index": ALL}, "children"),
        State("input-sample-id", "value"),
        State("store-language", "data"),
        prevent_initial_call=True,
    )
    def run_analysis(
        n_clicks,
        file_contents: list,
        file_names: list,
        dates: list,
        tp_labels: list,
        sample_id: str | None,
        lang: str,
    ):
        if not n_clicks:
            return no_update, no_update, no_update, no_update, no_update, no_update

        lang = lang or "en"
        show = {"display": "block"}
        hide = {"display": "none"}

        # Validate sample ID
        if not sample_id or not sample_id.strip():
            return (
                no_update,
                no_update,
                hide,
                hide,
                t("error.missing_sample_id", lang),
                True,
            )

        # Validate files
        if not file_contents or all(c is None for c in file_contents):
            return (
                no_update,
                no_update,
                hide,
                hide,
                t("error.missing_files", lang),
                True,
            )

        # Validate dates
        if not dates or all(d is None for d in dates):
            return (
                no_update,
                no_update,
                hide,
                hide,
                t("error.missing_dates", lang),
                True,
            )

        # Parse each timepoint
        timepoint_data = []
        for i, (content, filename, date, label) in enumerate(
            zip(file_contents, file_names, dates, tp_labels)
        ):
            if content is None or filename is None:
                continue

            # Decode base64 content
            try:
                content_type, content_string = content.split(",", 1)
                decoded = base64.b64decode(content_string).decode("utf-8")
            except Exception as e:
                return (
                    no_update,
                    no_update,
                    hide,
                    hide,
                    t("error.parse_failed", lang, detail=str(e)),
                    True,
                )

            try:
                records = parse_file(filename, decoded)
            except Exception as e:
                return (
                    no_update,
                    no_update,
                    hide,
                    hide,
                    t("error.parse_failed", lang, detail=f"{filename}: {e}"),
                    True,
                )

            tp_label = label if isinstance(label, str) else f"Timepoint {i + 1}"
            timepoint_data.append((tp_label, date, records))

        if len(timepoint_data) < 2:
            return (
                no_update,
                no_update,
                hide,
                hide,
                t("upload.min_timepoints", lang),
                True,
            )

        # Merge
        merged_df = merge_timepoints(timepoint_data)

        if merged_df.is_empty():
            return (
                no_update,
                no_update,
                hide,
                hide,
                t("error.no_variants", lang),
                True,
            )

        # Serialize to JSON for dcc.Store
        data_json = merged_df.write_json()

        return (
            data_json,
            sample_id.strip(),
            show,
            show,
            "",
            False,
        )
