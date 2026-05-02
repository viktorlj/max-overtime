"""Main layout with client-side routing between Analysis and Tutorial pages."""

from __future__ import annotations

from dash import dcc, html

from app.components.navbar import create_navbar
from app.components.upload_section import create_upload_section
from app.components.plot_section import create_plot_section
from app.components.variant_table import create_variant_table


def build_layout() -> html.Div:
    """Compose the full application layout.

    Both pages are always mounted (for state preservation).
    Visibility is toggled via the navigation callback.
    """
    return html.Div(
        [
            # Routing & stores
            dcc.Location(id="url", refresh=False),
            dcc.Store(id="store-language", storage_type="local", data="en"),
            dcc.Store(id="store-merged-data", storage_type="memory"),
            dcc.Store(id="store-sample-name", storage_type="memory"),

            # Navbar (always visible)
            create_navbar(),

            # Analysis page
            html.Div(
                html.Div(
                    [
                        create_upload_section(),
                        create_plot_section(),
                        create_variant_table(),
                    ],
                    className="content-wrapper",
                ),
                id="analysis-page",
            ),

            # Tutorial page (hidden by default, populated via callback)
            html.Div(
                id="tutorial-page",
                style={"display": "none"},
            ),

            html.Footer(
                html.Div(
                    html.P(
                        "Max Overtime. For research use and clinical decision support only. "
                        "Not a standalone diagnostic device. Outputs may be incomplete or "
                        "incorrect and must be reviewed by qualified experts in the full "
                        "clinical, laboratory, and histopathological context. The authors "
                        "assume no responsibility for clinical decisions or other "
                        "consequences of use.",
                        id="disclaimer-text",
                        className="mp-soft",
                    ),
                    className="app-footer-inner",
                ),
                className="app-footer",
            ),
        ],
    )
