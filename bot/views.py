# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from models import *
from bot_config import *  # import token, confirmation_token and over constants from bot_config.py
from bot_utils import vkbot, keyboard, button
import random, requests, datetime, time
import json  # vk is library from VK

times = dict(
    old_region_time=[datetime.time(11), datetime.time(15), datetime.time(19)],
    new_region_time=[datetime.time(11), datetime.time(15), datetime.time(21)],
    center_region_time=[datetime.time(12), datetime.time(17)],
    PTF_region_time=[datetime.time(11), datetime.time(15), datetime.time(19)],
    shtanigurt_region_time=[datetime.time(12), datetime.time(17)]
)
allowed_days = dict(
    old_region_time=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    new_region_time=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    center_region_time=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    PTF_region_time=['Tue', 'Thu'],
    shtanigurt_region_time=['Wed']
)
time_periods = dict(
    old_region_time=['8:00-11:00', '12:00-15:00', '17:00-19:00'],
    new_region_time=['8:00-11:00', '12:00-15:00', '18:00-21:00'],
    center_region_time=['10:00-12:00', '15:00-17:00'],
    PTF_region_time=['8:00-11:00', '12:00-15:00', '17:00-19:00'],
    shtanigurt_region_time=['10:00-12:00', '15:00-17:00']
)

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

vk_bot.setlevels(17)

for i in range(17):
    @vk_bot.handle(i, 'отменить', 'отмена')
    def cansel(data):
        kbrd = keyboard()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        btn_changename = button(type='text', label='Сменить имя')
        btn_changename.set_color('secondary')
        btn_changename.collect()
        btn_changenumber = button(type='text', label='Сменить номер')
        btn_changenumber.set_color('secondary')
        btn_changenumber.collect()
        btn_makebasket = button(type='text', label='Заказ')
        btn_makebasket.set_color('positive')
        btn_makebasket.collect()
        btn_products = button(type='text', label='Товары')
        btn_products.set_color('primary')
        btn_products.collect()
        btn_call = button(type='text', label='Обратный звонок')
        btn_call.set_color('primary')
        btn_call.collect()
        kbrd.add_multi_buttons(btn_makebasket, btn_products, btn_call)
        kbrd.add_multi_buttons(btn_changename, btn_changenumber, btn_cansel)
        return '=)', 0, kbrd.collect()


@vk_bot.handle(0)
def hi(data):
    user_id = data['object']['message']['from_id']
    kbrd = keyboard()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_changename = button(type='text', label='Сменить имя')
    btn_changename.set_color('secondary')
    btn_changename.collect()
    btn_changenumber = button(type='text', label='Сменить номер')
    btn_changenumber.set_color('secondary')
    btn_changenumber.collect()
    btn_makebasket = button(type='text', label='Заказ')
    btn_makebasket.set_color('positive')
    btn_makebasket.collect()
    btn_products = button(type='text', label='Товары')
    btn_products.set_color('primary')
    btn_products.collect()
    btn_call = button(type='text', label='Обратный звонок')
    btn_call.set_color('primary')
    btn_call.collect()
    kbrd.add_multi_buttons(btn_makebasket, btn_products, btn_call)
    kbrd.add_multi_buttons(btn_changename, btn_changenumber, btn_cansel)
    try:
        user = User.objects.get(user_id=int(user_id))
        name = user.name
    except:
        try:
            params = {'user_ids': str(user_id), 'access_token': token, 'v': '5.130'}
            user_info = requests.get('https://api.vk.com/method/users.get', params=params)
            user_info = json.loads(user_info.text)['response'][0]
            name = user_info['first_name'] + ' ' + user_info['last_name']
            user = User(user_id=int(user_id), name=name)
            user.save()
        except:
            user = User(user_id=int(user_id))
            user.save()
            return 'Здравствуйте уважаемый клиент! Рады приветствовать вас! Здесь Вы можете сделать заказ воды. Заказывайте и наслаждайтесь качественной и безопасной водой!', 0, kbrd.collect()
    return 'Здравствуйте {}! Рады приветствовать вас! Здесь Вы можете сделать заказ воды. Заказывайте и наслаждайтесь качественной и безопасной водой!'.format(
        name), 0, kbrd.collect()

@vk_bot.handle(0, 'статус')
def check_status(data):
    kbrd = keyboard()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    kbrd.add_wide_button(btn_cansel)
    return 'Напишите номер заказа, статус которого вы хотите посмотреть', 16, kbrd.collect()

@vk_bot.handle(0, 'сменить имя')
def change_name(data):
    user_id = data['object']['message']['from_id']
    try:
        user = User.objects.get(user_id=int(user_id))
    except:
        try:
            params = {'user_ids': str(user_id), 'access_token': token, 'v': '5.130'}
            user_info = requests.get('https://api.vk.com/method/users.get', params=params)
            user_info = json.loads(user_info.text)['response'][0]
            name = user_info['first_name'] + ' ' + user_info['last_name']
            user = User(user_id=int(user_id), name=name)
            user.save()
        except:
            user = User(user_id=int(user_id))
            user.save()
    kbrd = keyboard()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_back = button(type='text', label='Назад')
    btn_back.set_color('secondary')
    btn_back.collect()
    kbrd.add_multi_buttons(btn_back, btn_cansel)
    return 'Укажите пожалуйста, как к вам можно обращаться)', 1, kbrd.collect()


@vk_bot.handle(0, 'товары')
def show_products(data):
    user_id = data['object']['message']['from_id']
    try:
        user = User.objects.get(user_id=int(user_id))
    except:
        try:
            params = {'user_ids': str(user_id), 'access_token': token, 'v': '5.130'}
            user_info = requests.get('https://api.vk.com/method/users.get', params=params)
            user_info = json.loads(user_info.text)['response'][0]
            name = user_info['first_name'] + ' ' + user_info['last_name']
            user = User(user_id=int(user_id), name=name)
            user.save()
        except:
            user = User(user_id=int(user_id))
            user.save()
    kbrd = keyboard()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_changename = button(type='text', label='Сменить имя')
    btn_changename.set_color('secondary')
    btn_changename.collect()
    btn_changenumber = button(type='text', label='Сменить номер')
    btn_changenumber.set_color('secondary')
    btn_changenumber.collect()
    btn_makebasket = button(type='text', label='Заказ')
    btn_makebasket.set_color('positive')
    btn_makebasket.collect()
    btn_products = button(type='text', label='Товары')
    btn_products.set_color('primary')
    btn_products.collect()
    btn_call = button(type='text', label='Обратный звонок')
    btn_call.set_color('primary')
    btn_call.collect()
    kbrd.add_multi_buttons(btn_makebasket, btn_products, btn_call)
    kbrd.add_multi_buttons(btn_changename, btn_changenumber, btn_cansel)
    return 'Вода:\nСветлая 5л/18.9л\nСветлая здоровье 5л/18.9л', 0, kbrd.collect()


