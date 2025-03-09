## **Step 1: Create a Webhook in GitLab**
1. Navigate to your GitLab repository.
2. Go to **Settings > Webhooks**.
3. In the **URL** field, enter a webhook receiver endpoint. If you don’t have a server, you can use [GitHub Actions](https://docs.github.com/en/actions) or a service like [Zapier](https://zapier.com/) to handle webhooks.
4. Select **Merge request events** as the trigger.
5. **Enable SSL verification** (if applicable).
6. Click **Add webhook**.

> This webhook will be triggered whenever a merge request is updated.

---

## **Step 2: Create a Webhook Receiver**
You need a service to **process the webhook** and trigger the GitLab pipeline. If you have a server, you can write a simple Flask app.

### **How It Works**
- The Flask app listens for GitLab **merge request updates**.
- When a merge request is updated, it **checks the draft status**.
- If the draft status is **removed**, it triggers a **new pipeline**.

#### **Steps to Run**
1. Install Flask:
   ```sh
   pip install flask requests
   ```
2. Run the server:
   ```sh
   python webhook_handler.py
   ```
3. Deploy the script to a server and expose it via a public URL (use **ngrok** for testing):
   ```sh
   ngrok http 5000
   ```
4. Copy the ngrok URL and set it as the webhook URL in GitLab.