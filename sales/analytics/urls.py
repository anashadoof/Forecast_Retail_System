from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_dashboard, name='analytics'),
    path('api/get_chart/', views.get_chart_data, name='get_chart_data'),
]
