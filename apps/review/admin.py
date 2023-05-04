from django.contrib import admin
from .models import ReviewImages, ApartmentReview

# class ReviewImagesInline(admin.TabularInline):
#     model = ReviewImages
    
# class ReviewAdmin(admin.ModelAdmin):
#     inlines = [ReviewImagesInline]

admin.site.register( ApartmentReview)