from django.contrib import admin
from tour.models import Tour, TourImage, Highlights

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
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "tour_id",
    )

