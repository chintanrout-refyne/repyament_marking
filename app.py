from flask import Flask, render_template, request
import csv
import json
import sys  # Import the sys module

app = Flask(__name__)

try:
    import requests
except ImportError:
    print("The 'requests' library is not installed. Installing it...")
    try:
        import subprocess
        subprocess.check_call(['pip', 'install', 'requests'])
        import requests  # Try importing again
    except Exception as e:
        print("Failed to install 'requests' library:", e)
        sys.exit(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    csv_file = request.files['csvFile']
    bearer_token = request.form['bearerToken']

    # Set the endpoint URL
    url = "https://api.beta.prod.refyne.co.in/refyne-admin/emi-repayment"

    # Set the headers
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }

    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            payload = {
                "userId": row['UserID'],
                "emiAmount": int(row['emiAmount']),
                "paidAt": "2023-08-16T20:55:24.953Z"
            }
            
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                print(f"Successfully sent EMI repayment for UserID: {row['UserID']}")
            else:
                print(f"Failed to send EMI repayment for UserID: {row['UserID']}, Status Code: {response.status_code}")
                sys.exit(1)  # Exit the script with a non-zero status code

    return "CSV data uploaded and processed."

if __name__ == '__main__':
    app.run(debug=True, port=5000)
