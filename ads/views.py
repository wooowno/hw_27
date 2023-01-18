from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad, Category, Selection
from ads.permissions import IsOwner, IsModerator
from ads.serializers import CategorySerializer, AdDetailSerializer, AdCreateSerializer, AdUpdateSerializer, \
    AdDestroySerializer, AdListSerializer, SelectionListSerializer, SelectionDetailSerializer, \
    SelectionCreateSerializer, SelectionUpdateSerializer, SelectionDestroySerializer


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.order_by("-price")

        ad_cat = request.GET.get('cat', None)
        if ad_cat:
            self.queryset = self.queryset.filter(
                category__id=ad_cat,
            )

        ad_text = request.GET.get('text', None)
        if ad_text:
            self.queryset = self.queryset.filter(
                text__icontains=ad_text,
            )

        ad_location = request.GET.get('location', None)
        if ad_location:
            self.queryset = self.queryset.filter(
                author__locations__contains=ad_location,
            )

        ad_price_from = request.GET.get('price_from', None)
        ad_price_to = request.GET.get('price_to', None)
        if ad_price_from and ad_price_to:
            self.queryset = self.queryset.filter(
                price__range=[ad_price_from, ad_price_to],
            )

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated]


class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    permission_classes = [IsAuthenticated]


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = (IsOwner | IsAdminUser | IsModerator,)


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDestroySerializer
    permission_classes = (IsOwner | IsAdminUser | IsModerator,)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "description", "category", "image"]

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES["image"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category": self.object.category,
            "image": self.object.image.url if self.object.image else None,
        }, safe=False)


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer


class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionUpdateSerializer
    permission_classes = [IsOwner]


class SelectionDestroyView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDestroySerializer
    permission_classes = [IsOwner]
