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
.
├── README.md
├── instance
├── requirements.txt
├── server
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── config.cpython-312.pyc
│   │   ├── models.cpython-312.pyc
│   │   └── validators.cpython-312.pyc
│   ├── app.py
│   ├── config.py
│   ├── migrations
│   │   ├── README
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── b8ae682a16a2_master_initialization_of_all_tables_and_.py
│   ├── models.py
│   ├── requirements.txt
│   ├── routes
│   │   ├── __pycache__
│   │   │   ├── analytics.cpython-312.pyc
│   │   │   ├── auth.cpython-312.pyc
│   │   │   ├── exercises.cpython-312.pyc
│   │   │   ├── metrics.cpython-312.pyc
│   │   │   ├── profile.cpython-312.pyc
│   │   │   └── workouts.cpython-312.pyc
│   │   ├── analytics.py
│   │   ├── auth.py
│   │   ├── exercises.py
│   │   ├── metrics.py
│   │   ├── profile.py
│   │   └── workouts.py
│   ├── seed.py
│   ├── start.sh
│   └── validators.py
└── venv
    ├── bin
    │   ├── Activate.ps1
    │   ├── activate
    │   ├── activate.csh
    │   ├── activate.fish
    │   ├── alembic
    │   ├── dotenv
    │   ├── flask
    │   ├── mako-render
    │   ├── pip
    │   ├── pip3
    │   ├── pip3.12
    │   ├── python -> python3
    │   ├── python3 -> /usr/bin/python3
    │   └── python3.12 -> python3
    ├── include
    │   └── site
    │       └── python3.12
    ├── lib
    │   └── python3.12
    │       └── site-packages
    ├── lib64 -> lib
    └── pyvenv.cfg

---

##  Setup Instructions

### 1. Clone the Repository

1. Fork & git clone <your-repo-url>
2. cd Backend-Fit-track-app
3. Create & Activate Virtual Environment
4. python3 -m venv venv
5. source venv/bin/activate   

### 2. Install Requirements

- pip install -r requirements.txt

### 3. Database Setup

Initialize migrations (first time only)
bash
- Copy code
- cd server
- flask db init

### 4. Generate migration file

- flask db migrate -m "initial tables"
- Apply migrations
- flask db upgrade
- Seed the database
- python seed.py

5. ### Running the Server
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
- George Mukoshi
- Dancan Odhiambo
- David Kinuthia
- Praxedes Kabeya
