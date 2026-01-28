from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace_home, name='marketplace_home'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('<int:owner_id>/', views.user_posts, name='user_posts'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('buy/<int:post_id>/', views.buy_jersey, name='buy_jersey'),
    path('confirm_purchase/<int:post_id>/', views.confirm_purchase, name='confirm_purchase'),
]