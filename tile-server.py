from flask import Flask
from flask import send_file

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/<int:zoom>/<int:x>/<int:y>.png')
def show_tile(zoom, x, y):
	filename = '%d/%d/%d.png' % (zoom, x, y)
	return send_file(filename, mimetype='image/png')
