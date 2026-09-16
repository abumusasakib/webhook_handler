# GitLab Merge Request Webhook Handler

This is a **Flask application** that listens for **GitLab webhook events** and triggers a pipeline when a **merge request draft status is removed**. The application can be deployed on **Render.com** for a free and publicly accessible webhook endpoint.

---

## 🚀 Features

- ✅ **Listens for GitLab Webhooks** for merge request updates.
- ✅ **Triggers GitLab CI/CD Pipelines** when a draft is removed.
- ✅ **Logs Webhook Events** for debugging.
- ✅ **Deployable on Render.com** for a **free static public URL**.

---

## 📌 Setup Instructions

### **1️⃣ Clone the Repository**

```sh
git clone <git_repo_link>
cd gitlab-webhook-handler
```

### **2️⃣ Install Dependencies**

Ensure you have **Python 3.8+** installed.

```sh
pip install -r requirements.txt
```

### **3️⃣ Set Up Environment Variables**

Create a **`.env` file** in the root directory and add:

```sh
GITLAB_URL=https://gitlab.com
GITLAB_PROJECT_ID=your_project_id
GITLAB_PRIVATE_TOKEN=your_gitlab_private_token
GITLAB_TRIGGER_TOKEN=your_gitlab_trigger_token
```

### **4️⃣ Run the Flask Application Locally**

```sh
python app.py
```

By default, the app runs on **port 6000**. If deploying on **Render.com**, the port is automatically assigned.

---

## 🌐 Deploying on Render.com (Free Hosted Server)

### **1️⃣ Push Your Code to GitHub**

```sh
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <git_repo_link>
git push -u origin main
```

### **2️⃣ Deploy to Render**

1. Go to [Render.com](https://render.com/).
2. Click **"New Web Service"** and connect your GitHub repository.
3. Set **Build Command:**

   ```sh
   pip install -r requirements.txt
   ```

4. Set **Start Command:**

   ```sh
   gunicorn wsgi:app
   ```

5. Click **Deploy**.
6. Once deployed, copy the **public URL** (e.g., `https://your-app.onrender.com`).

---

## 🐳 Running with Docker

The app can also be run in a container instead of directly with Python/Gunicorn — useful when co-hosting it on a machine that already runs other Dockerized services.

### **1️⃣ Set Up Environment Variables**

Create a **`.env` file** in the root directory (same as above) and additionally set the host port to publish the container on:

```sh
GITLAB_URL=https://gitlab.com
GITLAB_PROJECT_ID=your_project_id
GITLAB_PRIVATE_TOKEN=your_gitlab_private_token
GITLAB_TRIGGER_TOKEN=your_gitlab_trigger_token

WEBHOOK_PORT=8201
```

`WEBHOOK_PORT` is the port exposed on the **host**; the container always listens on `6000` internally.

### **2️⃣ Build and Start the Container**

```sh
docker compose up -d --build
```

This builds the image from the `Dockerfile` and starts the app with Gunicorn, bound to `0.0.0.0:6000` inside the container and published to `${WEBHOOK_PORT}` on the host.

### **3️⃣ Verify It's Running**

```sh
docker compose ps
docker compose logs -f webhook-handler
```

The handler should now be reachable at `http://<host>:${WEBHOOK_PORT}/`.

### **4️⃣ Stop / Restart**

```sh
docker compose down
docker compose up -d --build   # rebuild after code changes
```

### Notes for shared hosts

- Pick a `WEBHOOK_PORT` that doesn't collide with other services already running on the host.
- `docker-compose.yml` and `Dockerfile` in this repo are intentionally standalone — they build and run only this Flask app, and don't share a network or reverse proxy with any other project's containers.

---

## 🔗 Setting Up GitLab Webhook

### **1️⃣ Add a Webhook to Your GitLab Repository**

1. Navigate to **GitLab → Settings → Webhooks**.
2. Set **Webhook URL** to your **Render URL** (e.g., `https://your-app.onrender.com/`).
3. Enable **"Merge Request Events"**.
4. Click **"Add webhook"**.

### **2️⃣ Test the Webhook**

1. **Create a Merge Request** in GitLab.
2. Change it from **Draft → Ready**.
3. Check **GitLab → CI/CD → Pipelines** to see if it was triggered.

---

## 🛠 Project Structure

```text
├── app.py               # Main Flask Application
├── wsgi.py              # WSGI entry point for Gunicorn
├── requirements.txt     # Dependencies
├── Dockerfile           # Container image definition
├── docker-compose.yml   # Container run configuration
├── .dockerignore        # Files excluded from the image build context
├── .env                 # Environment Variables (not committed)
└── README.md            # This File
```

---

## 🎯 Running in Production

Use **Gunicorn** for better performance:

```sh
gunicorn wsgi:app --bind 0.0.0.0:6000
```

---

## 📝 License

This project is open-source. Feel free to modify and use it as needed!

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit changes (`git commit -m "Add new feature"`)
4. Push to GitHub (`git push origin feature-branch`)
5. Open a Pull Request 🚀

---

## 📧 Contact

For any issues or questions, please open an **issue** on GitHub.
