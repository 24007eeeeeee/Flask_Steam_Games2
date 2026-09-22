"""Flask application to display Steam games and studio details from a SQLite database."""

import sqlite3
from flask import (
    Flask,
    g,
    render_template,
)

DATABASE = 'database.db'

# Initialise Flask application
app = Flask(__name__)


def get_db():
    """Open and return a database connection tied to the current request context."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Makes it use column names like 'cost' instead of numbers like game[3]
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection automatically when the application context ends"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close() 


def query_db(query, args=(), one=False):
    """Execute SQL queries and fetch results

    Returns a single row if one=True, otherwise returns a list of rows.
    """

    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    #Returns a single dictionary-like row if one=True, otherwise returns a list of rows
    return (rv[0] if rv else None) if one else rv


#Home route, displays a list of all games joined with their studio information
@app.route('/')
def home():
    """Display a list of all games joined with their studio info
    
    Selects GameID, Studio Name, ImageURL, Cost, Description, and VideoURL
    """
    sql = """SELECT SteamGames.GameID, SteamGames.Game, SteamGames.ImageURL, SteamGames.Cost, SteamGames.Description, SteamGames.VideoURL
    FROM SteamGames
    JOIN Studios ON Studios.StudioID=SteamGames.StudioID;"""
    results = query_db(sql)
    return render_template("home.html", results=results)


#Game detail route, fetches a single game using its unique ID
@app.route("/game/<int:id>")
def game(id):
    """Fetches and display a single steam game by its unique ID."""
    sql = """SELECT * FROM SteamGames
    JOIN Studios ON Studios.StudioID=SteamGames.StudioID
    WHERE SteamGames.GameID = ?;"""
    result = query_db(sql,(id,),True)
    return render_template("game.html", game=result)


# Studio description page route
@app.route('/studiodesc')
def description():
    """Render the studio description page."""
    return render_template("studiodesc.html")


# Favorite steam games page route
@app.route('/myfavouritesteamgames')
def favouritesteamgames():
    """Render the user's favorite steam games page."""
    return render_template("myfavouritesteamgames.html")


@app.errorhandler(404)
def page_not_found(_error):
    """Render a custom 404 page error screen."""
    return render_template("error404.html"), 404


#Run the Flask development server in debug mode
if __name__ == "__main__":
    app.run(debug=True)
