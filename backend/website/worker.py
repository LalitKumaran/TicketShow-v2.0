from celery import Celery, Task

def create_celery_app(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask,include=["website.tasks"])
    celery_app.config_from_object("celeryconfig")
    celery_app.set_default()
    return celery_app
