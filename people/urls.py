from django.urls import path, re_path
from django.conf.urls import url
from .views import (home,
                    PersonCreateView,
                    PersonListView,
                    PersonView,
                    PersonUpdateView,
                    PersonDeleteView,
                    load_persons,
                    PersonGroupsView)

app_name = 'people'
urlpatterns = [
    path('person/new', PersonCreateView.as_view(), name="person-add"),
    path('', PersonListView.as_view(), name='person-list'),
    re_path(r'^person/detail/(?P<id>[0-9]+)/$', PersonView.as_view(), name='person-detail'),
    re_path(r'^person/update/(?P<id>[0-9]+)/$', PersonUpdateView.as_view(), name='person-update'),
    re_path(r'^person/delete/(?P<id>[0-9]+)/$', PersonDeleteView.as_view(), name='person-delete'),
    re_path(r'^(?P<id>[0-9]+)/groups/$', PersonGroupsView.as_view(), name='person-groups'),
    url(r'^ajax_calls/search/', load_persons, name='search'),
]