from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    data = {
        "key": "value",
        "number": 123,
        "array": [1, 2, 3],
        "nested": {
            "name": "example",
            "boolean": True
        }
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
