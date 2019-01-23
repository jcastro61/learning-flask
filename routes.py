from flask import Flask, flash, redirect, render_template, request, session, abort

app = Flask(__name__)

@app.route("/")
def index():
	#return 'Flask app'
	return render_template('index.html')


@app.route("/about")
def about():
	return render_template('about.html')

	
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000,debug=True)