import json

from celery.utils.log import get_task_logger

from photoalbum.celery import app

from .models import UpdateHistory, User

logger = get_task_logger(__name__)


@app.task(bind=True)
def log_update_history_task(self, user_id, data_to_log):
    logger.info(f"TASK run with user={user_id}")
    try:
        user = User.objects.filter(id=user_id).first()
        UpdateHistory.objects.create(user=user, update_values=data_to_log)
    except Exception as e:
        logger.error(e)
