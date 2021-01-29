import sys
from flask import Flask, render_template, url_for
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from datetime import datetime

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)

# Passing app to get the information we need about the app
pages = FlatPages(app)
freezer = Freezer(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>.html')
def page(path):
    print("Page function running")
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)

@freezer.register_generator
# This function generates URLs for each post in pages.
def pagelist():
    for page in pages:
        # yield is a keyword like return
        yield url_for('page', path=page.path)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', port=5001)