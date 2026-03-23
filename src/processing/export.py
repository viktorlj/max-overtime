"""Export functions for PDF, Excel, and TSV."""

from __future__ import annotations

import io

import polars as pl
import plotly.graph_objects as go


def export_pdf(fig: go.Figure) -> bytes:
    """Export a Plotly figure to PDF bytes.

    Parameters
    ----------
    fig : go.Figure
        Plotly figure object.

    Returns
    -------
    bytes
        PDF content as bytes.
    """
    return fig.to_image(format="pdf", scale=3, width=1000, height=600)


def export_excel(df: pl.DataFrame, sample_name: str = "") -> bytes:
    """Export variant data to an Excel workbook.

    Creates a wide-format table showing "VAF% (depth)" per timepoint.

    Parameters
    ----------
    df : pl.DataFrame
        Long-format merged DataFrame.
    sample_name : str
        Sample name for the sheet title.

    Returns
    -------
    bytes
        Excel workbook as bytes.
    """
    # Create wide-format: one row per variant, columns per timepoint
    timepoints = df["timepoint_label"].unique(maintain_order=True).to_list()

    # Build display value: "VAF% (depth)"
    df_display = df.with_columns(
        pl.when(pl.col("vaf").is_not_null())
        .then(
            pl.format(
                "{}% ({})",
                (pl.col("vaf") * 100).round(1).cast(pl.Utf8),
                pl.col("depth").fill_null(pl.lit("N/A")).cast(pl.Utf8),
            )
        )
        .otherwise(pl.lit("—"))
        .alias("display_value")
    )

    # Pivot to wide format
    wide = df_display.pivot(
        on="timepoint_label",
        index=["gene", "transcript", "protein_change", "chrom", "pos", "ref", "alt", "variant_label"],
        values="display_value",
    )

    # Reorder timepoint columns
    base_cols = ["gene", "transcript", "protein_change", "chrom", "pos", "ref", "alt", "variant_label"]
    ordered_cols = base_cols + [tp for tp in timepoints if tp in wide.columns]
    wide = wide.select(ordered_cols)

    buf = io.BytesIO()
    wide.write_excel(
        buf,
        worksheet=sample_name or "Variants",
    )
    return buf.getvalue()


def export_tsv(df: pl.DataFrame) -> bytes:
    """Export the long-format DataFrame as TSV.

    Parameters
    ----------
    df : pl.DataFrame
        Long-format merged DataFrame.

    Returns
    -------
    bytes
        TSV content as bytes.
    """
    buf = io.BytesIO()
    df.write_csv(buf, separator="\t")
    return buf.getvalue()