@vk_bot.handle(0, 'заказ', 'сделать заказ', 'заказать')
def make_basket(data):
    user_id = data['object']['message']['from_id']
    try:
        user = User.objects.get(user_id=int(user_id))
    except:
        try:
            params = {'user_ids': str(user_id), 'access_token': token, 'v': '5.130'}
            user_info = requests.get('https://api.vk.com/method/users.get', params=params)
            user_info = json.loads(user_info.text)['response'][0]
            name = user_info['first_name'] + ' ' + user_info['last_name']
            user = User(user_id=int(user_id), name=name)
            user.save()
        except:
            user = User(user_id=int(user_id))
            user.save()
    kbrd = keyboard()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_back = button(type='text', label='Назад')
    btn_back.set_color('secondary')
    btn_back.collect()
    btn_first_order = button(type='text', label='Заказываю впервые')
    btn_first_order.set_color('primary')
    btn_first_order.collect()
    btn_contract_id = button(type='text', label='По номеру договора')
    btn_contract_id.set_color('primary')
    btn_contract_id.collect()
    btn_adress = button(type='text', label='По адресу')
    btn_adress.set_color('primary')
    btn_adress.collect()
    kbrd.add_multi_buttons(btn_contract_id, btn_adress, btn_first_order)
    kbrd.add_multi_buttons(btn_back, btn_cansel)
    return 'Выберите подходящий для вас вариант заказа.', 3, kbrd.collect()


@vk_bot.handle(0, 'обратный звонок')
def call_back(data):
    user_id = data['object']['message']['from_id']
    try:
        user = User.objects.get(user_id=int(user_id))
        phone_number = str(user.phone_number)
        if phone_number.isdigit() and (len(phone_number) == 11) and (phone_number[0] == '8'):
            kbrd = keyboard()
            btn_cansel = button(type='text', label='Отмена')
            btn_cansel.set_color('negative')
            btn_cansel.collect()
            btn_changename = button(type='text', label='Сменить имя')
            btn_changename.set_color('secondary')
            btn_changename.collect()
            btn_changenumber = button(type='text', label='Сменить номер')
            btn_changenumber.set_color('secondary')
            btn_changenumber.collect()
            btn_makebasket = button(type='text', label='Заказ')
            btn_makebasket.set_color('positive')
            btn_makebasket.collect()
            btn_products = button(type='text', label='Товары')
            btn_products.set_color('primary')
            btn_products.collect()
            btn_call = button(type='text', label='Обратный звонок')
            btn_call.set_color('primary')
            btn_call.collect()
            kbrd.add_multi_buttons(btn_makebasket, btn_products, btn_call)
            kbrd.add_multi_buttons(btn_changename, btn_changenumber, btn_cansel)
            try:
                call = Callback.objects.get(user_id=int(user_id))
                if call.phone_number == phone_number:
                    return 'Мы уже добавили вас в очередь, мы обязательно вам позвоним)', 0, kbrd.collect()
                else:
                    return 'Мы добавили вас в очередь, мы обязательно вам позвоним)', 0, kbrd.collect()
            except:
                call = Callback(user_id=user_id, name=user.name, phone_number=phone_number)
                call.save()
            return 'Мы добавили вас в очередь, наши специалисты вам скоро позвонят)', 0, kbrd.collect()
        else:
            kbrd = keyboard()
            btn_back = button(type='text', label='Назад')
            btn_back.set_color('secondary')
            btn_back.collect()
            kbrd.add_wide_button(btn_back)
            return 'Похоже, что у вас неправильно указан номер телефона, укажите его правильно пожалуйста', 2, kbrd.collect()
    except Exception:
        try:
            params = {'user_ids': str(user_id), 'access_token': token, 'v': '5.130'}
            user_info = requests.get('https://api.vk.com/method/users.get', params=params)
            user_info = json.loads(user_info.text)['response'][0]
            name = user_info['first_name'] + ' ' + user_info['last_name']
            user = User(user_id=int(user_id), name=name)
            user.save()
        except:
            user = User(user_id=int(user_id))
            user.save()
        kbrd = keyboard()
        btn_back = button(type='text', label='Назад')
        btn_back.set_color('secondary')
        btn_back.collect()
        kbrd.add_wide_button(btn_back)
        return 'Похоже что у вас не указан номер мобильного телефона, укажите его пожалуйста', 2, kbrd.collect()


@vk_bot.handle(0, 'сменить номер')
def change_number(data):
    user_id = data['object']['message']['from_id']
    try:
        user = User.objects.get(user_id=int(user_id))
    except:
        try:
            params = {'user_ids': str(user_id), 'access_token': token, 'v': '5.130'}
            user_info = requests.get('https://api.vk.com/method/users.get', params=params)
            user_info = json.loads(user_info.text)['response'][0]
            name = user_info['first_name'] + ' ' + user_info['last_name']
            user = User(user_id=int(user_id), name=name)
            user.save()
        except:
            user = User(user_id=int(user_id))
            user.save()
    kbrd = keyboard()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_back = button(type='text', label='Назад')
    btn_back.set_color('secondary')
    btn_back.collect()
    kbrd.add_multi_buttons(btn_back, btn_cansel)
    return 'Укажите пожалуйста новый номер', 2, kbrd.collect()


@vk_bot.handle(1)
def save_name(data):
    name = data['object']['message']['text']
    user_id = data['object']['message']['from_id']
    try:
        user = User.objects.get(user_id=int(user_id))
        user.name = name
        user.save()
        kbrd = keyboard()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        btn_changename = button(type='text', label='Сменить имя')
        btn_changename.set_color('secondary')
        btn_changename.collect()
        btn_changenumber = button(type='text', label='Сменить номер')
        btn_changenumber.set_color('secondary')
        btn_changenumber.collect()
        btn_makebasket = button(type='text', label='Заказ')
        btn_makebasket.set_color('positive')
        btn_makebasket.collect()
        btn_products = button(type='text', label='Товары')
        btn_products.set_color('primary')
        btn_products.collect()
        btn_call = button(type='text', label='Обратный звонок')
        btn_call.set_color('primary')
        btn_call.collect()
        kbrd.add_multi_buttons(btn_makebasket, btn_products, btn_call)
        kbrd.add_multi_buttons(btn_changename, btn_changenumber, btn_cansel)
        return 'Хорошо, {}'.format(name), 0, kbrd.collect()
    except:
        kbrd = keyboard()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        kbrd.add_wide_button(btn_cansel)
        return 'Ты как сюда попал? Авторизируйся пожалуйста)', 0, kbrd.collect()


@vk_bot.handle(1, 'назад')
def one_back(data):
    kbrd = keyboard()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_changename = button(type='text', label='Сменить имя')
    btn_changename.set_color('secondary')
    btn_changename.collect()
    btn_changenumber = button(type='text', label='Сменить номер')
    btn_changenumber.set_color('secondary')
    btn_changenumber.collect()
    btn_makebasket = button(type='text', label='Заказ')
    btn_makebasket.set_color('positive')
    btn_makebasket.collect()
    btn_products = button(type='text', label='Товары')
    btn_products.set_color('primary')
    btn_products.collect()
    btn_call = button(type='text', label='Обратный звонок')
    btn_call.set_color('primary')
    btn_call.collect()
    kbrd.add_multi_buttons(btn_makebasket, btn_products, btn_call)
    kbrd.add_multi_buttons(btn_changename, btn_changenumber, btn_cansel)
    return '<--', 0, kbrd.collect()


