# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(port=3000, debug=True)

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Serve the main page
@app.route("/")
def index():
    return render_template("new.html")

# Serve the generated speech file
@app.route("/output.mp3")
def get_audio():
    return send_from_directory(".", "output.mp3")  # current directory

if __name__ == "__main__":
    app.run(port=3000, debug=True)










