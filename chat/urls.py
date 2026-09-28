from django.urls import path
from .views import home, ask
urlpatterns=[
    path("",home, name="home"),
    path("ask/", ask, name="ask"),
    

]