import requests
import pandas as pd
from flask import Flask, request, render_template
from urllib.parse import quote
from bs4 import BeautifulSoup

# Load CSV (assuming a column named 'CAS' contains the CAS numbers)
df = pd.read_csv("your_file.csv")

# Iterate through each CAS number and construct the URL
for cas_number in df['CAS']:
    cas_encoded = quote(str(cas_number))  # URL-encode the CAS number
    url = f"https://pubchem.ncbi.nlm.nih.gov/#query={cas_encoded}"
    print(url)



r = requests.get('https://pubchem.ncbi.nlm.nih.gov/')

print(r)

soup = BeautifulSoup(r.content, 'html.parser')
print(soup.prettify())









