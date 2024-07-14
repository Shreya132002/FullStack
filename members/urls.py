from django.urls import path
from . import views

app_name = 'members'  # Add this line to set the app namespace

urlpatterns = [ 
        path('crop/', views.crop, name='crop_price'),

     path('', views.index, name='index'),
        path('voice_query/', views.voice_query2, name='voice_query'),

    path('handle_table_data/', views.handle_table_data, name='handle_table_data'),
    path('add_crop/', views.add_crop, name='add_crop'),
    path('add/', views.add, name='add'),



 ]

