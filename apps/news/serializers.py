from rest_framework import serializers
from .models import News,NewsCategory
from apps.cmsauth.serializers import UserSerializers

class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('name',)

class NewsSerializers(serializers.ModelSerializer):

    author = UserSerializers()
    category = NewsCategorySerializer()
    class Meta:
        model = News
        fields = ('id','title','desc','thumbnail','pub_time','author','category')

