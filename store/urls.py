from django.urls import path
from . import views

urlpatterns = [
    # /store/ page and user admin requests
    path('', views.index, name='index'),
    path('sold/', views.sold, name='sold'),
    path('approved/', views.approved, name='approved'),
    path('kicked-back/', views.kicked_back, name='kicked-back'),
    path('denied/', views.denied, name='denied'),
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name="login"),
    path('logout/', views.logout_request, name="logout"),
    # database requests
    path('dbrequests/approve/', views.approve_item, name="approve-item"),
    path('dbrequests/kick-back/', views.kick_back_item, name="kick-back-item"),
    path('dbrequests/deny/', views.deny_item, name="deny-item"),
    path('dbrequests/sell/', views.sell_item, name="sell-item"),
    path('dbrequests/submit/', views.submit_item, name="submit-item"),
]