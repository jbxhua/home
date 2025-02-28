import requests
import pandas as pd
from flask import Flask, request, render_template
from urllib.parse import quote

app = Flask(__name__)

PUBCHEM_API_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/JSON"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)

        results = []

        for cas_number in df['CAS']:
            cas_encoded = quote(str(cas_number))  # URL-encode CAS number
            url = PUBCHEM_API_URL.format(cas_encoded)

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                # Extract relevant info (e.g., CID, molecular formula, name)
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

        return render_template('results.html', results=results)

    return "Invalid file format. Please upload a CSV file."

if __name__ == '__main__':
    app.run(debug=True)
