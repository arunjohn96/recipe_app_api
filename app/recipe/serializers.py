from rest_framework import serializers

from core.models import Tag, Ingredients, Recipe


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


class RecipeSerializer(serializers.ModelSerializer):
    """ Serialize a  recipe """

    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredients.objects.all()
    )

    tag = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'title', 'ingredients', 'tag',
            'time_minutes', 'price', 'link'
        )
        read_only_fields = ('id',)
