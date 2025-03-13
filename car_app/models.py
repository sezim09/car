from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from multiselectfield import MultiSelectField
from rest_framework.exceptions import ValidationError

ROLE_CHOICES = (
    ('client', 'client'),
    ('owner', 'owner')
)

class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True,blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18),
                                                       MaxValueValidator(70)], null=True, blank=True)
    STATUS_CHOICES = (
        ('client', 'client'),
        ('owner', 'owner')
    )
    status_choices = models.CharField(max_length=32, choices=STATUS_CHOICES, null=True, blank=True)
    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

class CarMake(models.Model):
    carmake_name = models.CharField(max_length=32)
    carmake_image = models.FileField(upload_to='carmake_images/', null=True, blank=True)

class CarModel(models.Model):
    carmodel_name = models.CharField(max_length=32)
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)

class Brand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.brand_name

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name

class Color(models.Model):
    color_name = models.CharField(max_length=32)
    color_image = models.FileField(upload_to='color_images/', null=True, blank=True)

class Equipment(models.Model):
    condition = models.TextField()
    APPEARANCE_CHOICES = (
        ('обвес', 'обвес'),
        ('тонировка', 'тонировка'),
        ('спойлер', 'спойлер'),
        ('литые диски', 'литые диски'),
        ('люк', 'люк'),
        ('лебёдка', 'лебёдка'),
        ('рейлинги', 'рейлинги'),
        ('багажник', 'багажник'),
        ('фаркоп', 'фаркоп'),
        ('панорамная крыша', 'панорамная крыша')
    )
    Appearance = MultiSelectField(max_length=62, choices=APPEARANCE_CHOICES, max_choices=10)
    SALON_CHOICES =(
        ('велюр', 'велюр'),
        ('кожа', 'кожа'),
        ('шторки', 'шторки'),
        (' алькантара', ' алькантара'),
        ('комбинированный', 'комбинированный'),
        ('дерево', 'дерево')
    )
    salon = MultiSelectField(max_length=62, choices=SALON_CHOICES, max_choices=1)
    MEDIA_CHOICES = (
        ('CD', 'CD'),
        ('DVD', 'DVD'),
        ('MP3', 'MP3'),
        ('USB', 'USB'),
    )
    media = MultiSelectField(max_length=32, choices=MEDIA_CHOICES, max_choices=1)
    option = models.CharField(max_length=100)
    ad = models.TextField()


class Car(models.Model):
    car_name = models.CharField(max_length=64)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='car_brand')
    CARS_BODY_TYPE = (
        ('Лифтбек', 'Лифтбек'),
        ('Купе', 'Купе'),
        ('Кабриолет', 'Кабриолет')
    )
    year = models.DateField(auto_now_add=True)
    car_body = models.CharField(max_length=32, choices=CARS_BODY_TYPE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_car')
    car_image = models.ImageField(upload_to='car_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    FUEL_CHOICES = (
        ('Бензин', 'Бензин'),
        ('Дизель','Дизель'),
        ('Газ', 'Газ'),
        ('Гибрид','Гибрид'),
        ('Электро','Электро')
    )
    fuel_type = MultiSelectField(max_length=32, choices=FUEL_CHOICES, max_choices=2)
    description = models.TextField()
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    video = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_avg_rating(self):
        all_reviews = self.Review.all()
        if all_reviews.exists():
          count_people = 0
          total_stars = 0
          for i in all_reviews:
              if i.stars is not None:
                  total_stars += i.stars
                  count_people += 1
          if count_people == 0:
              return 0
          return round(total_stars / count_people, 1)
        return 0

    def get_count_people(self):
        return self.course_review.count()


class Client(models.Model):
    image = models.ImageField(upload_to='client_images')
    role_type = models.CharField(max_length=32, choices=ROLE_CHOICES, default='client')

    def __str__(self):
        return f'{self.role_type}'

class Company(models.Model):
    role_type = models.CharField(max_length=32, choices=ROLE_CHOICES )
    company_name =models.CharField(max_length=32)
    company_image = models.ImageField(unique='company_images/')
    def __str__(self):
        return f'{self.role_type}, {self.company_name}'



class Order(models.Model):
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Ожидание'),
        ('confirmed', 'Подтверждено'),
        ('canceled', 'Отменено'),
    ])


class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    rating = models.IntegerField(choices=[(i, str(i))for i in range(1, 6)],
                                             null=True, blank=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Отзыв от {self.client},  на {self.car}"

    def clean(self):
        super().clean()
        if not self.client and not self.company:
            raise ValidationError('Choose minimum one of (client, company)!')



class Advertisement(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    def __str__(self):
        return  f'{self.car}, {self.is_premium}'


class Cart(models.Model):
    client = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    car = models.ForeignKey( Car,  on_delete=models.CASCADE)

class Favourite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

class FavouriteItem(models.Model):
    favourite = models.ForeignKey(Favourite, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
