from django.conf.urls import url
from .views import *
from django.urls import path, re_path

from .views import showNotification
app_name = 'Notification'
urlpatterns = [
    
    re_path(r'^all/$', showNotification,  {'IsFilter': 'all'},name="AllNotification"),
    re_path(r'^l/$', openListNotification, name="NotificationPaginationList"),
    re_path(r'^n/(?P<pk>\d+)/$', openNotificationFullObject, name="NotificationFullForm"),
    re_path(r'^n/$', createNotificationFullObject, name="NotificationFullFormCreate"),
    #re_path(r'^all/', index,  {'IsFilter': 'all'},name="AllNotification"),
    #re_path(r'^month/', index,  {'IsFilter': 'today'},name="ThisMonthNotification"),
    #re_path(r'^a/', api_active, name="api_active"),
    #re_path(r'^c/', api_create, name="api_create"),
    #re_path(r'^u/<int:pk>/', api_update, name="api_update"),
    #re_path(r'^n/c/',      CrudNotification.createNotification, name='createObjectNotification'), 
    #re_path(r'^n/(?P<pk>\d+)/', CrudNotification.updateNotification, name="updateObjectNotification"),
    #re_path(r'^test_pk/(?P<pk>\d+)/', view_test_pk, name="test_pk"),
    #re_path(r'^test_pk_create/', test_pk_create, name="test_pk_create"),
    #re_path(r'^test_page_choose/', test_page_choose, name="test_page_choose"),
    #re_path(r'^test_page_list/', Notification_list_paginator, name="Notification_list_paginator"),
    #re_path(r'^$', index,  {'IsFilter': 'active'},name="activeNotification"),
    

    re_path(r'^ajax/c/a$', api_AddComment,name="apiAddComment"),
    re_path(r'^ajax/a/a$', api_AddAct,name="api_AddAct"),
    re_path(r'^ajax/i/a$', api_AddImage,name="api_AddImage"),
]



