@Pracky ✨️🫶 / @David Moringa 

kindly access backend repo and assist update backend repo.Just noticed am 7 commits behind and i might mess.

#  FitTrack API

A lightweight Fitness Tracking REST API built featuring JWT Authentication, Workout Logging, Profile Management, Analytics, and Exercises catalog.

---

##  Features
- User Authentication using 
- CRUD Workouts & Exercises  
- Personal Profile endpoints  
- Workout Analytics & Statistics  
- Database migrations 
- CORS enabled for frontend integration

---

##  Project Structure

Backend-Fit-track-app/
│
├── README.md
├── requirements.txt
├── server/
│ ├── app.py
│ ├── config.py
│ ├── models.py
│ ├── seed.py
│ ├── validators.py
│ ├── migrations/
│ │ └── versions/
│ └── routes/
│ ├── auth.py
│ ├── exercises.py
│ ├── workouts.py
│ ├── profile.py
│ └── analytics.py
└── venv/

---

##  Setup Instructions

### 1. Clone the Repository
1. git clone <your-repo-url>
2. cd Backend-Fit-track-app
3. Create & Activate Virtual Environment

Copy code

python3 -m venv venv
source venv/bin/activate     # Linux/Mac

2. Install Requirements

- pip install -r requirements.txt

3. Database Setup

Initialize migrations (first time only)
bash
- Copy code
- cd server
- flask db init

Generate migration file

- flask db migrate -m "initial tables"
- Apply migrations
- flask db upgrade
- Seed the database
- python seed.py

## Running the Server
From inside /server directory:
- python app.py

The API will run at:

http://127.0.0.1:5555 -Locally 
https://fittrack-0v68.onrender.com/ -Live link

## 🔑 Authentication

Auth uses JWT tokens via PyJWT.

Login returns:
json
Copy code
{
  "access_token": "<jwt-token>"
}
Pass this in headers for all protected routes:

---

## License

- MIT

## Authors

### Group 4
- Praxedes Kabeya
- Dancan Odhiambo
- David Kinuthia
- George Mukoshi
