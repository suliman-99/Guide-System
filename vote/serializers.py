from rest_framework import serializers
from .models import *


class VotedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotedItem
        fields = '__all__'
