from __future__ import unicode_literals

from django.db import models

class User_level(models.Model):
    '''
    :param int user_id: User id from received message
    :param int level: Level of user order
    :param date: Not stable
    '''
    user_id = models.IntegerField(primary_key=True, null=False, unique=True, help_text='Saves persons user_id')
    level = models.SmallIntegerField(null=False, help_text='Saves at witch level(step) of the order user is')
    date = models.DateTimeField(auto_now=True, help_text='Saves time of last message from this user')

    def __unicode__(self):
        return self.user_id

class Basket(models.Model):
    user_id = models.IntegerField(primary_key=True, null=False, help_text='Saves persons user_id')
    products = models.CharField(null=False, default='', max_length=100, help_text='Day and time when buyer will receive his order')
    date = models.DateTimeField(auto_now_add=True, help_text='Saves time of last message from this user')
    first_time = models.CharField(null=False, default='false', max_length=6, help_text='Is this order first persons order or not')
    pay_type = models.CharField(null=False, default=' ', max_length=30, help_text='Saves payment type, cash or card or ticket')
    delivery_time = models.CharField(null=False, default='', max_length=50, help_text='Saves date and time to delivery')
    comment = models.CharField(null=False, default=' ', max_length=200, help_text='Comment to the order')

    def __unicode__(self):
        return self.user_id

class User(models.Model):
    user_id = models.IntegerField(primary_key=True, null=False, help_text='Saves persons user_id')
    name = models.CharField(null=False, default='', max_length=100, help_text='Persons firstname and lastname')
    phone_number = models.CharField(null=False, default='', max_length=11, help_text='Saves persons phone number')
    adress = models.CharField(null=False, default='', max_length=200, help_text='Persons adress')
    contract_id = models.IntegerField(null=False, default=-1, help_text='Persons contract id')

    def __unicode__(self):
        return self.user_id

class Callback(models.Model):
    user_id = models.IntegerField(primary_key=True, null=False, help_text='Saves persons user_id')
    name = models.CharField(null=False, default='', max_length=100, help_text='Persons firstname and lastname')
    phone_number = models.CharField(null=False, default = '', max_length=11, help_text='Saves persons phone number')

    def __unicode__(self):
        return self.user_id

class Order(models.Model):
    order_id = models.IntegerField(primary_key=True, null=False, unique=True, help_text='Saves order unique id')
    user_id = models.IntegerField(null=False, help_text='Saves persons user_id')
    first_time = models.CharField(null=False, default='false', max_length=6,
                                  help_text='Is this order first persons order or not')
    contract_id = models.IntegerField(null=False, default=-1, help_text='Persons contract id')
    name = models.CharField(null=False, default='', max_length=100, help_text='Persons firstname and lastname')
    phone_number = models.CharField(null=False, default='', max_length=11, help_text='Saves persons phone number')
    adress = models.CharField(null=False, default='', max_length=200, help_text='Persons adress')
    product = models.CharField(null=False, default='', max_length=30,
                                help_text='Day and time when buyer will receive his order')
    size = models.CharField(null=False, default='', max_length=7,
                                help_text='Product size')
    count = models.IntegerField(null=False, default=-1, help_text='Count of product')
    pay_type = models.CharField(null=False, default=' ', max_length=30,
                                help_text='Saves payment type, cash or card or ticket')
    delivery_time = models.CharField(null=False, default='', max_length=50, help_text='Saves date and time to delivery')
    comment = models.CharField(null=False, default=' ', max_length=200, help_text='Comment to the order')
    status = models.CharField(null=False, default='In processing', max_length=50,
                                help_text='Order status')

    def __unicode__(self):
        return self.order_id