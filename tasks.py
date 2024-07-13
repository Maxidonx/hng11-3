# File: tasks.py

from celery import Celery
from mail import send_mail

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery_app = Celery('flask_app', broker='pyamqp://guest@localhost//', backend='rpc://')

@celery_app.task(name='flask_app.send_salutation_mail')
def send_mail_task(email):
    send_mail(email)

