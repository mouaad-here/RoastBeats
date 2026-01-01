#  RoastBeats

**RoastBeats** is a Django web application that uses **Google Gemini AI** to ruthlessly roast your music taste. Users can log in via Spotify to analyze their top tracks or enter their preferences manually. The app generates a snarky critique, a "Taste Score" (0-100), and a dating life assumption.

![Status](https://img.shields.io/badge/Status-Development-green)
![Stack](https://img.shields.io/badge/Stack-Django%20|%20Python%20|%20Gemini%20AI-blue)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## Features

*   **Spotify Integration:** Secure OAuth2 login to fetch User Top Artists & Tracks.
*   **Manual Mode:** "Confessional Booth" for users without Spotify.
*   **AI Engine:** Powered by **Google Gemini 2.5 Flash** for high-speed, savage roasts.
*   **Viral Share Cards**: Users can download a generated image for thier roast (via `html2canvas`) or share directly to  Socail-media using a custom-built in share modal.
*   **Production Ready:** configured with `WhiteNoise` for static files and `dj-database-url`.

## Project Structure
```bash
roastbeats/
├── core/                   # Application Logic (Views, Auth, AI)
├── templates/              # HTML Files (Base, Index, Roast)
├── static/                 # CSS, Images, JS
├── RoastBeats/             # Project Settings (settings.py)
├── .env                    # Environment Secrets
├── Dockerfile              # Container Configuration
├── entrypoint.sh           # Startup script for Docker
└── manage.py               # Django Task Runner
```
---

## Tech Stack

*   **Framework:** Django 5.2.8
*   **Language:** Python 3.12.3
*   **AI API:** Google Generative AI 
*   **Database:** SQLite (Default) / PostgreSQL (Supported via URL)
*   **Deployment Tools:** Gunicorn, WhiteNoise, Docker

---

##  Local Installation

### 1. Clone the Repository
```bash
git clone <repository_url>
cd roastbeats
```

### 2. Create Virtual Environment
```bash
# Windows / WSL
python -m venv venv
source venv/bin/activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables (.env)

Create a .env file in the root directory. Copy the structure below and fill in your keys.

Note: You need a Spotify Developer Account and a Google AI Studio Key.
```bash
# --- Core Django ---
DEBUG=True
# Generate a secret key or use a random string for dev
DJANGO_SECRET_KEY=django-insecure-change-me-for-production
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0,*

# --- Spotify API ---
# Ensure Redirect URI matches exactly what you set in Spotify Dashboard
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/callback/

# --- Google Gemini AI ---
GEMINI_API_KEY=your_gemini_api_key
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Run the Server

```bash
python manage.py runserver

# Visit http://127.0.0.1:8000 to start roasting.
```
## Running with Docker

This project is Docker-ready.

1. Build the Image

```bash
docker build -t roastbeats .
```

2. Run the Container
This command passes your .env file variables into the container.
```bash
docker run -p 8000:8000 --env-file .env roastbeats
# Visit http://localhost:8000 to start roasting.
```
The Docker container will execute the `entrypoint.sh` script to migrate the database and start Gunicorn.
### Production Settings

The settings.py file is configured to automatically switch to Production mode when you change your .env file:

* Set `DEBUG=False` in .env.

* Set a strong `DJANGO_SECRET_KEY`.

* Set `ALLOWED_HOSTS` to your domain (e.g., roastbeats.com).

* Add your domain to `CSRF_TRUSTED_ORIGINS`.

* When DEBUG is False, the app automatically:

* Enforces `SSL/HTTPS`.

* Secures Cookies `CSRF/Session`.

* Uses `WhiteNoise` to serve compressed static files efficiently.

# Licence
Distributed under the MIT License. See `LICENSE` for more information.
