from django.urls import path
from django.conf.urls import url
from .views import home, PersonCreateView, PersonListView, \
                        PersonView, GroupCreateView, GroupListView

app_name = 'people'
urlpatterns = [
    path('person/new', PersonCreateView.as_view(), name="person-add"),
    path('', PersonListView.as_view(), name='person-list'),
    url(r'^person/show/(?P<id>[0-9]+)/$', PersonView.as_view(), name='person-detail'),
    # path('<int:id>/update/', CourseUpdateView.as_view(), name='courses-update'),
    # path('<int:id>/delete/', CourseDeleteView.as_view(), name='courses-delete'),
    path('group/new', GroupCreateView.as_view(), name="group-add"),
    path('group/', GroupListView.as_view(), name='group-list'),
]