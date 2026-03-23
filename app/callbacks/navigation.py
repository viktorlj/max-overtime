"""Page routing and navigation callbacks."""

from __future__ import annotations

import dash
from dash import Input, Output, State, no_update

from app.components.tutorial import create_tutorial


def register(app: dash.Dash) -> None:
    """Register navigation callbacks."""

    @app.callback(
        Output("analysis-page", "style"),
        Output("tutorial-page", "style"),
        Output("tutorial-page", "children"),
        Output("nav-analysis", "className"),
        Output("nav-tutorial", "className"),
        Input("url", "pathname"),
        Input("store-language", "data"),
    )
    def navigate(pathname: str | None, lang: str):
        lang = lang or "en"
        pathname = pathname or "/"

        active = "nav-link-clinical active"
        inactive = "nav-link-clinical"

        if pathname == "/tutorial":
            return (
                {"display": "none"},
                {"display": "block"},
                create_tutorial(lang),
                inactive,
                active,
            )

        return (
            {"display": "block"},
            {"display": "none"},
            no_update,
            active,
            inactive,
        )
