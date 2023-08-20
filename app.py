from flask import Flask, render_template, request
from datetime import date, datetime
import csv
import json
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    csv_file = request.files['csvFile']
    bearer_token = request.form['bearerToken']

    # Ensure the CSV file exists
    if csv_file:
        # Read the CSV file contents
        csv_contents = csv_file.read().decode('utf-8')
        current_date = datetime.utcnow().strftime("%Y-%m-%dT") + "20:55:24.953Z"
        # API endpoint URL
        url = "https://api.beta.prod.refyne.co.in/refyne-admin/emi-repayment"
        
        # Headers
        headers = {
            'accept': '*/*',
            'Authorization': f'Bearer {bearer_token}',
            'Content-Type': 'application/json'
        }
        
        # Process the CSV contents
        csv_rows = csv.reader(csv_contents.splitlines())  # Use csv.reader instead of csv.DictReader
        header = next(csv_rows)  # Read the header row
        
        # Assuming the CSV has 'UserID' and 'emiAmount' columns
        user_id_index = header.index('UserID')
        emi_amount_index = header.index('emiAmount')

        for row in csv_rows:
            payload = {
                "userId": row[user_id_index],
                "emiAmount": float(row[emi_amount_index]),
                "paidAt": current_date
            }
            
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            
            if response.status_code == 201:
                print(f"Successfully sent EMI repayment for UserID: {row[user_id_index]}")
            else:
                print(f"Failed to send EMI repayment for UserID: {row[user_id_index]}, Status Code: {response.status_code}")

        return "CSV data uploaded and processed."
    else:
        return "No CSV file uploaded."

if __name__ == '__main__':
    app.run(debug=True)
