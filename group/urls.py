from django.urls import path, re_path
from .views import (GroupListView,
                    GroupCreateView,
                    GroupUpdateView,
                    GroupDeleteView)

app_name = 'group'
urlpatterns = [
    path('new/', GroupCreateView.as_view(), name="group-add"),
    path('', GroupListView.as_view(), name='group-list'),
    re_path(r'^update/(?P<id>[0-9]+)/$', GroupUpdateView.as_view(), name='group-update'),
    re_path(r'^delete/(?P<id>[0-9]+)/$', GroupDeleteView.as_view(), name='group-delete'),
]