from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],  
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/api/process_text', methods=['POST', 'OPTIONS'])
def handle_query():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Invalid request"}), 400
    
    result = {
        "original_url": data['url'],
        "processed": True,
        "message": "URL received successfully"
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)