"""Navbar: hexagonal brand mark, navigation links, and language toggle."""

from __future__ import annotations

from dash import html, dcc


def create_navbar() -> html.Div:
    """Create the top navigation bar with clinical design."""
    return html.Div(
        html.Div(
            [
                # Brand group
                html.Div(
                    [
                        html.Div("M", className="brand-mark"),
                        html.Div(
                            [
                                html.Span("Max Overtime", className="brand-name"),
                                html.Span(
                                    "Variant Allele Frequency Tracker",
                                    className="brand-tagline",
                                    id="brand-tagline",
                                ),
                            ],
                            className="brand-text",
                        ),
                    ],
                    className="brand-group",
                ),
                # Navigation + language
                html.Div(
                    [
                        html.A(
                            "Analysis",
                            id="nav-analysis",
                            href="/",
                            className="nav-link-clinical active",
                        ),
                        html.A(
                            "Tutorial",
                            id="nav-tutorial",
                            href="/tutorial",
                            className="nav-link-clinical",
                        ),
                        html.Div(className="nav-divider"),
                        html.Div(
                            [
                                html.Button(
                                    "EN",
                                    id="btn-lang-en",
                                    className="lang-btn lang-btn-active",
                                ),
                                html.Button(
                                    "SV",
                                    id="btn-lang-sv",
                                    className="lang-btn lang-btn-inactive",
                                ),
                            ],
                            className="lang-toggle",
                        ),
                    ],
                    className="nav-controls",
                ),
            ],
            className="navbar-inner",
        ),
        className="navbar-clinical",
    )
