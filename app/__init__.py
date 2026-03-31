"""Dash application factory for MaxOvertime v2."""

from __future__ import annotations

from pathlib import Path

import dash
import dash_bootstrap_components as dbc

# Project root: one level up from this file's directory (app/)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def create_app() -> dash.Dash:
    """Create and configure the Dash application."""
    app = dash.Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=DM+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap",
        ],
        suppress_callback_exceptions=True,
        assets_folder=str(_PROJECT_ROOT / "assets"),
        title="Max Overtime",
    )
    app._favicon = "favicon.svg"

    from app.layout import build_layout

    app.layout = build_layout()

    from app.callbacks import language, navigation, upload, processing, plot, export

    language.register(app)
    navigation.register(app)
    upload.register(app)
    processing.register(app)
    plot.register(app)
    export.register(app)

    return app
