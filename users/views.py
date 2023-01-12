import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from users.models import User, Location
from hw_27 import settings


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        users_qs = User.objects.annotate(ads=Count("ad", filter=Q(ad__is_published=True)))

        paginator = Paginator(users_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "role": user.role,
                "age": user.age,
                "locations": list(map(str, user.locations.all())),
                "total_ads": user.ads,
            })

        response = {
            "items": users,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": list(map(str, user.locations.all())),
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ["name", "author", "price", "description", "category", "image"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            username=user_data["username"],
            role=user_data["role"],
            age=user_data["age"],
        )

        for location in user_data["locations"]:
            location_obj, _ = Location.objects.get_or_create(name=location)
            user.locations.add(location_obj)

        user.save()

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": list(map(str, user.locations.all())),
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ["name", "author", "price", "description", "category", "image"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        self.object.first_name = user_data['first_name']
        self.object.last_name = user_data['last_name']
        self.object.username = user_data['username']
        self.object.role = user_data['role']
        self.object.age = user_data['age']

        for location in user_data["locations"]:
            location_obj, _ = Location.objects.get_or_create(name=location)
            self.object.locations.add(location_obj)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "age": self.object.age,
            "locations": list(map(str, self.object.locations.all())),
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserZListView(View):
    def get(self, request):
        user_qs = User.objects.annotate(ads=Count("ad"))

        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "role": user.role,
                "age": user.age,
                "locations": list(map(str, user.locations.all())),
                "total_ads": user.ads,
            })

        response = {
            "items": users,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
        }

        return JsonResponse(response, safe=False)
