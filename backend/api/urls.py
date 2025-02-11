from django.urls import path
from .views import HelloWorldView, login_view,obtenerRegistros

urlpatterns = [
    path('hello/', HelloWorldView.as_view(), name='hello'),
    path('login', login_view, name='login'),
    path('getCedulas', obtenerRegistros, name='getCedulas')
]