from flask import Flask

DATABASE = 'database.db'


app = Flask(__UpComingSteamGames__)

@app.route('/')
def home():
    #home page
    return "Hello Again!"

if __name__ == "__main__":
    app.run(debug=True)