@vk_bot.handle(2)
def save_phone_number(data):
    phone_number = data['object']['message']['text']
    user_id = data['object']['message']['from_id']
    try:
        user = User.objects.get(user_id=int(user_id))
        if phone_number.isdigit() and (len(phone_number) == 11) and (phone_number[0] == '8'):
            user.phone_number = phone_number
            user.save()
            kbrd = keyboard()
            btn_cansel = button(type='text', label='Отмена')
            btn_cansel.set_color('negative')
            btn_cansel.collect()
            btn_changename = button(type='text', label='Сменить имя')
            btn_changename.set_color('secondary')
            btn_changename.collect()
            btn_changenumber = button(type='text', label='Сменить номер')
            btn_changenumber.set_color('secondary')
            btn_changenumber.collect()
            btn_makebasket = button(type='text', label='Заказ')
            btn_makebasket.set_color('positive')
            btn_makebasket.collect()
            btn_products = button(type='text', label='Товары')
            btn_products.set_color('primary')
            btn_products.collect()
            btn_call = button(type='text', label='Обратный звонок')
            btn_call.set_color('primary')
            btn_call.collect()
            kbrd.add_multi_buttons(btn_makebasket, btn_products, btn_call)
            kbrd.add_multi_buttons(btn_changename, btn_changenumber, btn_cansel)
            return 'Хорошо, теперь ваш номер {}'.format(phone_number), 0, kbrd.collect()
        else:
            return 'Похоже вы неправильно ввели номер, попробуйте снова)', 2
    except:
        kbrd = keyboard()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        kbrd.add_wide_button(btn_cansel)
        return 'Ты как сюда попал? Авторизируйся пожалуйста)', 0, kbrd.collect()


@vk_bot.handle(2, 'назад')
def two_back(data):
    kbrd = keyboard()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_changename = button(type='text', label='Сменить имя')
    btn_changename.set_color('secondary')
    btn_changename.collect()
    btn_changenumber = button(type='text', label='Сменить номер')
    btn_changenumber.set_color('secondary')
    btn_changenumber.collect()
    btn_makebasket = button(type='text', label='Заказ')
    btn_makebasket.set_color('positive')
    btn_makebasket.collect()
    btn_products = button(type='text', label='Товары')
    btn_products.set_color('primary')
    btn_products.collect()
    btn_call = button(type='text', label='Обратный звонок')
    btn_call.set_color('primary')
    btn_call.collect()
    kbrd.add_multi_buttons(btn_makebasket, btn_products, btn_call)
    kbrd.add_multi_buttons(btn_changename, btn_changenumber, btn_cansel)
    return '<--', 0, kbrd.collect()


@vk_bot.handle(3, 'назад')
def three_back(data):
    kbrd = keyboard()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_changename = button(type='text', label='Сменить имя')
    btn_changename.set_color('secondary')
    btn_changename.collect()
    btn_changenumber = button(type='text', label='Сменить номер')
    btn_changenumber.set_color('secondary')
    btn_changenumber.collect()
    btn_makebasket = button(type='text', label='Заказ')
    btn_makebasket.set_color('positive')
    btn_makebasket.collect()
    btn_products = button(type='text', label='Товары')
    btn_products.set_color('primary')
    btn_products.collect()
    btn_call = button(type='text', label='Обратный звонок')
    btn_call.set_color('primary')
    btn_call.collect()
    kbrd.add_multi_buttons(btn_makebasket, btn_products, btn_call)
    kbrd.add_multi_buttons(btn_changename, btn_changenumber, btn_cansel)
    return '<--', 0, kbrd.collect()


@vk_bot.handle(3, 'заказываю впервые')
def first_order(data):
    user_id = data['object']['message']['from_id']
    user = User.objects.get(user_id=int(user_id))
    if user.adress != '':
        basket = Basket(user_id=int(user_id), first_time='true')
        basket.save()
        kbrd = keyboard(inline=True)
        btn_old = button(type='text', label='Старый')
        btn_old.collect()
        btn_new = button(type='text', label='Новый')
        btn_new.collect()
        btn_center = button(type='text', label='Центральный')
        btn_center.collect()
        btn_PTF = button(type='text', label='ПТФ')
        btn_PTF.collect()
        btn_shtanigurt = button(type='text', label='Штанигурт')
        btn_shtanigurt.collect()
        kbrd.add_multi_buttons(btn_old, btn_new, btn_center)
        kbrd.add_multi_buttons(btn_PTF, btn_shtanigurt)
        return 'Выберите свой район из присутствующих:', 6, kbrd.collect()
    else:
        basket = Basket(user_id=int(user_id), first_time='true')
        basket.save()
        kbrd = keyboard()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        btn_back = button(type='text', label='Назад')
        btn_back.set_color('secondary')
        btn_back.collect()
        kbrd.add_multi_buttons(btn_back, btn_cansel)
        return 'Укажите точный адрес, куда курьер привезет Вам воду: название улицы - номер дома - номер квартиры - этаж', 5, kbrd.collect()


@vk_bot.handle(3, 'по номеру договора')
def by_contract_id(data):
    user_id = data['object']['message']['from_id']
    user = User.objects.get(user_id=int(user_id))
    basket = Basket(user_id=int(user_id))
    basket.save()
    if (user.contract_id != -1) and (user.adress != ''):
        kbrd = keyboard(inline=True)
        btn_old = button(type='text', label='Старый')
        btn_old.collect()
        btn_new = button(type='text', label='Новый')
        btn_new.collect()
        btn_center = button(type='text', label='Центральный')
        btn_center.collect()
        btn_PTF = button(type='text', label='ПТФ')
        btn_PTF.collect()
        btn_shtanigurt = button(type='text', label='Штанигурт')
        btn_shtanigurt.collect()
        kbrd.add_multi_buttons(btn_old, btn_new, btn_center)
        kbrd.add_multi_buttons(btn_PTF, btn_shtanigurt)
        return 'Выберите свой район из присутствующих:', 6, kbrd.collect()
    elif (user.contract_id != -1) and (user.adress == ''):
        kbrd = keyboard()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        btn_back = button(type='text', label='Назад')
        btn_back.set_color('secondary')
        btn_back.collect()
        kbrd.add_multi_buttons(btn_back, btn_cansel)
        return 'Укажите точный адрес, куда курьер привезет Вам воду: название улицы - номер дома - номер квартиры - этаж', 5, kbrd.collect()
    else:
        kbrd = keyboard()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        btn_back = button(type='text', label='Назад')
        btn_back.set_color('secondary')
        btn_back.collect()
        kbrd.add_multi_buttons(btn_back, btn_cansel)
        return 'Укажите номер вашего договора: ~формат неизвестен~`', 4, kbrd.collect()


