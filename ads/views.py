import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Ad, Category
from users.models import User
from hw_27 import settings


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.select_related("author").select_related("category").order_by("-price")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ads = []
        for ad in page_obj:
            ads.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "category": ad.category,
                "image": ad.image.utl if ad.image else None,
            })

        response = {
            "items": ads,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category": ad.category,
            "image": ad.image.utl if ad.image else None,
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author", "price", "description", "category", "image"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        ad = Ad.objects.create(
            name=ad_data["name"],
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
        )

        ad.author = get_object_or_404(User, pk=ad_data["author_id"])
        ad.category, _ = Category.objects.get_or_create(name=ad_data["category"])
        
        ad.save()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category": ad.category,
            "image": ad.image.utl if ad.image else None,
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "description", "category", "image"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        self.object.name = ad_data['name']
        self.object.price = ad_data['price']
        self.object.description = ad_data['description']
        self.object.is_published = ad_data['is_published']

        self.object.category, _ = Category.objects.get_or_create(name=ad_data["category"])

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
            "image": self.object.image.utl if self.object.image else None,
        }, safe=False)


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
            "image": self.object.image.utl if self.object.image else None,
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("name")

        categories = []
        for category in self.object_list:
            categories.append({
                "id": category.id,
                "name": category.name,
            })

        return JsonResponse(categories, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data["name"],
        )

        category.save()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        category_data = json.loads(request.body)

        self.object.name = category_data['name']

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
