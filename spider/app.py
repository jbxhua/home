from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

@app.route("/")
def home():
    return render_template("index.html")  # Load homepage

@app.route('/upload', methods=['POST'])  
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.csv'):
        try:
            
            df = pd.read_csv(file)
            results = []

            for name_c in df['name']:
                name_encoded = quote(str(name_c))
                url = f"https://pubchem.ncbi.nlm.nih.gov/#query={name_encoded}"
                # site = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'
                # property = '/property/IUPACName,Title,MolecularWeight,MolecularFormula'
                # output = '/JSON'
                # url = f"{site}{name_encoded}{property}{output}"
                # Scrape PubChem
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                #soup = BeautifulSoup(response, 'html.parser')

                # r = request.get(url)
                # cont = r.json()
                # print(cont)
                
                #a_tag = soup.find('a', {'href': True})
                #url =  a_tag['href'] if a_tag else 'URL not found.'

                name = soup.find('div', class_ = 'break-words space-y-1')
                compound = name.get_text() if name else "Compound not found."

                results.append({
                    "CAS": cas_number,
                    "Compound": compound,
                    "URL": url
                })

                print(name)
            return jsonify({"data": results}), 200  # Send JSON data to frontend

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

if __name__ == '__main__':
    app.run(debug=True)
