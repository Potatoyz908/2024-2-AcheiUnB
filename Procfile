web: python API/manage.py runserver 0.0.0.0:$PORT
worker: celery -A API.AcheiUnB worker --loglevel=info
beat: celery -A API.AcheiUnB beat --loglevel=info
celeryworker: celery -A API.AcheiUnB worker & celery -A API.AcheiUnB beat -1 INFO & wait -n