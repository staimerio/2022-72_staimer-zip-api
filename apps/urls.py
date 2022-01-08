# Retic
from retic import App as app

BACKEND_SENDFILES = {
    u"base_url": app.config.get('APP_BACKEND_SENDFILES'),
    u"files": "/files",
}

APP_BACKEND = {
    u"sendfiles": BACKEND_SENDFILES,
}

"""Add Backend apps"""
app.use(APP_BACKEND, "backend")
