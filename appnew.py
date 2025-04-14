from flask import Flask, render_template

app = Flask(__name__)

# Home Route
@app.route("/")
def home():
    return render_template("home.html")

# AI Marketing Bot Route
@app.route("/ai-customercare-bot")
def ai_marketing_bot():
    return render_template("bot1.html")  # The page.html you've created

if __name__ == "__main__":
    app.run(port=3000, debug=True)
