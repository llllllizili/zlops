#!/usr/bin python
# -*- encoding: utf-8 -*-
"""
@File    :    consumers.py
@Time    :   2024/06/14 23:40:30
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class SystemConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groups = set()

    async def connect(self):
        user_id = self.scope["user"].id
        username = self.scope["user"].username

        self.room_group_name = f"user_{user_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        self.groups.add(self.room_group_name)  # 添加到集合中
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "remind",
                "msg": "你好," + username,
                "from": "系统",
            },
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        for group in self.groups:
            await self.channel_layer.group_discard(group, self.channel_name)
        self.groups.clear()  # 清空集合
    async def receive(self, text_data):
        username = self.scope["user"].username
        user_id = self.scope["user"].id

        if text_data:
            content = json.loads(text_data)
            if content["type"] == "event":
                await self.channel_layer.group_add("event", self.channel_name)
                await self.send(
                text_data=json.dumps(
                    {"type": "event", "msg": "故障," + username, "from": "故障消息"}
                )
            )
        else:
            await self.send(
                text_data=json.dumps(
                    {"type": "remind", "msg": "你好," + username, "from": "系统提示"}
                )
            )

    async def remind(self, content):
        await self.send(json.dumps(content, ensure_ascii=False))

    async def event(self, content):
        await self.send(json.dumps(content, ensure_ascii=False))

    async def ticket(self, content):
        await self.send(json.dumps(content, ensure_ascii=False))
