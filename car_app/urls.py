from .views import *
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework import routers

router = DefaultRouter()
router.register(r'UserProfile', UserProfileViewSet)
router.register(r'CarMake', CarMakeViewSet)
router.register(r'CarModel', CarModelViewSet)
router.register(r'Brand', BrandViewSet)
router.register(r'Category', CategoryViewSet)
router.register(r'Color', ColorViewSet)
router.register(r'Equipment', EquipmentViewSet)
router.register(r'Review', ReviewViewSet)
router.register(r'Advertisement', AdvertisementViewSet)
router.register(r'Cart', CartViewSet)
router.register(r'CartItem', CartItemViewSet)
router.register(r'Favourite', FavouriteViewSet)
router.register(r'FavouriteItem', FavouriteItemViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('car/', CarListAPIView.as_view(), name='car_list'),
    path('car/<int:pk>/', CarDetailAPIView.as_view(), name='car_detail'),
    path('order/', OrderListAPIView.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderDetailAPIView.as_view(), name='order_detail')
]
