web: python API/manage.py runserver 0.0.0.0:$PORT
worker: celery -A API.AcheiUnB worker --loglevel=info
beat: celery -A API.AcheiUnB beat --loglevel=info