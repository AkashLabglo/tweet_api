from rest_framework import permissions
from tweet_account.pagination import * # App
from tweet_account.permissions import IsOwner # App


def override_view_attributes(ref):
    ref.permission_classes = (permissions.IsAuthenticated,
                              IsOwner)
    ref.pagination_class = My_pagination