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
```

`GITLAB_PRIVATE_TOKEN` needs at least **Developer** access on the project — it's used to create a merge request pipeline via GitLab's API, which requires more than a trigger token's permissions.

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

### Surviving Reboots (Auto-Start)

`docker-compose.yml` sets `restart: unless-stopped`, so once the container is started with `docker compose up -d`, it automatically comes back up whenever the Docker daemon restarts — you don't need to re-run `docker compose up -d` yourself after that.

This only kicks in once Docker itself is running, though. If Docker Desktop isn't set to launch on login, a full machine reboot leaves Docker (and this container) stopped until someone opens Docker Desktop manually. To make it fully hands-off after a reboot:

1. Open **Docker Desktop → Settings → General**.
2. Enable **"Start Docker Desktop when you log in"**.

With that enabled, a reboot brings up Docker Desktop → which brings up this container → with no manual steps.

---

## 🍎 Deploying via Colima (macOS)

On a macOS host where Docker Desktop isn't installed — e.g. a machine that already runs other projects' containers via [Colima](https://github.com/abiosoft/colima) — use the same Colima setup for this app rather than installing Docker Desktop separately.

### **1️⃣ Install Colima (if not already installed)**

```sh
brew install colima docker docker-compose
```

Skip this if Colima/Docker CLI are already set up on the host for another project.

### **2️⃣ Check if Colima Is Already Running**

Don't start a second VM if one is already up for another project — check first:

```sh
docker info >/dev/null 2>&1 && echo "Docker/Colima already running" || echo "Not running"
```

### **3️⃣ Start Colima (only if not already running)**

```sh
colima start --cpu 4 --memory 8
```

If the first attempt fails, clear stale/partial cache files and retry once:

```sh
rm -rf "$HOME/Library/Caches/colima/caches"/*.downloading
rm -rf "$HOME/Library/Caches/colima/caches"/*.tmp
colima start --cpu 4 --memory 8
```

### **4️⃣ Point Docker at the Colima Context**

```sh
docker context use colima
```

### **5️⃣ Wait Until Docker Is Ready**

```sh
for i in {1..60}; do
    if docker info >/dev/null 2>&1; then
        echo "Docker is ready"
        break
    fi
    sleep 2
done
```

### **6️⃣ Build and Start the Webhook Handler**

```sh
docker compose up -d --build
```

(Falls back to `docker-compose up -d --build` if the `compose` plugin isn't available.)

### **7️⃣ Recovery (if `docker compose up -d` fails)**

If the container fails to start even with Colima reporting healthy, recreate the VM and retry once:

```sh
colima delete -f
colima start --cpu 4 --memory 8
docker context use colima
# re-run the "wait until ready" loop from step 5, then:
docker compose up -d --build
```

### Notes

- Colima is shared infrastructure on the host — don't stop or delete it without checking whether other projects' containers (e.g. the static site deployments) depend on it too.
- This app doesn't need its own Colima VM or Docker context; it runs as just another container on the existing one, isolated by its own compose project/network as described above.

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
