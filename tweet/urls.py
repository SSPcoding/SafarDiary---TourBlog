from django.urls import path
from .import views

urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('feature/', views.feature, name='feature'),
    path('search/', views.search_tweets, name='search_tweets'),
    path("profile/<str:username>/", views.user_profile, name="user_profile"),
    path("update-bio/", views.update_bio, name="update_bio"),
    path("bucket-list/add/<int:tweet_id>/", views.add_to_bucket_list, name="add_to_bucket_list"),
    path("bucket-list/remove/<int:tweet_id>/", views.remove_from_bucket_list, name="remove_from_bucket_list"),
    path("bucket-list/", views.view_bucket_list, name="bucket_list"),
    path("bucket-list/remove/<int:tweet_id>/", views.remove_from_bucket_list, name="remove_from_bucket_list"),

] 
