from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import Tour, TourImage, Highlights, Transfer, Review, Hotel
from django.db.models import Q
from .serializers import (
    TourSerializer, TourImageSerializer, HighlightSerializer, TransferSerializer, ReviewSerializer, HotelSerializer
)


class HighlightViewSet(viewsets.ModelViewSet):
    queryset = Highlights.objects.all()
    serializer_class = HighlightSerializer
    permission_classes = [AllowAny]

    

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        tour_images = request.data.getlist('tour_image')
        highlights = request.data.getlist('highlights')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tour = serializer.save()
        for image in tour_images:
            TourImage.objects.create(image=image, tour_id=tour)
        # for highlight in highlights:

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        page_number = request.query_params.get("page", 1)
        paginated = Paginator(self.queryset, 20)
        paged_data = paginated.page(page_number)
        has_next = paged_data.has_next()

        serializer = TourSerializer(
            paged_data,
            many=True,
            context={"request": request},
        )
        return Response({"results": serializer.data, "has_next": has_next})

    

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def search(self, request, *args, **kwargs):
        pickup = request.data.get("pickup_datetime")
        dropoff = request.data.get("dropoff_datetime")
        filter_type = request.data.get("car_type")
        if pickup and dropoff:
            pickup_datetime = datetime.strptime(pickup, "%Y-%m-%dT%H:%M")
            dropoff_datetime = datetime.strptime(dropoff, "%Y-%m-%dT%H:%M")
            cars = self.get_queryset()
            if filter_type:
                cars = cars.filter(car_type=filter_type)
            available_cars = [
                car
                for car in cars
                if car.check_availability(pickup_datetime, dropoff_datetime)
            ]

            serializer = CarSerializer(
                available_cars,
                many=True,
                context={"request": request},
            )

            return Response(serializer.data)
        else:
            return Response(
                {"detail": "pickup_datetime and dropoff_datetime are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [AllowAny]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [AllowAny]