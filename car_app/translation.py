from modeltranslation.translator import register, TranslationOptions
from .models import (Car, Category, Review)


@register(Car)
class CarTranslationOptions(TranslationOptions):
    fields = ('car_name', 'description')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('comment',)
