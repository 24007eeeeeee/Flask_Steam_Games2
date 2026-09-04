from flask import Flask, g, render_template
import sqlite3

DATABASE = 'database.db'

#Initialise Flask application
app = Flask(__name__)

def get_db():
    #Open and return a database connection tied to the current request (g context)
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        #Makes it use column names like 'cost' instead of numbers like game[3]
        db.row_factory = sqlite3.Row 
    return db

@app.teardown_appcontext
def close_connection(exception):
    #Closes the database connection automatically when the application context ends
    db = getattr(g, '_database', None)
    if db is not None:
        db.close() 

def query_db(query, args=(), one=False):
    #Helper function to execute SQL queries and fetch results
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    #Returns a single dictionary-like row if one=True, otherwise returns a list of rows
    return (rv[0] if rv else None) if one else rv

#Home route, displays a list of all games joined with their studio information
@app.route('/')
def home():
    # Selecting GameID(0), Studio Name(1), ImageURL(2), Cost(3), Description(4), and VideoURL(6)
    sql = """SELECT SteamGames.GameID, SteamGames.Game, SteamGames.ImageURL, SteamGames.Cost, SteamGames.Description, SteamGames.VideoURL
    FROM SteamGames
    JOIN Studios ON Studios.StudioID=SteamGames.StudioID;"""
    results = query_db(sql)
    return render_template("home.html", results=results)

#Game detail route, fetches a single game using its unique ID
@app.route("/game/<int:id>")
def game(id):
    #just one game based on the id
    sql = """SELECT * FROM SteamGames
    JOIN Studios ON Studios.StudioID=SteamGames.StudioID
    WHERE SteamGames.GameID = ?;"""
    result = query_db(sql,(id,),True)
    return render_template("game.html", game=result)

#Studio description page route
@app.route('/studiodesc')
def description():
    return render_template("studiodesc.html")

#Favorite steam games page route
@app.route('/myfavouritesteamgames')
def favouritesteamgames():
    return render_template("myfavouritesteamgames.html")

#Run the Flask development server in debug mode
if __name__ == "__main__":
    app.run(debug=True)


