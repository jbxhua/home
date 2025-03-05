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
            for cas_number in df['CAS']:
                cas_encoded = quote(str(cas_number))
                url = f"https://pubchem.ncbi.nlm.nih.gov/#query={cas_encoded}"
                
                # Scrape PubChem
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract relevant data (Modify selectors based on actual page structure)
                name = soup.find("meta", {"name": "pubchem_title"})  # Example selector
                molecular_formula = soup.find("meta", {"name": "pubchem_formula"})
                title = soup.title.string if soup.title else "N/A"

                results.append({
                    "CAS": cas_number,
                    "Name": name["content"] if name else "N/A",
                    "Title": title if title else "N/A",
                    "URL": url
                })

            return jsonify({"data": results}), 200  # Send JSON data to frontend

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

if __name__ == '__main__':
    app.run(debug=True)
