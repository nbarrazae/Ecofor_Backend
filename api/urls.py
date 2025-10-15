from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, RandomCats, CatsByBreed

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('logout/', TokenRefreshView.as_view(), name='token_refresh'),
    path('random-cats/', RandomCats.as_view(), name='random_cats'),
    path('cats-by-breed/<str:breed_id>/', CatsByBreed.as_view(), name='cats_by_breed'),


    ]
