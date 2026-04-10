"""Flask app for Webhook Logger"""
import json
import os
from flask import Flask, request, jsonify, render_template, g
from src.models import init_db, insert_webhook, get_recent_webhooks, get_webhook_by_id

# Explicitly set template and static folders
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Initialize DB on startup
init_db()


@app.before_request
def before_request():
    """Store request info for later use"""
    g.request_data = {
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent", ""),
        "headers": dict(request.headers)
    }


@app.route("/")
def index():
    """Show recent webhooks in HTML table"""
    webhooks = get_recent_webhooks(limit=50)
    return render_template("index.html", webhooks=webhooks)


@app.route("/webhook", methods=["POST"])
def receive_webhook():
    """Receive and store a webhook payload"""
    try:
        body = json.dumps(request.get_json(silent=True) or request.data.decode())
    except Exception:
        body = request.data.decode()
    
    webhook_id = insert_webhook(
        method=request.method,
        headers=json.dumps(g.request_data["headers"]),
        body=body,
        ip_address=g.request_data["ip"],
        user_agent=g.request_data["user_agent"]
    )
    
    return jsonify({
        "status": "success",
        "id": webhook_id,
        "message": "Webhook received"
    }), 201


@app.route("/logs", methods=["GET"])
def list_logs():
    """List recent webhooks"""
    webhooks = get_recent_webhooks(limit=50)
    return jsonify({"webhooks": webhooks, "count": len(webhooks)})


@app.route("/logs/<int:webhook_id>", methods=["GET"])
def get_log(webhook_id):
    """Get specific webhook details"""
    webhook = get_webhook_by_id(webhook_id)
    
    if not webhook:
        return jsonify({"error": "Webhook not found"}), 404
    
    return jsonify({"webhook": webhook})


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
