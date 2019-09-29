from django.urls import path
from . import views

app_name = 'back_test_app'

urlpatterns = [
    path('', views.back_test, name='back_test'),
    path('/recent_result/', views.recent_result, name='recent_result'),
]
