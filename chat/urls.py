from django.urls import path
from . import views

urlpatterns = [
    path('create-account/', views.create_account, name='create_account'),
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('inbox/', views.inbox, name='inbox'),
    path('send-email/', views.send_email, name='send_email'),
    path('logout/', views.logout_view, name='logout'),
    path('retrain-model/', views.retrain_model, name='retrain_model'),
]
