from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('websocket-test/', views.websocket_test, name='websocket_test'),
    path("api/metrics/history/", views.metric_history, name="metric_history"),
    path("dashboard/", views.dashboard, name="dashboard"),
]