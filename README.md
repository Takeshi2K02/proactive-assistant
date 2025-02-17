# Proactive Personal Assistant Chatbot

## Project Overview

This project is a proactive personal assistant chatbot with a **Flask backend** and a **React frontend**. It integrates the **Gemini API** for NLP and provides time-aware interactions, task management, and proactive engagement.

## Features

- **Basic Chatbot** (Handles user queries via Gemini API)
- **Task and To-Do Management** (Add, edit, delete tasks)
- **Proactive Messages** (Check-ins, suggestions)
- **Time Awareness** (Reminders, scheduling)
- **Web Notifications** (Future enhancement)

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: React (JavaScript)
- **Database**: SQLite/MongoDB (for storing user data)
- **Real-Time Communication**: Flask-SocketIO/WebSockets
- **External API**: Gemini API for chat responses

## Project Structure

```
proactive-assistant/
├── backend/                 # Flask backend
│   ├── app.py               # Main API handler
│   ├── config.py            # Configuration settings
│   ├── requirements.txt     # Dependencies
│   ├── routes/
│   │   ├── chat.py          # Handles chatbot interactions
│   │   ├── tasks.py         # Manages tasks and reminders
│   ├── models/
│   │   ├── database.py      # Database setup
│   ├── services/
│   │   ├── gemini_api.py    # Handles API calls to Gemini
│   ├── utils/
│   │   ├── time_helper.py   # Handles time-based functions
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/      # UI components
│   │   ├── pages/           # Main pages
│   │   │   ├── Chat.js      # Chat page for the chatbot
│   │   ├── services/        # API calls to backend
│   ├── package.json         # React dependencies
├── README.md                # Project documentation

```

## Setup & Installation

### Backend (Flask)

```sh
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend (React)

```sh
cd frontend
npm install
npm start
```