from celery import Celery
from scedule_manager import tasks
from celery.schedules import crontab


app = Celery('scedule_manager', broker='redis://')
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(60.0, tasks.save_tweets.s(), name='updates every minute')

    # sender.add_periodic_task(30.0, tasks.save_tweets.s(), expires=10)
    #
    # # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=10, minute=0, day_of_week=4),
    #     tasks.save_tweets.s(),
    # )