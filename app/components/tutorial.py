"""Tutorial page component with step-by-step guide."""

from __future__ import annotations

from dash import html

from src.i18n import t


def create_tutorial(lang: str = "en") -> html.Div:
    """Build the full tutorial page content.

    Parameters
    ----------
    lang : str
        Language code ('en' or 'sv').
    """
    return html.Div(
        [
            # Hero
            html.Div(
                [
                    html.H1(t("tutorial.hero.title", lang)),
                    html.P(t("tutorial.hero.subtitle", lang)),
                ],
                className="tutorial-hero",
            ),

            # Workflow indicator bar
            html.Div(
                [
                    _workflow_step("1", t("tutorial.workflow.s1", lang)),
                    html.Div(className="workflow-connector"),
                    _workflow_step("2", t("tutorial.workflow.s2", lang)),
                    html.Div(className="workflow-connector"),
                    _workflow_step("3", t("tutorial.workflow.s3", lang)),
                    html.Div(className="workflow-connector"),
                    _workflow_step("4", t("tutorial.workflow.s4", lang)),
                ],
                className="workflow-bar",
            ),

            # Step 1: Prepare files
            _step_section(
                num="1",
                title=t("tutorial.step1.title", lang),
                children=[
                    html.P(t("tutorial.step1.desc", lang)),
                    html.Div(
                        [
                            _format_card(
                                t("tutorial.format.vcf.title", lang),
                                t("tutorial.format.vcf.desc", lang),
                            ),
                            _format_card(
                                t("tutorial.format.maf.title", lang),
                                t("tutorial.format.maf.desc", lang),
                            ),
                            _format_card(
                                t("tutorial.format.tsv.title", lang),
                                t("tutorial.format.tsv.desc", lang),
                            ),
                        ],
                        className="format-grid",
                    ),
                    # Column requirements table
                    html.H5(
                        t("tutorial.column_reqs", lang),
                        style={
                            "fontSize": "14px",
                            "fontWeight": "600",
                            "marginTop": "20px",
                            "marginBottom": "8px",
                        },
                    ),
                    _column_table(lang),
                ],
            ),

            # Step 2: Set up timepoints
            _step_section(
                num="2",
                title=t("tutorial.step2.title", lang),
                children=[
                    html.P(t("tutorial.step2.desc", lang)),
                    html.Div(
                        [
                            html.Strong("Tip: "),
                            t("tutorial.step2.tip", lang),
                        ],
                        className="tip-callout",
                    ),
                ],
            ),

            # Step 3: Analyze & Interpret
            _step_section(
                num="3",
                title=t("tutorial.step3.title", lang),
                children=[
                    html.P(t("tutorial.step3.desc", lang)),
                    html.P(t("tutorial.step3.plot", lang)),
                    html.P(t("tutorial.step3.table", lang)),
                ],
            ),

            # Step 4: Export
            _step_section(
                num="4",
                title=t("tutorial.step4.title", lang),
                children=[
                    html.P(t("tutorial.step4.desc", lang)),
                    html.Div(
                        [
                            _export_card("PDF", t("tutorial.step4.pdf", lang)),
                            _export_card("Excel", t("tutorial.step4.excel", lang)),
                            _export_card("TSV", t("tutorial.step4.tsv", lang)),
                        ],
                        className="export-grid",
                    ),
                ],
            ),

            # Back button
            html.Div(
                html.A(
                    "\u2190  " + t("tutorial.back", lang),
                    href="/",
                    className="btn-back",
                ),
                style={"textAlign": "center", "marginTop": "40px"},
            ),
        ],
        className="tutorial-page",
    )


def _workflow_step(num: str, label: str) -> html.Div:
    return html.Div(
        [
            html.Div(num, className="workflow-num"),
            html.Span(label, className="workflow-label"),
        ],
        className="workflow-step",
    )


def _step_section(num: str, title: str, children: list) -> html.Div:
    return html.Div(
        [
            html.Div(
                [
                    html.Div(num, className="step-num"),
                    html.H3(title, className="step-title"),
                ],
                className="step-header",
            ),
            html.Div(children, className="step-body"),
        ],
        className="tutorial-step",
    )


def _format_card(title: str, desc: str) -> html.Div:
    return html.Div(
        [
            html.Span(title, className="format-tag"),
            html.P(desc, className="format-desc"),
        ],
        className="format-card",
    )


def _export_card(label: str, desc: str) -> html.Div:
    return html.Div(
        [
            html.Div(label, className="export-card-label"),
            html.P(desc, className="export-card-desc"),
        ],
        className="export-card",
    )


def _column_table(lang: str) -> html.Table:
    req = t("tutorial.col.required", lang)
    rec = t("tutorial.col.recommended", lang)
    opt = t("tutorial.col.optional", lang)

    def _badge(text: str, level: str) -> html.Span:
        return html.Span(text, className=f"req-badge req-badge-{level}")

    rows = [
        ("chrom / chromosome / chr", _badge(req, "required"), "Chromosome identifier"),
        ("pos / position / start", _badge(req, "required"), "Genomic position (1-based)"),
        ("ref / reference", _badge(req, "required"), "Reference allele"),
        ("alt / alternate", _badge(req, "required"), "Alternate allele"),
        ("vaf / af", _badge(rec, "recommended"), "Variant allele frequency (0\u20131)"),
        ("gene / hugo_symbol", _badge(rec, "recommended"), "Gene symbol (HGNC)"),
        ("protein_change / hgvsp", _badge(rec, "recommended"), "Protein change (HGVS)"),
        ("depth / dp", _badge(opt, "optional"), "Sequencing read depth"),
        ("transcript", _badge(opt, "optional"), "Transcript ID (RefSeq/Ensembl)"),
    ]

    return html.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Column"),
                        html.Th("Status"),
                        html.Th("Description"),
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr([html.Td(col), html.Td(badge), html.Td(desc)])
                    for col, badge, desc in rows
                ]
            ),
        ],
        className="col-req-table",
    )
