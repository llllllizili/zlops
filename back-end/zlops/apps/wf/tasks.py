# Create your tasks here
import time
import importlib
import logging
import traceback
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from zlops import config
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from apps.system.models import User
from apps.wf.models import State, Ticket, TicketFlow, Transition
from apps.wf.serializers import TicketDetailSerializer
from utils.tasks import send_mail_task, CustomTask

# from __future__ import absolute_import, unicode_literals

myLogger = logging.getLogger("log")

# @shared_task(base=CustomTask)
# def ticket_push(ticketId, userId):
#     ticket = Ticket.objects.get(id=ticketId)
#     channel_layer = get_channel_layer()
#     data = {
#         "type": "ticket",
#         "ticket": TicketDetailSerializer(instance=ticket).data,
#         "msg": "",
#     }
#     async_to_sync(channel_layer.group_send)(f"user_{userId}", data)

@shared_task(base=CustomTask)
def run_task(ticket_id: str, retry_num=1):
    ticket = Ticket.objects.get(id=ticket_id)
    transition_obj = Transition.objects.filter(
        source_state=ticket.state, is_deleted=False
    ).first()
    script_result = True
    script_result_msg = ""
    script_str = ticket.participant
    # try:
    #     module, func = script_str.rsplit(".", 1)
    #     m = importlib.import_module(module)
    #     f = getattr(m, func)
    #     f(ticket)
    # except Exception:
    #     retry_num_new = retry_num - 1
    #     err_detail = traceback.format_exc()
    #     myLogger.error("工作流脚本执行失败", exc_info=True)
    #     script_result = False
    #     script_result_msg = err_detail
    #     if retry_num_new >= 0:
    #         time.sleep(10)
    #         run_task.delay(ticket_id, retry_num_new)
    #         return
    #     send_mail_task.delay(
    #         subject="wf_task_error",
    #         message=str(err_detail),
    #         recipient_list=[config.SYSTEM_MANAGER_EMAIL],
    #     )  # run_task执行失败发送邮件
    ticket = Ticket.objects.filter(id=ticket_id).first()
    if not script_result:
        ticket.script_run_last_result = False
        ticket.save()
    # 记录日志
    participant_cc = ticket.participant
    
    from apps.wf.services import WfService

    TicketFlow.objects.create(
        ticket=ticket,
        state=ticket.state,
        participant_cc = participant_cc,
        ticket_data=WfService.get_ticket_all_field_value(ticket),
        participant_type=State.PARTICIPANT_TYPE_ROBOT,
        participant_str="func:{}".format(script_str),
        transition=transition_obj,
        suggestion="自动化处理:{}".format(script_result_msg),
    )
    # 自动流转
    if script_result and transition_obj:
        WfService.handle_ticket(
            ticket=ticket,
            transition=transition_obj,
            new_ticket_data=ticket.ticket_data,
            by_task=True,
        )
