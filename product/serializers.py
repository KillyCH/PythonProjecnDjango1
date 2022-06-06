from rest_framework import serializers
from .models import Product, Tag, Review


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title'.split()


class ReviewSerializer(serializers.ModelSerializer):
    product = ProductItemSerializer(many=False)

    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    filtered_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id filter_reviews title price rating tags reviews filtered_reviews'.split()

    def get_filtered_reviews(self, product):
        reviews = product.reviews.filter(rating__gt=3)
        # reviews = Review.objects.filter(product=product)
        # return ReviewSerializer(reviews, many=True).data
        return [{'id': review.id,
                'text': review.text,
                'rating': review.rating} for review in reviews]


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=20,
        allow_null=False,
        required=True
    )
    price = serializers.FloatField(
        min_value=20,
        max_value=100_000
    )
    tag = serializers.