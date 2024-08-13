from django.contrib import admin
from tour.models import Tour, TourImage, Highlights, Transfer, Hotel, Review

@admin.register(Highlights)
class HighlightAdmin(admin.ModelAdmin):
    list_display = (
        "title",
    )
    search_fields = ("title",)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "availability",
        "price_from",
        "featured",
    )
    list_filter = ("category",'availability','featured')
    search_fields = ("title","category","availability")


@admin.register(TourImage)
class TourImageAdmin(admin.ModelAdmin):
    list_display = (
        "tour_id",
    )

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    pass

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

