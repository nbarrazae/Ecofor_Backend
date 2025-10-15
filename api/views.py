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
        response = requests.get('https://api.thecatapi.com/v1/images/search?limit=20&breed_ids=beng&api_key=live_yEibOC2MWOazRnaBlDfAPyWIxZmtUnQutCIcrlfCdESCaVTVs4ZPrijW7rRASmsa')
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Error fetching data from The Cat API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CatsByBreed(APIView):
    def get(self, request, breed_id):
        response = requests.get(f'https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}&limit=10', headers={'x-api-key': 'live_yEibOC2MWOazRnaBlDfAPyWIxZmtUnQutCIcrlfCdESCaVTVs4ZPrijW7rRASmsa'})
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Error fetching data from The Cat API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)