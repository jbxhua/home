import os
import requests
import pandas as pd
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from urllib.parse import quote

app = Flask(__name__)

PUBCHEM_API_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/JSON"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)

        results = []

        for cas_number in df['CAS']:
            cas_encoded = quote(str(cas_number))  # URL-encode CAS number
            url = PUBCHEM_API_URL.format(cas_encoded)

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                try:
                    compound_info = data['PC_Compounds'][0]
                    cid = compound_info['id']['id']['cid']
                    molecular_formula = compound_info['props'][0]['value']['sval']
                    compound_name = compound_info['props'][1]['value']['sval']

                    results.append({
                        "CAS": cas_number,
                        "CID": cid,
                        "Molecular Formula": molecular_formula,
                        "Compound Name": compound_name,
                        "PubChem Link": f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}"
                    })
                except KeyError:
                    results.append({"CAS": cas_number, "CID": "Not Found", "Molecular Formula": "N/A", "Compound Name": "N/A", "PubChem Link": "N/A"})
            else:
                results.append({"CAS": cas_number, "CID": "Error", "Molecular Formula": "N/A", "Compound Name": "N/A", "PubChem Link": "N/A"})

        return jsonify(results)

    return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
