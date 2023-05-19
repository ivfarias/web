from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def get_file():
    file_url = request.json.get('file_url')
    df = pd.read_table(file_url, nrows=100, header=None, encoding='ISO-8859-1')
    json_data = df.to_json(orient='records')
    response = {
        'payload': json_data
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
