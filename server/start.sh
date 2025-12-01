#!/bin/bash
cd server
python -c "from app import app; from models import db; with app.app_context(): db.create_all()"
python seed.py
gunicorn app:app