from django.urls import path
from .views import home, PersonCreateView, PersonListView


app_name = 'people'
urlpatterns = [
    # path('', home, name="home_page"),
    path('person/new', PersonCreateView.as_view(), name="person-add"),
    path('', PersonListView.as_view(), name='person-list'),
    # path('create/', CourseCreateView.as_view(), name='courses-create'),
    # path('<int:id>/', CourseView.as_view(), name='courses-detail'),
    # path('<int:id>/update/', CourseUpdateView.as_view(), name='courses-update'),
    # path('<int:id>/delete/', CourseDeleteView.as_view(), name='courses-delete'),
]