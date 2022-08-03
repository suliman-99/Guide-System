from django_filters import FilterSet, BooleanFilter
from django_filters.rest_framework import *
from .models import *


class ForumFilter(FilterSet):

    class Meta:
        model = Forum
        fields = ['is_question', 'is_closed']

    is_closed = BooleanFilter(method='get_is_closed', label='is_closed')
    is_mine = BooleanFilter(method='get_is_mine', label='is_mine')

    def get_is_closed(self, queryset, name, value):
        if value:
            return queryset.filter(closed_reply__isnull=False)
        return queryset.filter(closed_reply__isnull=True)

    def get_is_mine(self, queryset, name, value):
        user_id = self.request.user.id
        if value:
            return queryset.filter(user_id=user_id)
        return queryset
