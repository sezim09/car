from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *
from .models import *
from rest_framework import viewsets, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CarFilter
from rest_framework.filters import SearchFilter, OrderingFilter




class ClientUserView(generics.CreateAPIView):
    serializer_class = ClientUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CompanyUserView(generics.CreateAPIView):
    serializer_class = CompanyUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers

class CarMakeViewSet(viewsets.ModelViewSet):
    queryset = CarMake.objects.all()
    serializer_class = CarMakeSerializers

class CarModelViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['carmodel_name']
    search_fields = ['carmodel_name']

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyUserSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializers

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category_name']

class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['color_name']

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializers


class CarListAPIView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListSerializers

class CarDetailAPIView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarDetailSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CarFilter
    search_fields = ['car_name', 'brand', 'price', 'created_at']
    ordering_fields = ['car_name', 'brand', 'price', 'created_at']

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializers

class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializers

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers

class ReviewCreate( generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers


class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializers

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializers

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializers

class FavouriteViewSet(viewsets.ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializers

class FavouriteItemViewSet(viewsets.ModelViewSet):
    queryset = FavouriteItem.objects.all()
    serializer_class = FavouriteItemSerializers

