"""Controls the web server for the entire site with a Flask framework. Assumes
that the main app is app.py. Contains links to the rest of the site, and it
handles non-static downloads.
"""

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import abort
from flask import redirect
from flask import url_for
from flask import send_file

import os
import sys
sys.path.insert(0, 'static/py')

import fetch

#from flaskext.mysql import MySQL

from bs4 import BeautifulSoup

app = Flask(__name__)

__author__ = "Robbie Freeman"
__credits__ = ["Robbie Freeman"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

# calls the app so it can run
if __name__ == "__main__":
    app.run()

import psycopg2
DATABASE_URL = os.environ['postgresql-convex-91631']
try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        conn.close()
        print("connected!")
    except:
        print("not connected!")


# loads home
@app.route('/')
@app.route('/home')
@app.route('/index')
def changelog():
    fetch.fetchHomePage()
    return render_template('history.html')

# 2/27/19 - experimental route that pulls searches
@app.route('/suggestions')
def suggestions():
    print("in suggestions")
    text = request.args.get('jsdata')
    codes = []
    queryTerms = text.split(" ") # use later to search for specific terms like map
    if text:
        # Assumption: there better only by one instance of 1vX. if not takes the first one
        clutchKills = -1 # -1 means no requirement
        i = text.find("1v")
        if i > -1 and len(text) - i > 2:
            clutchKills = int(text[i + 2])
            if clutchKills and 0 <= clutchKills and 5 >= clutchKills: # if there's a number after v
                clutchKills = int(text[i + 2])
            else:
                clutchKills = -1

        for d in data:
            if queryRequirements(text) and (text in d or text.lower() in d or d[15] == clutchKills) and d[0] not in codes:
                codes.append(d[0])


        print("out suggestions")

    return jsonify(codes)

def queryRequirements(q):
    if q == 'Y' or q == 'N':
        return False
    return True

# basic 404 page. Hopefully isn't called all that often TODO: implement
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# loads About page
@app.route('/about')
def about():
    return render_template('about.html')

# loads the page with list of articles TODO implement
@app.route('/article/<query>')
def article(query):
        return render_template('articleFiles/' + query + '.html')

# loads the page with list of articles TODO get rid of
@app.route('/article')
def exArticle():
    return render_template('article.html')

# loads the page with list of articles TODO implement
@app.route('/articles')
def articles():
    return render_template('index.html')

# loads contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# loads Hall of History page
@app.route('/history')
def history():
    return render_template('history.html')

# loads Smoke Stop page
@app.route('/smokestop')
def smokestop():
    return render_template('smokestop.html')
