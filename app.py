from flask import Flask, request, jsonify
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Load environment variables
GITLAB_URL = os.getenv("GITLAB_URL") # Example: "https://gitlab.com"
PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")
GITLAB_PRIVATE_TOKEN = os.getenv("GITLAB_PRIVATE_TOKEN")
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
                print(f"GitLab API Response Code: {response.status_code}")
                print(f"GitLab API Response: {response.text}")  # Log the response
                print(f"Raw Response Headers: {response.headers}")
                print(f"Raw Response Content: {response.content}")

                # Handle empty or malformed responses properly
                if response.status_code in [200, 201]:
                    try:
                        return jsonify(response.json()), response.status_code  # ✅ Return GitLab's response
                    except ValueError:
                        return jsonify({"message": f"Pipeline triggered for {source_branch}, but no content returned"}), response.status_code

                return jsonify({"error": "Unexpected response from GitLab", "details": response.text}), response.status_code

            except requests.exceptions.RequestException as e:
                print(f"Error triggering GitLab pipeline: {e}")
                return jsonify({"error": "Failed to trigger pipeline", "details": str(e)}), 500

    return jsonify({"message": "No action taken"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)
