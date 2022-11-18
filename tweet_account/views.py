from django.db.models import Q 
from django.shortcuts import render
from rest_framework.exceptions import NotAcceptable
from rest_framework.response import Response # Rest_framework 
from django.contrib.auth.models import User
from tweet_account.serializers import * # App_serializer
from tweet_account.pagination import * # App_Pagination
from rest_framework.generics import * # Rest_framework 
from tweet_account.utils import * # App_utils
from rest_framework.authtoken.models import Token




# >>>>>>>>>>>>>>>>>>>>>>>>>> User._Related -------------->
class User_Details(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = User_Serializer
    pagination_class = My_pagination 
class User_View(ListAPIView):
    queryset = User.objects.all()
    serializer_class = User_Serializer
    pagination_class = My_pagination    

# >>>>>>>>>>>>>>>>>>>>>>>>>> Like._Related -------------->
class CreateDeleteLikeView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        if self.request.data['user'] != str(self.request.user.id):
            raise NotAcceptable("Not authorized.")

        queryset = self.filter_queryset(self.get_queryset())
        subset = queryset.filter(Q(user_id=self.request.data['user']) & Q(tweet_id=self.request.data['tweet']))

        # If it's already liked, then just dislike.
        if subset.count() > 0:
            subset.first().delete()
            return
        serializer.save()

# >>>>>>>>>>>>>>>>>>>>>>>>>> Tweet._Related -------------->

class ListPublicTweetsView(ListAPIView):
    queryset = Tweet.objects.filter(is_public=False)
    serializer_class = TweetSerializer
    pagination_class = My_pagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()) # Queryset Access
        queryset = queryset.filter(Q(is_public=False) & Q(type=0))

        for tweet in queryset:
            tweet_id = tweet.id
            likes_count = Like.objects.filter(tweet=tweet_id).count()

            tweet.likes_count = likes_count
            tweet.comments_count = tweet.comment.all().count()
            tweet.save()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
# >>>>>>>>>>>>>>>>>>>>>>>>>> Tweet._Related -------------->

class ListUpdateDeleteTweetView(RetrieveUpdateDestroyAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
      


# >>>>>>>>>>>>>>>>>>>>>>>>>> Tweet._Related -------------->

class ListCreateTweetView(ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def perform_create(self, serializer):
        serializer.save(account_owner=self.request.user, type=0)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter((Q(account_owner=request.user) | Q(is_public=False)) & Q(type=0))

        for tweet in queryset:
            tweet_id = tweet.id
            likes_count = Like.objects.filter(tweet=tweet_id).count()

            tweet.likes_count = likes_count
            tweet.comments_count = tweet.comment.all().count()
            tweet.save()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
# >>>>>>>>>>>>>>>>>>>>>>>>>> Tweet._Related -------------->


class CreateCommentView(ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        override_view_attributes(self)

    def perform_create(self, serializer):
        parent_id = int(self.request.data['parent'])
        tweets = Tweet.objects.filter(id=parent_id, is_public=False)

        if tweets.count() != 1:
            raise NotFound()

        serializer.save(account_owner=self.request.user, type=1, is_public=False, parent_id=parent_id)
# >>>>>>>>>>>>>>>>>>>>>>>>>> Tweet._Related -------------->

class ListUpdateDeleteCommentView(RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    
    def perform_update(self, serializer):
        comment_id = int(self.kwargs.get('pk'))

        queryset = self.filter_queryset(self.queryset)
        queryset = queryset.filter(Q(id=comment_id) & Q(account_owner=self.request.user))

        if queryset.count() != 1:
            raise NotFound("Comment not found.")

        comment = queryset.get()

        serializer.save(parent=comment.parent, is_public=False)
# >>>>>>>>>>>>>>>>>>>>>>>>>> Tweet._Related -------------->