@vk_bot.handle(3, 'по адресу')
def by_adress(data):
    user_id = data['object']['message']['from_id']
    user = User.objects.get(user_id=int(user_id))
    if user.adress != '':
        kbrd = keyboard(inline=True)
        btn_old = button(type='text', label='Старый')
        btn_old.collect()
        btn_new = button(type='text', label='Новый')
        btn_new.collect()
        btn_center = button(type='text', label='Центральный')
        btn_center.collect()
        btn_PTF = button(type='text', label='ПТФ')
        btn_PTF.collect()
        btn_shtanigurt = button(type='text', label='Штанигурт')
        btn_shtanigurt.collect()
        kbrd.add_multi_buttons(btn_old, btn_new, btn_center)
        kbrd.add_multi_buttons(btn_PTF, btn_shtanigurt)
        return 'Выберите свой район из присутствующих:', 6, kbrd.collect()
    else:
        basket = Basket(user_id=int(user_id))
        basket.save()
        kbrd = keyboard()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        btn_back = button(type='text', label='Назад')
        btn_back.set_color('secondary')
        btn_back.collect()
        kbrd.add_multi_buttons(btn_back, btn_cansel)
        return 'Укажите точный адрес, куда курьер привезет Вам воду: название улицы - номер дома - номер квартиры - этаж', 5, kbrd.collect()


@vk_bot.handle(3)
def three_default(data):
    kbrd = keyboard()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_back = button(type='text', label='Назад')
    btn_back.set_color('secondary')
    btn_back.collect()
    btn_first_order = button(type='text', label='Заказываю впервые')
    btn_first_order.set_color('primary')
    btn_first_order.collect()
    btn_contract_id = button(type='text', label='По номеру договора')
    btn_contract_id.set_color('primary')
    btn_contract_id.collect()
    btn_adress = button(type='text', label='По адресу')
    btn_adress.set_color('primary')
    btn_adress.collect()
    kbrd.add_multi_buttons(btn_contract_id, btn_adress, btn_first_order)
    kbrd.add_multi_buttons(btn_back, btn_cansel)
    return 'Выберите подходящий для вас вариант заказа.', 3, kbrd.collect()


@vk_bot.handle(4)
def save_contract_id(data):
    user_id = data['object']['message']['from_id']
    contract_id = data['object']['message']['text']
    if contract_id.isdigit() and len(contract_id) <= 10:
        user = User.objects.get(user_id=int(user_id))
        user.contract_id = int(contract_id)
        user.save()
        if user.adress != '':
            kbrd = keyboard(inline=True)
            btn_old = button(type='text', label='Старый')
            btn_old.collect()
            btn_new = button(type='text', label='Новый')
            btn_new.collect()
            btn_center = button(type='text', label='Центральный')
            btn_center.collect()
            btn_PTF = button(type='text', label='ПТФ')
            btn_PTF.collect()
            btn_shtanigurt = button(type='text', label='Штанигурт')
            btn_shtanigurt.collect()
            kbrd.add_multi_buttons(btn_old, btn_new, btn_center)
            kbrd.add_multi_buttons(btn_PTF, btn_shtanigurt)
            return 'Выберите свой район из присутствующих:', 6, kbrd.collect()
        else:
            kbrd = keyboard()
            btn_cansel = button(type='text', label='Отмена')
            btn_cansel.set_color('negative')
            btn_cansel.collect()
            btn_back = button(type='text', label='Назад')
            btn_back.set_color('secondary')
            btn_back.collect()
            kbrd.add_multi_buttons(btn_back, btn_cansel)
            return 'Укажите точный адрес, куда курьер привезет Вам воду: название улицы - номер дома - номер квартиры - этаж', 5, kbrd.collect()
    else:
        kbrd = keyboard()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        btn_back = button(type='text', label='Назад')
        btn_back.set_color('secondary')
        btn_back.collect()
        kbrd.add_multi_buttons(btn_back, btn_cansel)
        return 'Номер вашего договора невалиден, введите еще раз)`', 4, kbrd.collect()


@vk_bot.handle(4, 'назад')
def four_back(data):
    kbrd = keyboard()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_back = button(type='text', label='Назад')
    btn_back.set_color('secondary')
    btn_back.collect()
    btn_first_order = button(type='text', label='Заказываю впервые')
    btn_first_order.set_color('primary')
    btn_first_order.collect()
    btn_contract_id = button(type='text', label='По номеру договора')
    btn_contract_id.set_color('primary')
    btn_contract_id.collect()
    btn_adress = button(type='text', label='По адресу')
    btn_adress.set_color('primary')
    btn_adress.collect()
    kbrd.add_multi_buttons(btn_contract_id, btn_adress, btn_first_order)
    kbrd.add_multi_buttons(btn_back, btn_cansel)
    return 'Выберите подходящий для вас вариант заказа.', 3, kbrd.collect()


@vk_bot.handle(5, 'назад')
def five_back(data):
    kbrd = keyboard()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_back = button(type='text', label='Назад')
    btn_back.set_color('secondary')
    btn_back.collect()
    btn_first_order = button(type='text', label='Заказываю впервые')
    btn_first_order.set_color('primary')
    btn_first_order.collect()
    btn_contract_id = button(type='text', label='По номеру договора')
    btn_contract_id.set_color('primary')
    btn_contract_id.collect()
    btn_adress = button(type='text', label='По адресу')
    btn_adress.set_color('primary')
    btn_adress.collect()
    kbrd.add_multi_buttons(btn_contract_id, btn_adress, btn_first_order)
    kbrd.add_multi_buttons(btn_back, btn_cansel)
    return 'Выберите подходящий для вас вариант заказа.', 3, kbrd.collect()


@vk_bot.handle(5)
def save_adress(data):
    # название улицы - номер дома - номер квартиры - этаж
    message = data['object']['message']['text']
    user_id = data['object']['message']['from_id']
    try:
        street, house, flat, floor = message.split(' - ')
        if (not street.isdigit()) and house.isdigit() and flat.isdigit() and floor.isdigit():
            user = User.objects.get(user_id=int(user_id))
            user.adress = 'Улица - {0}, номер дома - {1}, номер квартиры - {2}, этаж - {3},'.format(street, house, flat,
                                                                                                    floor)
            user.save()
            kbrd = keyboard(inline=True)
            btn_old = button(type='text', label='Старый')
            btn_old.collect()
            btn_new = button(type='text', label='Новый')
            btn_new.collect()
            btn_center = button(type='text', label='Центральный')
            btn_center.collect()
            btn_PTF = button(type='text', label='ПТФ')
            btn_PTF.collect()
            btn_shtanigurt = button(type='text', label='Штанигурт')
            btn_shtanigurt.collect()
            kbrd.add_multi_buttons(btn_old, btn_new, btn_center)
            kbrd.add_multi_buttons(btn_PTF, btn_shtanigurt)
            return 'Выберите свой район из присутствующих:', 6, kbrd.collect()
        else:
            kbrd = keyboard()
            btn_cansel = button(type='text', label='Отмена')
            btn_cansel.set_color('negative')
            btn_cansel.collect()
            btn_back = button(type='text', label='Назад')
            btn_back.set_color('secondary')
            btn_back.collect()
            kbrd.add_multi_buttons(btn_back, btn_cansel)
            return 'Ваш адрес невалиден, введите его в формате: название улицы - номер дома - номер квартиры - этаж (обратите внимание: пишите через пробел тире пробел)', 5, kbrd.collect()
    except:
        kbrd = keyboard()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        btn_back = button(type='text', label='Назад')
        btn_back.set_color('secondary')
        btn_back.collect()
        kbrd.add_multi_buttons(btn_back, btn_cansel)
        return 'Ваш адрес невалиден, введите его в формате: название улицы - номер дома - номер квартиры - этаж (обратите внимание: пишите через пробел тире пробел)', 5, kbrd.collect()


