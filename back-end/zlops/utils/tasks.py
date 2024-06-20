# from __future__ import absolute_import, unicode_literals
from celery import Task
from celery import shared_task
import logging
from django.conf import settings
from django.core.mail import send_mail

# 实例化myLogger
myLogger = logging.getLogger("log")


@shared_task
def send_mail_task(*args, **kwargs):
    kwargs["subject"] = "{}:{}_{}".format(
        settings.SYS_NAME,
        settings.SYS_VERSION,
        kwargs.get("subject", "500"),
    )
    kwargs["from_email"] = kwargs.get("from_email", settings.EMAIL_HOST_USER)
    kwargs["recipient_list"] = kwargs.get("recipient_list", [settings.DEFAULT_EMAIL_RECIPIENT])
    kwargs["message"] = kwargs.get("message", None)
    kwargs["html_message"] = kwargs.get("html_message", None)
    myLogger.debug(kwargs)
    send_mail(*args, **kwargs)
    


class CustomTask(Task):
    """
    自定义的任务回调
    """

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        detail = "{0!r} failed: {1!r}".format(task_id, exc)
        myLogger.error(detail)
        send_mail_task.delay(subject="task_error", message=detail)
        return super().on_failure(exc, task_id, args, kwargs, einfo)
