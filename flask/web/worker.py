from celery import Celery, Task

# def create_celery_app(app):
#     class FlaskTask(Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 self.run(*args, **kwargs)

#     celery_app = Celery(
#             app.name, task_cls=FlaskTask,
#             broker_url="redis://localhost:6379/1",
#             result_backend="redis://localhost:6379/2",
#             broker_connection_retry_on_startup=True,
#             # timezone = "Asia/kolkata",
#             include=["web.tasks"],     
#         )
#     celery_app.set_default()
# #   celery_app.conf.update(
# #     result_serializer='json',
# #     task_serializer='json',
# #     accept_content=['json'],
# # )
# #   celery_app.control.enable_events(reply=True)
# #   app.extensions["celery"] = celery_app
#     return celery_app

def create_celery_app(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask,include=["web.tasks"])
    celery_app.config_from_object("celeryconfig")
    celery_app.set_default()
    return celery_app
