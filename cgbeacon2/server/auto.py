from werkzeug.contrib.fixers import ProxyFix
from cgbeacon2.server import create_app

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)
