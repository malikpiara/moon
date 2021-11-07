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
    articles = (page for page in pages if 'published' in page.meta)
    latest = sorted(
        articles, key=lambda page: page.meta['published'], reverse=True)
    return render_template('index.html', articles=latest[:25], title="Moonwith")


@app.route('/tag/<tag>/')
def tag(tag):
    articles = [page for page in pages if tag in page.meta.get('tags', [])]
    latest = sorted(
        articles, key=lambda page: page.meta['published'], reverse=True)
    # The comment below is a test to help me understand how the urls for
    # the pages are being generated.
    """ for page in pages:
        print(url_for('tag', tag=tag))
        print(url_for('page', path=page.path)) """

    return render_template('tagged.html', articles=latest[:25], tag=tag, title="Tagged")


@app.route('/feed.xml')
def rss():
    articles = (page for page in pages if 'published' in page.meta)
    latest = sorted(
        articles, key=lambda page: page.meta['published'], reverse=True)
    return render_template('feed.xml', articles=latest,
                           build_date=datetime.now())


@app.route("/about/")
def about():
    return render_template("about.html", title="About")


@app.route("/contact/")
def contact():
    return render_template("contact.html", title="Contact")


@app.route("/projects/")
def projects():
    return render_template("projects.html", title="Projects")


@app.route("/earnest-privacy/")
def earnest_privacy():
    return render_template("earnest-privacy.html", title="Earnest Cards Privacy Policy")

# This doesn't work when I make my website static.
# I probably have to create an app route.


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", title="Not Found"), 404


@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page, title=page.meta['title'])


@freezer.register_generator
# This function generates URLs for each post in pages.
def pagelist():
    for page in pages:
        # yield is a keyword like return
        yield url_for('page', path=page.path)
        # This doesn't seem to be giving me what I need
        yield url_for('tag', tag=tag)


# Attempt at finding every tag page and freezing it.
""" 
def taglist():
    for page in pages:
        yield url_for('tag', tag=tag) """


if __name__ == '__main__':
    # If the 'build' command is executed, freeze the app
    # and create static files. Otherwise, run it locally.
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', port=5001)
