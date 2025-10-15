from django.shortcuts import render
import requests
# Create your views here.
from rest_framework import generics
from .serializer import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

User = get_user_model()
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []  # Permitir acceso sin autenticación
    serializer_class = RegisterSerializer


class RandomCats(APIView):
    def get(self, request):
        response = requests.get('https://api.thecatapi.com/v1/images/search?limit=18&has_breeds=1&abys&api_key=yEibOC2MWOazRnaBlDfAPyWIxZmtUnQutCIcrlfCdESCaVTVs4ZPrijW7rRASmsa')

        jsonArray = []
        # print id de cada gato
        for cat in response.json():
            response = requests.get(f'https://api.thecatapi.com/v1/images/{cat["id"]}')
            jsonArray.append(response.json())
        return Response(jsonArray, status=status.HTTP_200_OK)
        
class CatsByBreed(APIView):
    def get(self, request, breed_id):
        response = requests.get(f'https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}&limit=10', headers={'x-api-key': 'live_yEibOC2MWOazRnaBlDfAPyWIxZmtUnQutCIcrlfCdESCaVTVs4ZPrijW7rRASmsa'})
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Error fetching data from The Cat API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class FavoriteCatsView(APIView):
    def get(self, request):
        user = request.user
        favorite_cats = user.favorite_cats.all()
        data = [{'cat_id': fav.cat_id, 'image_url': fav.image_url} for fav in favorite_cats]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        cat_id = request.data.get('cat_id')
        image_url = request.data.get('image_url')

        if not cat_id or not image_url:
            return Response({'error': 'cat_id and image_url are required'}, status=status.HTTP_400_BAD_REQUEST)

        favorite_cat, created = user.favorite_cats.get_or_create(cat_id=cat_id, defaults={'image_url': image_url})

        if created:
            return Response({'message': 'Cat added to favorites'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Cat is already in favorites'}, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        cat_id = request.data.get('cat_id')

        if not cat_id:
            return Response({'error': 'cat_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            favorite_cat = user.favorite_cats.get(cat_id=cat_id)
            favorite_cat.delete()
            return Response({'message': 'Cat removed from favorites'}, status=status.HTTP_200_OK)
        except favorite_cat.DoesNotExist:
            return Response({'error': 'Cat not found in favorites'}, status=status.HTTP_404_NOT_FOUND)