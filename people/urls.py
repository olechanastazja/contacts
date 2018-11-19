from django.urls import path
from .views import home, PersonCreateView


app_name = 'people'
urlpatterns = [
    path('', home, name="home_page"),
    path('person/new', PersonCreateView.as_view(), name="person-add")
]