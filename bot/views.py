# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from bot_config import * # import token, confirmation_token and over constants from bot_config.py
from bot_utils import vkbot, keyboard, button
import random, requests
import json# vk is library from VK

"""
Using VK Callback API version 5.130
For more ditalies visit https://vk.com/dev/callback_api
"""

"""
From Django documentation (https://docs.djangoproject.com/en/1.11/ref/request-response/)
When a page is requested, Django automatically creates an HttpRequest object that contains
metadata about the request. Then Django loads the appropriate view, passing the
HttpRequest as the first argument to the view function.
This argiment is <request> in def index(request):

Decorator <@csrf_exempt> marks a view as being exempt from the protection
ensured by the Django middleware.
For cross site request protection will be used secret key from VK
"""

vk_bot = vkbot(token)

vk_bot.setlevels(1)
@vk_bot.handle(0, ('Начать',))
def start():
    kbrd = keyboard()
    btn_order = button(type='text', payload='order', label='Заказать')
    btn_order.set_color('secondary')
    kbrd.add_wide_button(btn_order)
    return 'Приветствую тебя! Я бот-доставщик воды в Глазове) Если хочешь заказать жми кнопку Заказ либо пиши мне слово Заказ)', 0, kbrd.collect()

@vk_bot.handle(0)
def zero_default():
    kbrd = keyboard()
    btn_order = button(type='text', payload='order', label='Заказать')
    btn_order.set_color('secondary')
    kbrd.add_wide_button(btn_order)
    return 'Приветствую тебя! Я бот-доставщик воды в Глазове) Если хочешь заказать жми кнопку Заказ либо пиши мне слово Заказ)', 0, kbrd.collect()


@csrf_exempt #exempt index() function from built-in Django protection
def bot(request): #url: https://mybot.mysite.ru/vk_bot/
    if (request.method == "POST"):
        data = json.loads(request.body)# take POST request from auto-generated variable <request.body> in json format
        if (data['secret'] == secret_key):# if json request contain secret key and it's equal my secret key
            if (data['type'] == 'confirmation'):# if VK server request confirmation
                """
                For confirmation my server (webhook) it must return
                confirmation token, whitch issuing in administration web-panel
                your public group in vk.com.

                Using <content_type="text/plain"> in HttpResponse function allows you
                response only plain text, without any format symbols.
                Parametr <status=200> response to VK server as VK want.
                """
                # confirmation_token from bot_config.py
                return HttpResponse(confirmation_token, content_type="text/plain", status=200)
            if (data['type'] == 'message_new'):# if VK server send a message
                vk_bot.answer(data)
                return HttpResponse('ok', content_type="text/plain", status=200)
    else:
        return HttpResponse('see you ;)')