@vk_bot.handle(6, 'новый', 'старый', 'центральный', 'птф', 'штанигурт')
def add_region(data):
    user_id = data['object']['message']['from_id']
    message = data['object']['message']['text']
    user = User.objects.get(user_id=int(user_id))
    if 'Район' not in user.adress:
        user.adress = user.adress + ' Район - {}'.format(message.lower())
        user.save()
    else:
        index = user.adress.index(' Район')
        user.adress = user.adress[:index] + ' Район - {}'.format(message.lower())
        user.save()
    kbrd = keyboard(inline=True)
    btn_bright = button(type='text', label='Светлая')
    btn_bright.collect()
    btn_bright_healthy = button(type='text', label='Светлая здоровье')
    btn_bright_healthy.collect()
    kbrd.add_multi_buttons(btn_bright, btn_bright_healthy)
    return 'Выберите воду из предложенных:', 7, kbrd.collect()


@vk_bot.handle(6, 'назад')
def six_back(data):
    kbrd = keyboard()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_back = button(type='text', label='Назад')
    btn_back.set_color('secondary')
    btn_back.collect()
    kbrd.add_multi_buttons(btn_back, btn_cansel)
    return 'Укажите точный адрес, куда курьер привезет Вам воду: название улицы - номер дома - номер квартиры - этаж', 5, kbrd.collect()


@vk_bot.handle(6)
def six_default(data):
    kbrd = keyboard(inline=True)
    btn_old = button(type='text', label='Старый')
    btn_old.collect()
    btn_new = button(type='text', label='Новый')
    btn_new.collect()
    btn_center = button(type='text', label='Центральный')
    btn_center.collect()
    btn_PTF = button(type='text', label='ПТФ')
    btn_PTF.collect()
    btn_shtanigurt = button(type='text', label='Штанигурт')
    btn_shtanigurt.collect()
    kbrd.add_multi_buttons(btn_old, btn_new, btn_center)
    kbrd.add_multi_buttons(btn_PTF, btn_shtanigurt)
    return 'Выберите свой район из присутствующих:', 6, kbrd.collect()


@vk_bot.handle(7, 'светлая', 'светлая здоровье')
def add_lot(data):
    user_id = data['object']['message']['from_id']
    message = data['object']['message']['text']
    basket = Basket.objects.get(user_id=int(user_id))
    basket.products = message
    basket.save()
    kbrd = keyboard(inline=True)
    btn_little_bottle = button(type='text', label='5л')
    btn_little_bottle.collect()
    btn_big_bottle = button(type='text', label='18.9л')
    btn_big_bottle.collect()
    kbrd.add_multi_buttons(btn_little_bottle, btn_big_bottle)
    return 'Выберите объем из предложенных:', 8, kbrd.collect()


@vk_bot.handle(7, 'назад')
def seven_back(data):
    user_id = data['object']['message']['from_id']
    user = User.objects.get(user_id=int(user_id))
    index = user.adress.index(' Район')
    user.adress = user.adress[:index]
    user.save()
    kbrd = keyboard(inline=True)
    btn_old = button(type='text', label='Старый')
    btn_old.collect()
    btn_new = button(type='text', label='Новый')
    btn_new.collect()
    btn_center = button(type='text', label='Центральный')
    btn_center.collect()
    btn_PTF = button(type='text', label='ПТФ')
    btn_PTF.collect()
    btn_shtanigurt = button(type='text', label='Штанигурт')
    btn_shtanigurt.collect()
    kbrd.add_multi_buttons(btn_old, btn_new, btn_center)
    kbrd.add_multi_buttons(btn_PTF, btn_shtanigurt)
    return 'Выберите свой район из присутствующих:', 6, kbrd.collect()


@vk_bot.handle(7)
def seven_default(data):
    kbrd = keyboard(inline=True)
    btn_bright = button(type='text', label='Светлая')
    btn_bright.collect()
    btn_bright_healthy = button(type='text', label='Светлая здоровье')
    btn_bright_healthy.collect()
    kbrd.add_multi_buttons(btn_bright, btn_bright_healthy)
    return 'Выберите воду из предложенных:', 7, kbrd.collect()


@vk_bot.handle(8, '5л', '18.9л')
def add_size(data):
    user_id = data['object']['message']['from_id']
    message = data['object']['message']['text']
    basket = Basket.objects.get(user_id=int(user_id))
    basket.products = basket.products + 'x{}'.format(message)
    basket.save()
    kbrd = keyboard()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_back = button(type='text', label='Назад')
    btn_back.set_color('secondary')
    btn_back.collect()
    kbrd.add_multi_buttons(btn_back, btn_cansel)
    return 'Какое колличество бутылок вы хотите?:', 9, kbrd.collect()


@vk_bot.handle(8, 'назад')
def eight_back(data):
    kbrd = keyboard(inline=True)
    btn_bright = button(type='text', label='Светлая')
    btn_bright.collect()
    btn_bright_healthy = button(type='text', label='Светлая здоровье')
    btn_bright_healthy.collect()
    kbrd.add_multi_buttons(btn_bright, btn_bright_healthy)
    return 'Выберите воду из предложенных:', 7, kbrd.collect()


@vk_bot.handle(8)
def eight_default(data):
    kbrd = keyboard(inline=True)
    btn_little_bottle = button(type='text', label='5л')
    btn_little_bottle.collect()
    btn_big_bottle = button(type='text', label='18.9л')
    btn_big_bottle.collect()
    kbrd.add_multi_buttons(btn_little_bottle, btn_big_bottle)
    return 'Выберите объем из предложенных:', 8, kbrd.collect()


@vk_bot.handle(9)
def add_water_number(data):
    user_id = data['object']['message']['from_id']
    message = str(data['object']['message']['text'])
    if message.isdigit():
        basket = Basket.objects.get(user_id=int(user_id))
        basket.products = basket.products + 'x{}'.format(message)
        basket.save()
        kbrd = keyboard(inline=True)
        btn_cash = button(type='text', label='Наличные')
        btn_cash.collect()
        btn_card = button(type='text', label='Картой')
        btn_card.collect()
        btn_ticket = button(type='text', label='По счету для юр лиц')
        btn_ticket.collect()
        kbrd.add_multi_buttons(btn_cash, btn_card)
        kbrd.add_wide_button(btn_ticket)
        return 'Выберите форму оплаты из нижеперечисленных:', 10, kbrd.collect()
    else:
        kbrd = keyboard()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        btn_back = button(type='text', label='Назад')
        btn_back.set_color('secondary')
        btn_back.collect()
        kbrd.add_multi_buttons(btn_back, btn_cansel)
        return 'Какое колличество бутылок вы хотите?', 9, kbrd.collect()


