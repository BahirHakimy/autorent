from rest_framework import serializers
from .models import Tour, TourImage, Highlights, Transfer, Review, Hotel

# from authentication.serializers import UserSerializer


class HighlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Highlights
        fields = [
            "id",
            "title",
        ]


class TourSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(use_url=True)
    highlights = HighlightSerializer(read_only=True, many=True)
    image_ids = serializers.SerializerMethodField('get_images')

    class Meta:
        model = Tour

        fields = [
            "id",
            'title',
            'description',
            'highlights',
            'availability',
            'category',
            'sub_category',
            'image_ids',
            'cover_image',
            'duration',
            'distance',
            'price_from',
            'pickup',
            'featured',
            'pickup_information',
            'additional_notes',
        ]


    def get_images(self,object):
        images = TourImage.objects.filter(tour_id=object.id)

        serialized = TourImageSerializer(images,many=True,context=self.context)
        
        return serialized.data

class TourImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = TourImage
        fields = [
            "id",
            "image",
        ]


class TransferSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Transfer
        fields = [
            "id",
            "title",
            "code",
            "cancellation_policy",
            "cost_from",
            "image",
        ]


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            "id",
            "name",
            "comment",
            "rating",
            "tour_id",
            "email",
        ]
        

class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = [
            "id",
            "name",
            "address",
        ]