# **Step 1: Create a Webhook in GitLab**

1. Navigate to your GitLab repository.
2. Go to **Settings > Webhooks**.
3. In the **URL** field, enter a webhook receiver endpoint. If you don’t have a server, you can use [GitHub Actions](https://docs.github.com/en/actions) or a service like [Zapier](https://zapier.com/) to handle webhooks.
4. Select **Merge request events** as the trigger.
5. **Enable SSL verification** (if applicable).
6. Click **Add webhook**.

> This webhook will be triggered whenever a merge request is updated.

---

# **Step 2: Create a Webhook Receiver**

You need a service to **process the webhook** and trigger the GitLab pipeline. If you have a server, you can write a simple Flask app.

## **How It Works**

- The Flask app listens for GitLab **merge request updates**.
- When a merge request is updated, it **checks the draft status**.
- If the draft status is **removed**, it triggers a **new pipeline**.

### **Steps to Run**

1. Install Flask:

   ```sh
   pip install flask requests
   ```

2. Run the server:

   ```sh
   python webhook_handler.py
   ```

3. Deploy the script to a server and expose it via a public URL

4. Copy the URL and set it as the webhook URL in GitLab.

### **Instruction for using Render.com (Free Hosted Server) to host Flask server**

📌 **How It Works:**

- Deploy a **Flask webhook server** for **free**.
- Your webhook runs **24/7 with a static URL**.

#### **Setup Steps:**

1. Push your Flask app to **GitHub**.
2. Deploy it on:
   - **[Render.com](https://render.com/)**
3. Get a **free static public URL**.

🔹 **Pros**: ✅ **Fully free**, **no need to keep your PC running**.
🔹 **Cons**: ❌ Needs GitHub deployment.

---
