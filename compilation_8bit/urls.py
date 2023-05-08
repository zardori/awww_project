from django.urls import path

from . import views

app_name = 'compilation_8bit'
urlpatterns = [
    path('', views.index, name='index'),
    path('get_file_system/', views.get_file_system, name='get_file_system'),
    path('del_dir', views.del_dir, name='del_dir'),
    path('del_file', views.del_file, name='del_file'),
    path('add_file', views.add_file, name='add_file'),
    path('get_compilation_standard', views.get_compilation_standard,
         name='get_compilation_standard'),
    path('set_compilation_standard', views.set_compilation_standard,
         name='set_compilation_standard'),
    path('select_file', views.select_file, name='select_file'),

]
