from datetime import * # datetime
from django.db.models import * # Model
from django.contrib.auth.models import User



class DateTimeUpdated(Model):
    created_at = DateTimeField(auto_now_add=True, editable=False)
    updated_at = DateTimeField(auto_now=True, editable=False)
    class Meta:
        abstract = True

class Tweet(DateTimeUpdated):
    PUBLICTWEET = False
    PRIVATETWEET = True
    TWEET_CHOICS = (
        (PUBLICTWEET, 'Public'), 
        (PRIVATETWEET, 'Private')
    )
    type = IntegerField(default=0, null=False, blank=False, editable=False)
    account_owner = ForeignKey('auth.User',on_delete=CASCADE)
    tweet_text = CharField(max_length=128, null=False, blank=False) # Text
    likes_count = IntegerField(default=0, null=False, blank=False, editable=False)
    comments_count = IntegerField(default=0, null=False, blank=False, editable=False)
    is_public = BooleanField(default = False, help_text = "0-Public, 1-Private", null=False, blank=False, choices = TWEET_CHOICS)

    def __str__(self):
        return self.tweet_text

class Like(DateTimeUpdated):
    tweet = ForeignKey('Tweet',on_delete=CASCADE,)
    user = ForeignKey('auth.User',on_delete=CASCADE, )

    def __str__(self):
        return self.tweet.tweet_text

class Reference(Tweet):
    pass

class Comments(Reference):
    parent = ForeignKey('Tweet',on_delete=CASCADE, related_name='comment')
    def __str__(self):
        return self.tweet_text