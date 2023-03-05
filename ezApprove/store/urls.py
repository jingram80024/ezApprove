from django.urls import path
from . import views

urlpatterns = [
    # /store/
    path('', views.index, name='index'),
    path('sold/', views.sold, name='sold'),
    path('approved/', views.approved, name='approved'),
    path('kicked-back/', views.kicked_back, name='kicked-back'),
    path('denied/', views.denied, name='denied'),
]