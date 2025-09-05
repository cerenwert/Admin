from rest_framework import generics, permissions
from .models import ModelPerson, Offer
from .serializers import ModelPersonSerializer, OfferSerializer

class ModelPersonListCreateView(generics.ListCreateAPIView):
    queryset = ModelPerson.objects.all().order_by("id")
    serializer_class = ModelPersonSerializer
    permission_classes = [permissions.AllowAny]

class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all().order_by("-id")
    serializer_class = OfferSerializer
    permission_classes = [permissions.AllowAny]
