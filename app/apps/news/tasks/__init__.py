from celery.signals import worker_ready

from .fetch_google_trends import SyncGoogleTrends
from .fetch_ua_news import SyncUANews


@worker_ready.connect
def run_periodic_tasks_on_start(sender, **kwargs):
    with sender.app.connection() as conn:
        sender.app.send_task("sync_google_trends", connection=conn)
        sender.app.send_task("sync_112ua_news", connection=conn)
