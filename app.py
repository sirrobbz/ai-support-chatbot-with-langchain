from flask import Flask, render_template
from routes.chat_routes import chat_bp

app = Flask(__name__, template_folder="templates")
app.register_blueprint(chat_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
