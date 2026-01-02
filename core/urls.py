from django.urls import path 
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('callback/', views.callback, name='callback'),
    path('roast/', views.roast_me, name='roast_me'),
    path('r/<uuid:roast_id>/', views.view_roast, name='view_roast'),
    path('manual/', views.roast_manual, name='roast_manual'),
    path('api/get_roast_data/', views.roast_api_data, name='roast_api_data'),
] 
