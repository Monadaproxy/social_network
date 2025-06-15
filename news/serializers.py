from .models import Articles
from rest_framework import serializers

class ArticlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Articles
        fields = ['title', 'anounce']