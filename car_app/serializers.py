from rest_framework import serializers
from .models import *

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class ClientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'image', 'role_type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Client.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class CompanyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                      'age', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Company.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
            'username': instance.username,
            'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']

class CarMakeSerializers(serializers.ModelSerializer):
    class Meta:
        model = CarMake
        fields = '__all__'

class CarModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = '__all__'

class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['brand_name']

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']

class ColorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class EquipmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class CarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class CarListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'car_name', 'car_image']


class ReviewCarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'comment', 'created_at']


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CarDetailSerializers(serializers.ModelSerializer):
    year = serializers.DateField(format('%d-%m-%Y'))
    brand = BrandSerializers()
    category = CategorySerializers()
    seller = UserProfileSerializers()
    reviews = ReviewCarSerializers()
    class Meta:
        model = Car
        fields = ['id', 'car_name', 'car_image', 'brand', 'year', 'car_body',
                  'category', 'price', 'fuel_type', 'description','seller', 'video', 'reviews',  'created_at']

class OrderListSerializers(serializers.ModelSerializer):
    car = CarListSerializers()
    class Meta:
        model = Order
        fields = ['car']


class OrderDetailSerializers(serializers.ModelSerializer):
    car = CarListSerializers()
    buyer = UserProfileSerializers()
    class Meta:
        model = Order
        fields = '__all__'





class ReviewCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class ClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class AdvertisementSerializers(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'

class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class FavouriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'

class FavouriteItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = FavouriteItem
        fields = '__all__'



