"""Download callbacks for PDF, Excel, and TSV exports."""

from __future__ import annotations

import dash
from dash import Input, Output, State, no_update, dcc


def register(app: dash.Dash) -> None:
    """Register export/download callbacks."""

    @app.callback(
        Output("download-pdf", "data"),
        Input("btn-download-pdf", "n_clicks"),
        State("vaf-plot", "figure"),
        State("store-sample-name", "data"),
        prevent_initial_call=True,
    )
    def download_pdf(n_clicks, figure_dict, sample_name):
        if not n_clicks or not figure_dict:
            return no_update

        import plotly.graph_objects as go
        from src.processing.export import export_pdf

        fig = go.Figure(figure_dict)
        pdf_bytes = export_pdf(fig)
        filename = f"{sample_name or 'vaf_overtime'}.pdf"
        return dcc.send_bytes(pdf_bytes, filename)

    @app.callback(
        Output("download-excel", "data"),
        Input("btn-download-excel", "n_clicks"),
        State("store-merged-data", "data"),
        State("store-sample-name", "data"),
        prevent_initial_call=True,
    )
    def download_excel(n_clicks, data_json, sample_name):
        if not n_clicks or not data_json:
            return no_update

        import polars as pl
        from src.processing.export import export_excel

        df = pl.read_json(data_json.encode())
        excel_bytes = export_excel(df, sample_name or "Variants")
        filename = f"{sample_name or 'variants'}.xlsx"
        return dcc.send_bytes(excel_bytes, filename)

    @app.callback(
        Output("download-tsv", "data"),
        Input("btn-download-tsv", "n_clicks"),
        State("store-merged-data", "data"),
        State("store-sample-name", "data"),
        prevent_initial_call=True,
    )
    def download_tsv(n_clicks, data_json, sample_name):
        if not n_clicks or not data_json:
            return no_update

        import polars as pl
        from src.processing.export import export_tsv

        df = pl.read_json(data_json.encode())
        tsv_bytes = export_tsv(df)
        filename = f"{sample_name or 'variants'}.tsv"
        return dcc.send_bytes(tsv_bytes, filename)