@vk_bot.handle(9, 'назад')
def nine_back(data):
    user_id = data['object']['message']['from_id']
    basket = Basket.objects.get(user_id=int(user_id))
    index = basket.products.index('x')
    basket.products = basket.products[:index]
    basket.save()
    kbrd = keyboard(inline=True)
    btn_little_bottle = button(type='text', label='5л')
    btn_little_bottle.collect()
    btn_big_bottle = button(type='text', label='18.9л')
    btn_big_bottle.collect()
    kbrd.add_multi_buttons(btn_little_bottle, btn_big_bottle)
    return 'Выберите объем из предложенных:', 8, kbrd.collect()


@vk_bot.handle(10, 'наличные', 'картой', 'по счету для юр лиц')
def save_pay(data):
    try:
        user_id = data['object']['message']['from_id']
        message = data['object']['message']['text']
        user = User.objects.get(user_id=int(user_id))
        basket = Basket.objects.get(user_id=int(user_id))
        basket.pay_type = message
        basket.save()
        region = user.adress.split(', ')[-1].split(' - ')[-1]
        now = datetime.datetime.now()
        today = time.ctime(time.time())[:3]
        if region == 'старый':
            region_time = times['old_region_time']
            day_allowed = allowed_days['old_region_time']
            if ((region_time[-1].hour - now.hour) < 4) and (today in day_allowed):
                today_allow = True
            else:
                today_allow = False
        elif region == 'новый':
            region_time = times['new_region_time']
            day_allowed = allowed_days['new_region_time']
            if ((region_time[-1].hour - now.hour) < 4) and (today in day_allowed):
                today_allow = True
            else:
                today_allow = False
        elif region == 'центральный':
            region_time = times['center_region_time']
            day_allowed = allowed_days['center_region_time']
            if ((region_time[-1].hour - now.hour) < 4) and (today in day_allowed):
                today_allow = True
            else:
                today_allow = False
        elif region == 'птф':
            region_time = times['PTF_region_time']
            day_allowed = allowed_days['PTF_region_time']
            if ((region_time[-1].hour - now.hour) < 4) and (today in day_allowed):
                today_allow = True
            else:
                today_allow = False
        elif region == 'штанигурт':
            region_time = times['shtanigurt_region_time']
            day_allowed = allowed_days['shtanigurt_region_time']
            if ((region_time[-1].hour - now.hour) < 4) and (today in day_allowed):
                today_allow = True
            else:
                today_allow = False
        else:
            return 'Кажется где то ты повернул не туда, ты не должен быть тут, пройди цикл заново пожалуйста)', 0
        kbrd = keyboard(inline=True)
        if today_allow:
            btn_today = button(type='text', label='Сегодня')
            btn_today.collect()
            kbrd.add_wide_button(btn_today)

        if len(day_allowed) < 4:
            btns = []
            for i in range(1, 30):
                day_time = time.time() + (i * 86400)
                day = time.ctime(day_time)
                if day[:3] in day_allowed:
                    btn_day = button(type='text', label=day[4:10])
                    btn_day.collect()
                    btns.append(btn_day)
                if len(btns) == 3:
                    kbrd.add_multi_buttons(*btns)
                    btns = []
            if len(btns) > 1:
                kbrd.add_multi_buttons(*btns)
            elif len(btns) == 1:
                kbrd.add_wide_button(btns[0])
            return 'Выберите дату:', 11, kbrd.collect()
        else:
            btns = []
            for i in range(1, 10):
                day_time = time.time() + (i * 86400)
                day = time.ctime(day_time)
                btn_day = button(type='text', label=day[4:10])
                btn_day.collect()
                btns.append(btn_day)
                if len(btns) == 3:
                    kbrd.add_multi_buttons(*btns)
                    btns = []
            if len(btns) > 1:
                kbrd.add_multi_buttons(*btns)
            elif len(btns) == 1:
                kbrd.add_wide_button(btns[0])
            return 'Выберите дату:', 11, kbrd.collect()
    except Exception as err:
        return err.message + 'error 10', 10


@vk_bot.handle(10)
def ten_default(data):
    kbrd = keyboard(inline=True)
    btn_cash = button(type='text', label='Наличные')
    btn_cash.collect()
    btn_card = button(type='text', label='Картой')
    btn_card.collect()
    btn_ticket = button(type='text', label='По счету для юр лиц')
    btn_ticket.collect()
    kbrd.add_multi_buttons(btn_cash, btn_card)
    kbrd.add_wide_button(btn_ticket)
    return 'Выберите форму оплаты из нижеперечисленных:', 10, kbrd.collect()


@vk_bot.handle(10, 'назад')
def ten_back(data):
    user_id = data['object']['message']['from_id']
    basket = Basket.objects.get(user_id=int(user_id))
    index1 = basket.products.index('x')
    index = basket.products.index('x', index1 + 1)
    basket.products = basket.products[:index]
    basket.save()
    kbrd = keyboard()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_back = button(type='text', label='Назад')
    btn_back.set_color('secondary')
    btn_back.collect()
    kbrd.add_multi_buttons(btn_back, btn_cansel)
    return 'Какое колличество бутылок вы хотите?', 9, kbrd.collect()

@vk_bot.handle(11)
def choose_date(data):
    user_id = data['object']['message']['from_id']
    message = data['object']['message']['text']
    user = User.objects.get(user_id=int(user_id))
    region = user.adress.split(', ')[-1].split(' - ')[-1]
    basket = Basket.objects.get(user_id=int(user_id))
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    try:
        month, day = message.split()
        if (month in months) and day.isdigit() and (int(day) > 0) and (int(day) < 31):
            basket.delivery_time = month + ' ' + day
            basket.save()
            today = datetime.date.today()
            delivery_date = datetime.date(today.year, months.index(month) + 1, int(day))
            if region == 'старый':
                region_time = times['old_region_time']
                region_time_period = time_periods['old_region_time']
            elif region == 'новый':
                region_time = times['new_region_time']
                region_time_period = time_periods['new_region_time']
            elif region == 'центральный':
                region_time = times['center_region_time']
                region_time_period = time_periods['center_region_time']
            elif region == 'птф':
                region_time = times['PTF_region_time']
                region_time_period = time_periods['PTF_region_time']
            elif region == 'штанигурт':
                region_time = times['shtanigurt_region_time']
                region_time_period = time_periods['shtanigurt_region_time']
            else:
                return 'Что-то пошло не так, попробуй еще раз пожалуйста)', 0
            if (delivery_date - today).days == 0:
                now = datetime.datetime.now()
                kbrd = keyboard(inline=True)
                for index in range(len(region_time)):
                    if (region_time[index].hour - now.hour) > 4:
                        for periond in region_time_period[index:]:
                            btn_time = button(type='text', label=periond)
                            btn_time.collect()
                            kbrd.add_wide_button(btn_time)
                        return 'Выберите время доставки на сегодня:', 12, kbrd.collect()
            else:
                kbrd = keyboard(inline=True)
                for periond in region_time_period:
                    btn_time = button(type='text', label=periond)
                    btn_time.collect()
                    kbrd.add_wide_button(btn_time)
                return 'Выберите время доставки:', 12, kbrd.collect()
        else:
            kbrd = keyboard()
            btn_cansel = button(type='text', label='Отмена')
            btn_cansel.set_color('negative')
            btn_cansel.collect()
            btn_back = button(type='text', label='Назад')
            btn_back.set_color('secondary')
            btn_back.collect()
            kbrd.add_multi_buttons(btn_back, btn_cansel)
            return 'Вы не выбрали время, попробуйте еще раз', 11, kbrd.collect()
    except:
        kbrd = keyboard()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        btn_back = button(type='text', label='Назад')
        btn_back.set_color('secondary')
        btn_back.collect()
        kbrd.add_multi_buttons(btn_back, btn_cansel)
        return 'Вы не выбрали время, попробуйте еще раз', 11, kbrd.collect()

