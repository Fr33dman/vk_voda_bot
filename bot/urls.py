from django.conf.urls import url

from . import views

app_name = 'vk_bot'

urlpatterns = [
    url(r'^$', views.bot, name='index'),
]