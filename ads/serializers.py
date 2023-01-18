from rest_framework import serializers

from ads.models import Category, Ad, Selection
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Ad
        fields = ['id', 'name', 'username', 'price', 'description', 'is_published', 'image', 'category']


class AdDetailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
        queryset=Category.objects.all(),
    )
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self._category = self.initial_data.pop("category")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        ad = Ad.objects.create(**validated_data)

        ad.category, _ = Category.objects.get_or_create(name=self._category)

        ad.save()
        return ad


class AdUpdateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
        queryset=Category.objects.all(),
    )
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self._category = self.initial_data.pop("category")
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        ad = super.save()

        ad.category, _ = Category.objects.get_or_create(name=self._category)

        ad.save()
        return ad


class AdDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id", "name"]


class SelectionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    items = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Selection.objects.all(),
        slug_field="id"
    )

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    owner = serializers.PrimaryKeyRelatedField(required=False)
    items = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Selection.objects.all(),
        slug_field="id"
    )

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'
