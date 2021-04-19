# -*- coding: utf-8 -*-

import requests, json
import sys, random
import logging
from models import User_level
from django.db import models

if __name__ == '__main__':
    log = logging.getLogger()
    logging.basicConfig(filename='bot.log',filemode='a', level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
    log.addHandler(logging.StreamHandler(sys.stderr))

else:
    log = logging.getLogger(__name__)

class keyboard():

    def __init__(self, **kwargs):
        '''
        :param str one_time: is this keyboard for one time using (true) or not (false), default: false
        :param str inline: is this keyboard inline (true) or not (false), default: false
        '''

        if 'one_time' in kwargs:
            self.__one_time = kwargs['one_time']

            if type(self.__one_time) != bool:
                logging.warning('Param one_time must be boolean type')
                quit()

        else:
            self.__one_time = True

        if 'inline' in kwargs:
            self.__inline = kwargs['inline']

            if type(self.__inline) != bool:
                logging.warning('Param inline must be boolean type')
                quit()

        else:
            self.__inline = False

        self.__buttons = []
        self.keybrd = {}

    def add_wide_button(self, btn):
        '''
        :param button btn: all types of button allowed
        :return:
        '''
        self.__buttons.append([btn.butt])

    def add_multi_buttons(self, *args):
        '''
        :param button args: only text and callback buttons allowed
        :return:
        '''
        if len(args) > 4:
            logging.warning('Max len of multi button is 4')
            quit()

        btns = []

        for btn in args:
            btns.append(btn.butt)

        self.__buttons.append(btns)

    def collect(self):
        '''
        :return dict: collected keyboard
        '''
        if self.__inline == False:
            self.keybrd = {'one_time': self.__one_time, 'buttons': self.__buttons}
            return self.keybrd
        else:
            self.keybrd = {'buttons': self.__buttons, 'inline': self.__inline}
            return self.keybrd



class button():
    def __init__(self, **kwargs):
        '''
        :param unicode type: location/callback/text
        :param unicode payload: answer from vk server if user push this button
        :param unicode labal: text inside button (user will send this text if button is pushed
        '''
        if kwargs == None:
            logging.warning('Button cant be initialised without **kwargs')
            quit()
        try:
            self.__type = kwargs['type']
        except KeyError:
            logging.warning('No type buttons initialisation!')
            quit()
        self.butt = {}
        self.__color = ''
        if self.__type == 'location':
            try:
                self.__action = {'type': self.__type, 'payload': kwargs['payload']}
            except KeyError as err:
                if err.message != 'type':
                    try:
                        self.__action = {'type': self.__type}
                    except KeyError as err1:
                        logging.warning('Missing {}, {} keys in button init'.format(err.message, err1.message))
                        quit()
                    logging.warning('Missing {} key in button init'.format(err.message))
                else:
                    logging.warning('Missing {} key in button init'.format(err.message))
                    quit()

        elif self.__type == 'callback':
            try:
                self.__action = {'type': self.__type, 'label': kwargs['label'], 'payload': kwargs['payload']}
            except KeyError as err:
                if err.message != 'type' and err.message != 'label':
                    try:
                        self.__action = {'type': self.__type, 'label': kwargs['label']}
                    except KeyError as err1:
                        logging.warning('Missing {}, {} keys in button init'.format(err.message, err1.message))
                        quit()
                    logging.warning('Missing {} key in button init'.format(err.message))
                else:
                    logging.warning('Missing {} key in button init'.format(err.message))
                    quit()

        elif self.__type == 'text':
            try:
                self.__action = {'type': self.__type, 'label': kwargs['label'], 'payload': kwargs['payload']}
            except KeyError as err:
                if err.message != 'type' and err.message != 'label':
                    try:
                        self.__action = {'type': self.__type, 'label': kwargs['label']}
                    except KeyError as err1:
                        logging.warning('Missing {}, {} keys in button init'.format(err.message, err1.message))
                        quit()
                    logging.warning('Missing {} key in button init'.format(err.message))
                else:
                    logging.warning('Missing {} key in button init'.format(err.message))
                    quit()

        else:
            logging.warning('Unknown type {}'.format(self.__type))
            quit()

    def set_color(self, color):
        '''
        :param unicode color: primary(blue) / secondary(white) / negative(red) / positive(green)
        :return:
        '''
        if self.__type != 'location':
            self.__color = color
        else:
            logging.warning('Location button cannot have color')
            quit()

    def collect(self):
        if self.__color != '':
            self.butt = {'action': self.__action, 'color': self.__color}
        else:
            self.butt = {'action': self.__action}

class handling_messages():
    def __init__(self, levels):
        '''
        :param int levels:
        '''
        self.__levels = levels
        self.__steps = {}
        for level in range(levels):
            self.__steps[str(level)] = {'handling_messages': [], 'funcs': []}

    def handler(self, lvl, func, *messages):
        '''
        :param int lvl:
        :param function func:
        :param unicode messages:
        :return:
        '''
        if messages:
            self.__steps[str(lvl)]['handling_messages'].append([])
            for message in messages:
                self.__steps[str(lvl)]['handling_messages'][-1].append(message)
            self.__steps[str(lvl)]['funcs'].append(func)
        else:
            self.__steps[str(lvl)]['default_func'] = func

    def find_message(self, lvl, message):
        try:
            for mess in range(len(self.__steps[str(lvl)]['handling_messages'])):
                if message.lower() in self.__steps[str(lvl)]['handling_messages'][mess]:
                    return self.__steps[str(lvl)]['funcs'][mess]
            else:
                try:
                    return self.__steps[str(lvl)]['default_func']
                except KeyError as err:
                    logging.warning('No {0} in {1} level in handling_messages'.format(err.message, str(lvl)))
        except IndexError:
            logging.warning('There is no {} level in handler'.format(str(lvl)))
            def Errorfunc():
                return 'Sorry we\'ve got some problems', 0
            return Errorfunc

class vkbot():
    def __init__(self, token):
        '''
        :param str token: bot token
        '''
        self.__token = token
        self.__url = 'https://api.vk.com/method/'
        self.__handling_messages = handling_messages(0)

    def handle(self, level, *messages):
        '''
        :rtype: function
        :param int level: what level this function is
        :param messages:  what messages to handle
        :return: None, adds func to handler
        '''
        def wrapper(func):
            def wrapped():
                self.__handling_messages.handler(level, func, *messages)
            return wrapped()
        return wrapper

    def setlevels(self, level):
        '''
        :param int level: adds new level of handling messages
        :return: None
        '''
        del self.__handling_messages
        self.__handling_messages = handling_messages(level)

    def find_func(self, level, message):
        '''
        :param int level: level of user at witch step of order hi is
        :param str message: what message sent user
        :return function: func that will answer to user
        '''
        return self.__handling_messages.find_message(lvl=level, message=message)

    def answer(self, data):
        '''
        :param data: json request from vk.com
        :return: None, only sends answer to vk.com
        '''
        method = 'messages.send'
        user_id = data['object']['message']['from_id']
        try:
            user = User_level.objects.get(user_id=int(user_id))
            level = user.level
        except:
            user = User_level(user_id=int(user_id), level=0)
            level = 0
            user.save()
        func = self.find_func(level=level, message=data['object']['message']['text'])
        try:
            message, newlevel, keyboard = func(data)
            random_id = random.randint(1, 9223372036854775807)
            kbrd = json.dumps(keyboard)
            dataanswer = {'user_id': str(user_id),
                    'random_id': str(random_id),
                    'message': message,
                    'keyboard': kbrd,
                    'access_token': self.__token,
                    'v': '5.130'}
            req = requests.get(self.__url + method, params=dataanswer)
            user.level = newlevel
            user.save()
        except:
            message, newlevel = func(data)
            random_id = random.randint(1, 9223372036854775807)
            dataanswer = {'user_id': str(user_id),
                    'random_id': str(random_id),
                    'message': message,
                    'access_token': self.__token,
                    'v': '5.130'}
            requests.get(self.__url + method, params=dataanswer)
            user.level = newlevel
            user.save()

    def Erroranswer(self, data):
        method = 'messages.send'
        user_id = data['object']['message']['from_id']
        random_id = random.randint(1, 9223372036854775807)
        message = 'Sorry we have some problems on server'
        dataanswer = {'user_id': str(user_id),
                'random_id': str(random_id),
                'message': message,
                'access_token': self.__token,
                'v': '5.130'}
        requests.get(self.__url + method, params=dataanswer)