# Third-party imports
from flask import Flask, jsonify, request, render_template, redirect
from flask_pymongo import PyMongo
# from werkzeug import secure_filename
import base64
from mood import main_func


# Initialize app and database
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'moodmusic'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/moodmusic'

mongo = PyMongo(app)

# Setup routes
@app.route('/')
def index():
  return redirect("/ind")

@app.route('/ind')
def ind():
  return render_template("index.html")

@app.route('/player')
def player():
  return render_template("player.html")

@app.route('/cam')
def cam():
  return render_template("cam.html")

@app.route('/music', methods=['GET'])
def music():
  songs = mongo.db.songs
  output = []
  for s in songs.find({'mood' : request.args.get("mood")}):
    output.append({'id' : s['id'],'title' : s['title'], 'album': s['album'], 'artist' : s['artist'], 'albumart' : s['albumart'], 'url' : s['url']})
  return jsonify(output)

@app.route('/emotion', methods=['GET', 'POST'])
def emotion():
  # Get img data
  img_data = request.form['img']
  img_data = img_data[23:]

  # Decode the img and save as snap.jpg
  f = open("snap.jpg", "wb")
  f.write(base64.b64decode(img_data.encode('ascii')))
  f.close()

  # Run script for emotion recognition
  mood = main_func()

  return redirect("/player?mood=" + mood)

# Main
if __name__ == '__main__':
  app.run(debug=True,ssl_context='adhoc')
