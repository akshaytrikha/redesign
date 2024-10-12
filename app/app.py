from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    # Get the URL from the form
    url = request.form.get('url')
    
    # Call the function from scrape.py
    result = scrape_function(url)
    
    # Return some response (you can customize this as needed)
    return result

if __name__ == '__main__':
    app.run(debug=True)
