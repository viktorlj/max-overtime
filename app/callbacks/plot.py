"""Plot rendering and variant selection callbacks."""

from __future__ import annotations

import dash
import plotly.graph_objects as go
from dash import Input, Output, State, no_update
import polars as pl

from src.i18n import t

# Clinical-grade color palette for variant traces
_TRACE_COLORS = [
    "#2BB5A6",  # teal
    "#E8913A",  # amber
    "#6366F1",  # indigo
    "#D94F4F",  # coral
    "#14B8A6",  # emerald
    "#8B5CF6",  # purple
    "#F59E0B",  # gold
    "#EC4899",  # pink
    "#0EA5E9",  # sky
    "#84CC16",  # lime
]


def register(app: dash.Dash) -> None:
    """Register plot and table callbacks."""

    @app.callback(
        Output("variant-table", "columns"),
        Output("variant-table", "data"),
        Output("variant-table", "selected_rows"),
        Input("store-merged-data", "data"),
        State("store-language", "data"),
    )
    def update_table(data_json: str | None, lang: str):
        if not data_json:
            return [], [], []

        lang = lang or "en"
        df = pl.read_json(data_json.encode())

        timepoints = df["timepoint_label"].unique(maintain_order=True).to_list()

        df_display = df.with_columns(
            pl.when(pl.col("vaf").is_not_null())
            .then(
                pl.format(
                    "{}% ({})",
                    (pl.col("vaf") * 100).round(1).cast(pl.Utf8),
                    pl.col("depth").fill_null(pl.lit("N/A")).cast(pl.Utf8),
                )
            )
            .otherwise(pl.lit("\u2014"))
            .alias("display_value")
        )

        wide = df_display.pivot(
            on="timepoint_label",
            index=["gene", "transcript", "protein_change", "chrom", "pos", "variant_label"],
            values="display_value",
        )

        base_cols = ["gene", "transcript", "protein_change", "chrom", "pos"]
        tp_cols = [tp for tp in timepoints if tp in wide.columns]
        display_cols = base_cols + tp_cols
        wide = wide.select([c for c in display_cols if c in wide.columns])

        col_labels = {
            "gene": t("table.gene", lang),
            "transcript": t("table.transcript", lang),
            "protein_change": t("table.protein_change", lang),
            "chrom": t("table.chrom", lang),
            "pos": t("table.pos", lang),
        }

        columns = [{"name": col_labels.get(col, col), "id": col} for col in wide.columns]
        data = wide.to_dicts()
        selected = list(range(len(data)))

        return columns, data, selected

    @app.callback(
        Output("vaf-plot", "figure"),
        Input("variant-table", "selected_rows"),
        Input("variant-table", "data"),
        State("store-merged-data", "data"),
        State("store-sample-name", "data"),
        State("store-language", "data"),
    )
    def update_plot(
        selected_rows: list[int] | None,
        table_data: list[dict] | None,
        data_json: str | None,
        sample_name: str | None,
        lang: str,
    ):
        if not data_json or not table_data:
            return go.Figure()

        lang = lang or "en"
        df = pl.read_json(data_json.encode())

        if selected_rows is None:
            selected_rows = list(range(len(table_data)))

        selected_labels = set()
        for idx in selected_rows:
            if idx < len(table_data):
                row = table_data[idx]
                label_parts = []
                gene = row.get("gene", "")
                pc = row.get("protein_change", "")
                if gene:
                    label_parts.append(gene)
                if pc:
                    label_parts.append(pc)
                if not label_parts:
                    chrom = row.get("chrom", "")
                    pos = row.get("pos", "")
                    label_parts.append(f"{chrom}:{pos}")
                selected_labels.add(" ".join(label_parts))

        df_selected = df.filter(pl.col("variant_label").is_in(list(selected_labels)))

        if df_selected["date"].null_count() < len(df_selected):
            df_selected = df_selected.sort("date")

        fig = go.Figure()
        variants = df_selected["variant_label"].unique(maintain_order=True).to_list()

        for i, variant in enumerate(variants):
            v_data = df_selected.filter(pl.col("variant_label") == variant)

            x_vals = v_data["date"].to_list()
            if all(x is None or x == "" for x in x_vals):
                x_vals = v_data["timepoint_label"].to_list()

            y_vals = [(v * 100 if v is not None else 0) for v in v_data["vaf"].to_list()]
            depths = v_data["depth"].to_list()
            genes = v_data["gene"].to_list()
            pchanges = v_data["protein_change"].to_list()

            hover_text = []
            for j in range(len(y_vals)):
                parts = [f"VAF: {y_vals[j]:.1f}%"]
                if depths[j] is not None:
                    parts.append(f"Depth: {depths[j]}")
                if genes[j]:
                    parts.append(f"Gene: {genes[j]}")
                if pchanges[j]:
                    parts.append(f"Protein: {pchanges[j]}")
                hover_text.append("<br>".join(parts))

            color = _TRACE_COLORS[i % len(_TRACE_COLORS)]

            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode="lines+markers",
                    name=variant,
                    hovertext=hover_text,
                    hoverinfo="text+name",
                    marker=dict(size=9, color=color, line=dict(width=1.5, color="white")),
                    line=dict(width=2.5, color=color),
                )
            )

        fig.update_layout(
            title=dict(
                text=sample_name or "",
                font=dict(family="Sora, sans-serif", size=16, color="#1B2332"),
                x=0,
                xanchor="left",
            ),
            xaxis=dict(
                title=dict(
                    text=t("upload.date", lang),
                    font=dict(family="Figtree, sans-serif", size=12, color="#5E6778"),
                ),
                gridcolor="#ECEAE5",
                linecolor="#DDD9D2",
                tickfont=dict(family="Fira Code, monospace", size=11, color="#5E6778"),
            ),
            yaxis=dict(
                title=dict(
                    text=t("results.vaf_axis", lang),
                    font=dict(family="Figtree, sans-serif", size=12, color="#5E6778"),
                ),
                rangemode="tozero",
                gridcolor="#ECEAE5",
                linecolor="#DDD9D2",
                tickfont=dict(family="Fira Code, monospace", size=11, color="#5E6778"),
                ticksuffix="%",
            ),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.18,
                xanchor="center",
                x=0.5,
                font=dict(family="Figtree, sans-serif", size=12),
            ),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="rgba(0,0,0,0)",
            hovermode="x unified",
            margin=dict(l=60, r=20, t=50, b=80),
            hoverlabel=dict(
                bgcolor="white",
                font=dict(family="Figtree, sans-serif", size=12),
                bordercolor="#DDD9D2",
            ),
        )

        return fig
