from flask import Flask, Response

app = Flask(__name__)

@app.route("/")
def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sample Flask HTML Response</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #2c3e50; }
            p { color: #555; }
        </style>
    </head>
    <body>
        <h1>Hello from Flask!</h1>
        <p>This HTML page is returned directly from a Flask API endpoint.</p>
    </body>
    </html>
    """
    return Response(html_content, mimetype="text/html")

if __name__ == "__main__":
    app.run(debug=True)
