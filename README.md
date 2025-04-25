# 💬 Real-Time Chat Room

A real-time chat room application built with Django and WebSockets. This project allows users to send and receive messages instantly without refreshing the page.

## 🚀 Features

- User registration and login
- Real-time messaging using WebSockets (Django Channels)
- Message history
- Message deletion with `[This message was deleted]` indicator
- Deployed on Render 

## 🛠️ Tech Stack

- Django
- Django Channels
- Redis (as a Channel layer backend)
- HTML, CSS, JavaScript
- PostgreSQL
- Render (Deployment)

## 📦 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/chat-room.git
   cd chat-room
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure `.env` for secrets**
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start Redis server**  
   (Make sure Redis is installed or you're using Memurai on Windows)

7. **Run the server**
   ```bash
   python manage.py runserver
   ```

8. **Visit**
   ```
   http://127.0.0.1:8000/
   ```


