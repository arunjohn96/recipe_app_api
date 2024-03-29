from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredients, Recipe
from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """ base viewset for user owned recipe attributes """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Return objects for current authenticated user """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ Create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """ Manage Tags in the database """
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientsViewSet(BaseRecipeAttrViewSet):
    """ Manage the ingredients in the database """
    queryset = Ingredients.objects.all()
    serializer_class = serializers.IngredientSerializers


class RecipeViewSet(viewsets.ModelViewSet):
    """ manage recipes in the database """
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """ Convert a list of strig ID's to a list of intergers """
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """ Retrieve the recipes for the authenticated user """
        tag = self.request.query_params.get('tag')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tag:
            tag_ids = self._params_to_ints(tag)
            queryset = queryset.filter(tag__id__in=tag_ids)
        if ingredients:
            ingredient_id = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_id)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """ Return appropriate serializer class """
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializers):
        """ Create a new recipe """
        serializers.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ upload an image to recipe """
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
