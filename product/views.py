from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, ProductValidateSerializer
from .models import Product


@api_view(['GET'])
def test(request):
    dict_ = {
        'str': "Hello world",
        'int': 100,
        'float': 99.9,
        'bool': True,
        'list': [1, 2, 3]
    }
    return Response(data=dict_, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def product_list_create_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(data=serializer.data)
    else:
        validate_serializer = ProductValidateSerializer(data=request.data)
        if not validate_serializer.is_valid():
            return Response(data=validate_serializer.errors)

        title = request.data.get('title')
        price = request.data.get('price')
        text = request.data.get('text')
        tags = request.data.get('tags')
        product = Product.objects.create(title=title, price=price, text=text)
        product.tags.set(tags)
        product.save()
        return Response(data=ProductSerializer(product).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': f'Product object with id = {id}  not found!!!'})
    if request.method == 'GET':
        data = ProductSerializer(product, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(data={'message': 'Product removed'})
    elif request.method == 'PUT':
        product.title = request.data.get('title')
        product.price = request.data.get('price')
        product.text = request.data.get('text')
        product.tags.set(request.data.get('tags'))
        product.save()
        return Response(data=ProductSerializer(product).data)
