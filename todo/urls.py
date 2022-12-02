from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login', views.login),
    path('sign_up', views.sign_up),
    path('logout', views.logout),
    path('delete-note', views.delete_note)
]
