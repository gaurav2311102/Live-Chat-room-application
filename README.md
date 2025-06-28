# 💬 Real-Time Chat Room

A production-ready real-time chat room application built with **Django**, **WebSockets (Django Channels)**, and deployed on **AWS EC2** with **Docker**, **Nginx**, **SSL**, and a custom domain `https://chatarena.xyz`.

---

## 🚀 Features

- ✅ User registration and login
- ⚡ Real-time messaging with Django Channels & WebSockets
- 🕓 Message history & deletion (`[This message was deleted]`)
- 👤 Profile picture support
- 🧠 Topics & joined rooms display
- 🌐 Custom domain with HTTPS (`https://chatarena.xyz`)
- 📦 Dockerized backend with PostgreSQL and Redis
- ☁️ Deployed on AWS EC2 with Nginx + SSL (Let's Encrypt)

---

## 🛠️ Tech Stack

- **Backend**: Django, Django Channels
- **Database**: PostgreSQL (via AWS RDS)
- **Channel Layer**: Redis
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**:
  - AWS EC2 (Ubuntu 22.04)
  - Docker & Docker Compose
  - Nginx as reverse proxy
  - Certbot for SSL (HTTPS)
  - Domain from Hostinger (`chatarena.xyz`)

---

## 📦 Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/gaurav2311102/Live-Chat-room-application.git
   cd chat-room
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure `.env`**
   Create a `.env` file in the root:
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   ```

5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start Redis (if not using Docker)**
   ```bash
   redis-server
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Visit**
   ```
   http://127.0.0.1:8000/
   ```

---

## 🚀 Production Deployment Steps (What Was Done)

### 1. ✅ EC2 Setup

- Launched **Ubuntu EC2 instance**
- Allowed inbound ports `80`, `443`, `8000`, `22`
- Installed: `docker`, `docker-compose`, `nginx`, `certbot`

### 2. 🐳 Dockerized App

- Created a `Dockerfile` for Django app
- Added `docker-compose.yml` with:
  - Django container (image from AWS ECR)
  - Redis container
- Bound Django app to `127.0.0.1:8000`

### 3. 🧠 Nginx Reverse Proxy

- Configured Nginx to:
  - Listen on port `443` for `chatarena.xyz`
  - Proxy pass to `127.0.0.1:8000`
- Config located at `/etc/nginx/sites-available/chatarena`

### 4. 🔐 SSL with Let's Encrypt

```bash
sudo certbot --nginx -d chatarena.xyz -d www.chatarena.xyz
```

### 5. 🌍 Domain Setup (Hostinger)

- Purchased `chatarena.xyz` from Hostinger
- Updated A record to point to EC2 public IP

---

## 🔗 Live Demo

👉 [https://chatarena.xyz](https://chatarena.xyz)

---

## 📌 Future Improvements

- ✅ JWT authentication
- 🔒 Rate limiting & security headers
- 📱 Mobile responsiveness
- 📤 File sharing in chats
- 🧑‍💻 Admin dashboard