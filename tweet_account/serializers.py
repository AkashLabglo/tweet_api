from rest_framework.serializers import * 
from tweet_account.models import *
from django.contrib.auth.models import User




class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'tweet')


class User_Serializer(ModelSerializer):
    #tweets = PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=Tweet.objects.all()
    # ) #, 'tweets'

    class Meta:
        model = User
        fields = ('id', 'username')

class CommentSerializer(ModelSerializer):
    account_owner = ReadOnlyField(source='account_owner.username')
    class Meta:
        model = Comments
        fields = ('id', 'tweet_text', 'account_owner','type', 'is_public', 'likes_count', 'comments_count', 'parent',
                  'created_at', 'updated_at')
    

class TweetSerializer(ModelSerializer):
    account_owner = ReadOnlyField(source='account_owner.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Tweet
        fields = ('id', 'tweet_text','type', 'account_owner', 'is_public', 'likes_count', 'comments_count', 'comments', 'created_at',
                  'updated_at')
        read_only_fields = ('created_at', 'updated_at')


