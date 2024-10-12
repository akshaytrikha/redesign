# External
import re
from flask import Flask, render_template, request, jsonify

# Internal
from scrape import fetch_source
from infer import give_improvement_ideas

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

@app.route('/feedback', methods=['GET'])
def feedback():
    overall_improvement_output, overall_scores_output = give_improvement_ideas("silverpizzeria.com")
    scores = [int(score) for score in re.findall(r'\b\d+\b', overall_scores_output)]
    return render_template('feedback.html', scores=scores, ideas=overall_improvement_output)

if __name__ == '__main__':
    app.run(debug=True)