@vk_bot.handle(11, 'назад')
def eleven_back(data):
    kbrd = keyboard(inline=True)
    btn_cash = button(type='text', label='Наличные')
    btn_cash.collect()
    btn_card = button(type='text', label='Картой')
    btn_card.collect()
    btn_ticket = button(type='text', label='По счету для юр лиц')
    btn_ticket.collect()
    kbrd.add_multi_buttons(btn_cash, btn_card)
    kbrd.add_wide_button(btn_ticket)
    return 'Выберите форму оплаты из нижеперечисленных:', 10, kbrd.collect()

@vk_bot.handle(12)
def choose_time(data):
    user_id = data['object']['message']['from_id']
    message = data['object']['message']['text']
    basket = Basket.objects.get(user_id=int(user_id))
    if len(message) > 12:
        kbrd = keyboard()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        btn_back = button(type='text', label='Назад')
        btn_back.set_color('secondary')
        btn_back.collect()
        kbrd.add_multi_buttons(btn_back, btn_cansel)
        return 'Вы не указали время', 12, kbrd.collect()
    else:
        basket.delivery_time = basket.delivery_time + ' ' + message
        basket.save()
        kbrd = keyboard()
        btn_yes = button(type='text', label='Да')
        btn_yes.set_color('positive')
        btn_yes.collect()
        btn_no = button(type='text', label='Нет')
        btn_no.set_color('negative')
        btn_no.collect()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        btn_back = button(type='text', label='Назад')
        btn_back.set_color('secondary')
        btn_back.collect()
        kbrd.add_multi_buttons(btn_yes, btn_no)
        kbrd.add_multi_buttons(btn_back, btn_cansel)
        return 'Связаться с вами при выполнении заказа?', 13, kbrd.collect()

@vk_bot.handle(12, 'назад')
def twelve_back(data):
    kbrd = keyboard(inline=True)
    btn_cash = button(type='text', label='Наличные')
    btn_cash.collect()
    btn_card = button(type='text', label='Картой')
    btn_card.collect()
    btn_ticket = button(type='text', label='По счету для юр лиц')
    btn_ticket.collect()
    kbrd.add_multi_buttons(btn_cash, btn_card)
    kbrd.add_wide_button(btn_ticket)
    return 'Выберите форму оплаты из нижеперечисленных:', 10, kbrd.collect()

@vk_bot.handle(13, 'да')
def add_need_callback(data):
    user_id = data['object']['message']['from_id']
    basket = Basket.objects.get(user_id=int(user_id))
    basket.comment = 'Нужен обратный звонок '
    basket.save()
    kbrd = keyboard()
    btn_pass = button(type='text', label='Пропустить')
    btn_pass.set_color('secondary')
    btn_pass.collect()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_back = button(type='text', label='Назад')
    btn_back.set_color('secondary')
    btn_back.collect()
    kbrd.add_wide_button(btn_pass)
    kbrd.add_multi_buttons(btn_back, btn_cansel)
    return 'Если хотите, можете добавить комментарий к заказу. Если подъездная дверь имеет домофон это следует указать здесь.', 14, kbrd.collect()

@vk_bot.handle(13, 'нет')
def add_notneed_callback(data):
    kbrd = keyboard()
    btn_pass = button(type='text', label='Пропустить')
    btn_pass.set_color('secondary')
    btn_pass.collect()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_back = button(type='text', label='Назад')
    btn_back.set_color('secondary')
    btn_back.collect()
    kbrd.add_wide_button(btn_pass)
    kbrd.add_multi_buttons(btn_back, btn_cansel)
    return 'Если хотите, можете добавить комментарий к заказу. Если подъездная дверь имеет домофон это следует указать здесь.', 14, kbrd.collect()

@vk_bot.handle(13, 'назад')
def thirteen_back(data):
    kbrd = keyboard(inline=True)
    btn_cash = button(type='text', label='Наличные')
    btn_cash.collect()
    btn_card = button(type='text', label='Картой')
    btn_card.collect()
    btn_ticket = button(type='text', label='По счету для юр лиц')
    btn_ticket.collect()
    kbrd.add_multi_buttons(btn_cash, btn_card)
    kbrd.add_wide_button(btn_ticket)
    return 'Выберите форму оплаты из нижеперечисленных:', 10, kbrd.collect()

@vk_bot.handle(13)
def thirteen_default(data):
    kbrd = keyboard()
    btn_yes = button(type='text', label='Да')
    btn_yes.set_color('positive')
    btn_yes.collect()
    btn_no = button(type='text', label='Нет')
    btn_no.set_color('negative')
    btn_no.collect()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_back = button(type='text', label='Назад')
    btn_back.set_color('secondary')
    btn_back.collect()
    kbrd.add_multi_buttons(btn_yes, btn_no)
    kbrd.add_multi_buttons(btn_back, btn_cansel)
    return 'Связаться с вами при выполнении заказа?', 13, kbrd.collect()

@vk_bot.handle(14, 'назад')
def fourteen_back(data):
    kbrd = keyboard()
    btn_yes = button(type='text', label='Да')
    btn_yes.set_color('positive')
    btn_yes.collect()
    btn_no = button(type='text', label='Нет')
    btn_no.set_color('negative')
    btn_no.collect()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_back = button(type='text', label='Назад')
    btn_back.set_color('secondary')
    btn_back.collect()
    kbrd.add_multi_buttons(btn_yes, btn_no)
    kbrd.add_multi_buttons(btn_back, btn_cansel)
    return 'Связаться с вами при выполнении заказа?', 13, kbrd.collect()

