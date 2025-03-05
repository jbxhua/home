from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from urllib.parse import quote

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

@app.route("/")
def home():
    return "Flask API is running!", 200

@app.route('/upload', methods=['POST'])  
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    
    if file.filename == '':
        return "No selected file", 400

    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)

        # Process CSV
        urls = []
        for cas_number in df['CAS']:
            cas_encoded = quote(str(cas_number))
            url = f"https://pubchem.ncbi.nlm.nih.gov/#query={cas_encoded}"
            urls.append(url)

        return {"urls": urls}, 200  # Return JSON response

    return "Invalid file format. Please upload a CSV file.", 400

if __name__ == '__main__':
    app.run(debug=True)
