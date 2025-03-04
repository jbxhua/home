from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from urllib.parse import quote

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the PubChem API! Use the /upload endpoint to upload a CSV."}), 200  # Ensure JSON response

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Read the CSV file
    try:
        df = pd.read_csv(file)
        if 'CAS' not in df.columns:
            return jsonify({"error": "CSV must contain a 'CAS' column"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to read CSV: {str(e)}"}), 400

    # Generate PubChem URLs for each CAS number
    urls = []
    for cas_number in df['CAS']:
        cas_encoded = quote(str(cas_number))  # URL-encode CAS number
        url = f"https://pubchem.ncbi.nlm.nih.gov/#query={cas_encoded}"
        urls.append({"CAS": cas_number, "PubChem_URL": url})

    return jsonify({"message": "File processed successfully", "data": urls}), 200  # Ensure JSON response

if __name__ == '__main__':
    app.run(debug=True)