@vk_bot.handle(14, 'пропустить')
def no_comment(data):
    user_id = data['object']['message']['from_id']
    user = User.objects.get(user_id=int(user_id))
    basket = Basket.objects.get(user_id=int(user_id))
    adress = user.adress.split(', ')
    street = adress[0].split(' - ')[-1]
    house = adress[1].split(' - ')[-1]
    flat = adress[2].split(' - ')[-1]
    floor = adress[3].split(' - ')[-1]
    lot, size, num = basket.products.split('x')
    pay = basket.pay_type
    delivery_time = basket.delivery_time
    comment = basket.comment
    order = 'Ваш заказ: {0} объемом {1} в количестве {2}. Адрес доставки: улица {3}, дом {4}, квартира {5}, этаж {6}. Форма оплаты: {7}. Дата доставки: {8}. Пожелания к заказу: {9}'.format(lot, size, num, street, house, flat, floor, pay, delivery_time, comment)
    kbrd = keyboard()
    btn_agree = button(type='text', label='Верно')
    btn_agree.set_color('positive')
    btn_agree.collect()
    btn_refresh = button(type = 'text', label='Заново')
    btn_refresh.set_color('negative')
    btn_refresh.collect()
    kbrd.add_multi_buttons(btn_agree, btn_refresh)
    return 'Проверьте ваш заказ перед отправкой.\n' + order, 15, kbrd.collect()

@vk_bot.handle(14)
def add_comment(data):
    user_id = data['object']['message']['from_id']
    comm = data['object']['message']['text']
    user = User.objects.get(user_id=int(user_id))
    basket = Basket.objects.get(user_id=int(user_id))
    try:
        basket.comment = basket.comment + '\n' + comm
        basket.save()
    except:
        kbrd = keyboard()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        btn_back = button(type='text', label='Назад')
        btn_back.set_color('secondary')
        btn_back.collect()
        kbrd.add_multi_buttons(btn_back, btn_cansel)
        return 'Ваш комментарий слишком велик, напишите пожалуйста короче.', 14, kbrd.collect()
    adress = user.adress.split(', ')
    street = adress[0].split(' - ')[-1]
    house = adress[1].split(' - ')[-1]
    flat = adress[2].split(' - ')[-1]
    floor = adress[3].split(' - ')[-1]
    lot, size, num = basket.products.split('x')
    pay = basket.pay_type
    delivery_time = basket.delivery_time
    comment = basket.comment
    order = 'Ваш заказ: {0} объемом {1} в количестве {2}. Адрес доставки: улица {3}, дом {4}, квартира {5}, этаж {6}. Форма оплаты: {7}. Дата доставки: {8}. Пожелания к заказу: {9}'.format(lot, size, num, street, house, flat, floor, pay, delivery_time, comment)
    kbrd = keyboard()
    btn_agree = button(type='text', label='Верно')
    btn_agree.set_color('positive')
    btn_agree.collect()
    btn_refresh = button(type = 'text', label='Заново')
    btn_refresh.set_color('negative')
    btn_refresh.collect()
    kbrd.add_multi_buttons(btn_agree, btn_refresh)
    return 'Проверьте ваш заказ перед отправкой.\n' + order, 15, kbrd.collect()

@vk_bot.handle(15, 'заново')
def refresh_all(data):
    kbrd = keyboard()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_back = button(type='text', label='Назад')
    btn_back.set_color('secondary')
    btn_back.collect()
    btn_first_order = button(type='text', label='Заказываю впервые')
    btn_first_order.set_color('primary')
    btn_first_order.collect()
    btn_contract_id = button(type='text', label='По номеру договора')
    btn_contract_id.set_color('primary')
    btn_contract_id.collect()
    btn_adress = button(type='text', label='По адресу')
    btn_adress.set_color('primary')
    btn_adress.collect()
    kbrd.add_multi_buttons(btn_contract_id, btn_adress, btn_first_order)
    kbrd.add_multi_buttons(btn_back, btn_cansel)
    return 'Выберите подходящий для вас вариант заказа.', 3, kbrd.collect()

@vk_bot.handle(15, 'верно')
def make_order_from_basket(data):
    try:
        user_id = data['object']['message']['from_id']
        user = User.objects.get(user_id=int(user_id))
        basket = Basket.objects.get(user_id=int(user_id))
        adress = user.adress
        name = user.name
        phone_number = user.phone_number
        lot, size, num = basket.products.split('x')
        num = num.strip(' ')
        pay = basket.pay_type
        delivery_time = basket.delivery_time
        comment = basket.comment
        first_time = basket.first_time
        contract_id =user.contract_id
        order_id = random.randint(1, 2147483646)
        order = Order(order_id=order_id,
                      user_id=int(user_id),
                      first_time=first_time,
                      contract_id=contract_id,
                      phone_number=phone_number,
                      name=name,
                      adress=adress,
                      product=lot,
                      size=size,
                      count=int(num),
                      pay_type=pay,
                      delivery_time=delivery_time,
                      comment=comment)
        order.save()
        return 'Ваш заказ сохранен, его номер {}, вы всегда можете посмотреть его статус, написав боту слово \'статус\''.format(str(order_id)), 0
    except Exception as err:
        return str(err) + ' ошибка сохранения', 15

@vk_bot.handle(15, 'назад')
def fiveteen_back(data):
    kbrd = keyboard()
    btn_pass = button(type='text', label='Пропустить')
    btn_pass.set_color('secondary')
    btn_pass.collect()
    btn_cansel = button(type='text', label='Отмена')
    btn_cansel.set_color('negative')
    btn_cansel.collect()
    btn_back = button(type='text', label='Назад')
    btn_back.set_color('secondary')
    btn_back.collect()
    kbrd.add_wide_button(btn_pass)
    kbrd.add_multi_buttons(btn_back, btn_cansel)
    return 'Если хотите, можете добавить комментарий к заказу. Если подъездная дверь имеет домофон это следует указать здесь.', 14, kbrd.collect()

@vk_bot.handle(16)
def find_status(data):
    message = data['object']['message']['text']
    try:
        order = Order.objects.get(order_id=int(message))
        status = order.status
        kbrd = keyboard()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        kbrd.add_wide_button(btn_cansel)
        return status, 0, kbrd.collect()
    except:
        kbrd = keyboard()
        btn_cansel = button(type='text', label='Отмена')
        btn_cansel.set_color('negative')
        btn_cansel.collect()
        kbrd.add_wide_button(btn_cansel)
        return 'Неправильно указан номер заказа, попробуйте еще раз', 16, kbrd.collect()

local_debug = False

@csrf_exempt  # exempt index() function from built-in Django protection
def bot(request):  # url: https://mybot.mysite.ru/vk_bot/
    if (request.method == "POST"):
        data = json.loads(request.body)  # take POST request from auto-generated variable <request.body> in json format
        if (data['secret'] == secret_key):  # if json request contain secret key and it's equal my secret key
            if (data['type'] == 'confirmation'):  # if VK server request confirmation
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
            if (data['type'] == 'message_new'):  # if VK server send a message
                if local_debug:
                    if data['object']['message']['from id'] != '272493558':
                        vk_bot.Debuganswer(data)
                    else:
                        try:
                            vk_bot.answer(data)
                        except Exception:
                            vk_bot.Erroranswer(data)
                else:
                    try:
                        vk_bot.answer(data)
                    except Exception:
                        vk_bot.Erroranswer(data)
                return HttpResponse('ok', content_type="text/plain", status=200)
    else:
        return HttpResponse('see you ;)')