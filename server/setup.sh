cd server

echo "Applying migrations..."
flask db upgrade

echo "Seeding database..."
python seed.py

echo "Starting Gunicorn server..."
exec gunicorn app:app