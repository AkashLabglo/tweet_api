from django.contrib import admin
from django.urls import path
from tweet_account.views import * # App_Views 
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_view/', User_View.as_view(), name="user_view"), 
    path('User_details/<int:pk>', User_Details.as_view(), name = 'User_details'), 


    path('tweet/', ListCreateTweetView.as_view(), name='create'),
    path('tweet/<int:pk>/', ListUpdateDeleteTweetView.as_view(), name='details'),
    path('likes/', CreateDeleteLikeView.as_view(), name='like'),
    path('comments/', CreateCommentView.as_view(), name='comment_create'),
    path('comments/<int:pk>/', ListUpdateDeleteCommentView.as_view(), name='comment_details'),
    path('public/', ListPublicTweetsView.as_view(), name='public_tweets'),
    path('get_token/', obtain_auth_token),
]
