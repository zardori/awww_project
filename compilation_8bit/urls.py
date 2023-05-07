from django.urls import path

from . import views

app_name = 'compilation_8bit'
urlpatterns = [
    path('', views.index, name='index'),
    path('get_file_system/', views.get_file_system, name='get_file_system'),
    path('del_dir', views.del_dir, name='del_dir'),
    path('del_file', views.del_file, name='del_file'),

]
