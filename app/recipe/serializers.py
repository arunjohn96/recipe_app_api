from rest_framework import serializers

from core.models import Tag, Ingredients


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for Tag object """

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializers(serializers.ModelSerializer):
    """ Serializer for Ingredients objects """

    class Meta:
        model = Ingredients
        fields = ('id', 'name')
        read_only_fields = ('id',)
