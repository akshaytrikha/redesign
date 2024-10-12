# External
from flask import Flask, render_template, request, jsonify

# Internal
from scrape import fetch_source

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    # Get the URL from the form
    url = request.form.get('url')
    if not url:
        return jsonify({"status": "error", "message": "No URL provided."}), 400

    # Call the function from scrape.py
    result = fetch_source(url)

    # Return JSON response
    if result["status"] == "success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400


if __name__ == '__main__':
    app.run(debug=True)
