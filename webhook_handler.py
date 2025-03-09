from flask import Flask, request, jsonify
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

GITLAB_URL = os.getenv("GITLAB_URL")
GITLAB_PRIVATE_TOKEN = os.getenv("GITLAB_PRIVATE_TOKEN")
PROJECT_ID = os.getenv("PROJECT_ID")

GITLAB_TRIGGER_TOKEN = os.getenv("GITLAB_TRIGGER_TOKEN")
GITLAB_TRIGGER_URL = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/trigger/pipeline?token={GITLAB_TRIGGER_TOKEN}"


@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    print("Webhook received:", data)  # Debugging

    # Log received data for debugging
    with open("webhook_log.json", "w") as log_file:
        json.dump(data, log_file, indent=4)
    
    print("Received Webhook:", json.dumps(data, indent=4))  # Print to console for debugging

    if data and "object_kind" in data and data["object_kind"] == "merge_request":
        title = data["object_attributes"]["title"]
        draft_status = data["object_attributes"]["draft"]
        source_branch = data["object_attributes"]["source_branch"]

        # Debugging logs
        print(f"Title: {title}, Draft Status: {draft_status}, Source Branch: {source_branch}")

        # Ensure we only trigger when the draft status is removed
        if draft_status is False:  # Draft was removed
            print(f"Draft status removed for branch {source_branch}. Triggering pipeline...")

            try:
                response = requests.post(
                    GITLAB_TRIGGER_URL,
                    headers={"PRIVATE-TOKEN": GITLAB_PRIVATE_TOKEN},
                    json={"token": GITLAB_TRIGGER_TOKEN, "ref": source_branch},
                    timeout=10  # Avoid long waits
                )
                response.raise_for_status()  # Raise an error for failed requests

                # Debugging GitLab API response
                print(f"GitLab API Response: {response.status_code}, {response.text}")
                print(f"Raw Response Headers: {response.headers}")
                print(f"Raw Response Content: {response.content}")

                return jsonify(response.json()), response.status_code  # ✅ Returns GitLab's full response

            except requests.exceptions.RequestException as e:
                print(f"Error triggering GitLab pipeline: {e}")
                return jsonify({"error": "Failed to trigger pipeline", "details": str(e)}), 500

    return jsonify({"message": "No action taken"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)
