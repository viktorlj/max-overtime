"""Entry point for MaxOvertime v2."""

from app import create_app

dash_app = create_app()
server = dash_app.server  # Flask WSGI app for gunicorn

if __name__ == "__main__":
    dash_app.run(debug=True)
