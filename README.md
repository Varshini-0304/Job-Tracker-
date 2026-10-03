# Job Application Tracker

A full-stack web app to track job applications. Users can sign up, log in, and manage their own list of applications with status updates.

## Features

- Signup and login with hashed passwords
- Session-based authentication, with protected pages
- Add, view, update and delete job applications
- Update status (Applied, Interview, Offer, Rejected) from a dropdown
- Each user sees only their own applications

## Tech Stack

- **Frontend:** HTML, CSS
- **Backend:** Python, Flask
- **Database:** SQLite

## Run Locally

```bash
pip install flask
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## What I Learned

- How forms send data from the browser to a Flask backend (GET vs POST)
- Password hashing and session handling
- CRUD operations with SQLite using parameterized queries
- Keeping user data separate with a `user_id` on every job

## Planned Next

- AI-based job description and resume match score
- Deployment with a live link
