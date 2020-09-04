set -e
cd /opt/code/
celery beat -A celery_worker.celery --loglevel=info