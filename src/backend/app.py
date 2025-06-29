import os
import markdown

from flask import Flask, request, jsonify, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
        }
    },
)


@app.route("/api/process_text", methods=["POST", "OPTIONS"])
def handle_query():
    """handle query for processing web url info

    Returns:
        Response: Returing status of getting web url which the user inputs.
    """
    if request.method == "OPTIONS":
        return jsonify({}), 200

    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Invalid request"}), 400

    result = {
        "original_url": data["url"],
        "processed": True,
        "message": "URL received successfully",
    }

    return jsonify(result)


@app.route("/markdown", methods=["GET"])
def serve_markdown():
    """showing the content of markdown file

    Returns:
        Response: The response for reading markdown file
    """
    md_path = os.path.join(os.path.dirname(__file__), "../data/index.md")
    if not os.path.exists(md_path):
        return Response("Markdown file not found.", status=404, mimetype="text/plain")
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
    html = markdown.markdown(content, extensions=["fenced_code", "tables"])
    
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 2em; }}
            pre, code {{ background: #f4f4f4; border-radius: 4px; padding: 2px 6px; }}
            table {{ border-collapse: collapse; }}
            th, td {{ border: 1px solid #ccc; padding: 4px 8px; }}
        </style>
    </head>
    <body>
    {html}
    </body>
    </html>
    """
    return Response(html, mimetype="text/html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
