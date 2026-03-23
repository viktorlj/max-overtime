"""Language toggle callbacks."""

from __future__ import annotations

from dash import Input, Output, State, callback_context, no_update
import dash

from src.i18n import t


def register(app: dash.Dash) -> None:
    """Register language toggle callbacks."""

    @app.callback(
        Output("store-language", "data"),
        Output("btn-lang-en", "className"),
        Output("btn-lang-sv", "className"),
        Input("btn-lang-en", "n_clicks"),
        Input("btn-lang-sv", "n_clicks"),
        State("store-language", "data"),
        prevent_initial_call=True,
    )
    def toggle_language(n_en: int | None, n_sv: int | None, current: str):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger_id == "btn-lang-en":
            return "en", "lang-btn lang-btn-active", "lang-btn lang-btn-inactive"
        else:
            return "sv", "lang-btn lang-btn-inactive", "lang-btn lang-btn-active"

    @app.callback(
        Output("label-sample-id", "children"),
        Output("input-sample-id", "placeholder"),
        Output("btn-add-timepoint", "children"),
        Output("btn-analyze", "children"),
        Output("heading-vaf-plot", "children"),
        Output("heading-variant-table", "children"),
        Output("btn-download-pdf-text", "children"),
        Output("btn-download-excel-text", "children"),
        Output("btn-download-tsv-text", "children"),
        Output("brand-tagline", "children"),
        Output("nav-analysis", "children"),
        Output("nav-tutorial", "children"),
        Output("table-hint", "children"),
        Input("store-language", "data"),
    )
    def update_translations(lang: str):
        lang = lang or "en"
        return (
            t("upload.sample_id", lang),
            t("upload.sample_id_placeholder", lang),
            "+ " + t("upload.add_timepoint", lang),
            t("upload.analyze", lang),
            t("results.plot_title", lang),
            t("table.heading", lang),
            t("results.download_pdf", lang),
            t("results.download_excel", lang),
            t("results.download_tsv", lang),
            t("app.subtitle", lang),
            t("nav.analysis", lang),
            t("nav.tutorial", lang),
            t("table.hint", lang),
        )
