from django.urls import path
from . import views

urlpatterns = [
    path('hello', views.hello, name='hello'),
    path('f', views.f, name='f'),
    path('', views.mortality_page_view, name='mortality_page'),
    path('download_file', views.download_file, name='download_file'),
    path('leaders', views.leaders, name='leaders'),

]