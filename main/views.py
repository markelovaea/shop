from tkinter import READABLE
from turtledemo.sorting_animate import start_ssort

from django.template.context_processors import request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from main.models import Customer, Shop, Cart, Product, CartItem


class CustomerViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        fio = request.data.get("fio")
        if not isinstance(fio, str):  # валидация
            return Response(data={"message": "fio должно быть строкой."}, status=status.HTTP_400_BAD_REQUEST)
        if not fio:
            return Response(data={"message": "fio не может быть пустым"}, status=status.HTTP_400_BAD_REQUEST)

        age = request.data.get("age")
        if not isinstance(age, int):
            return Response(data={"message": "age должно быть числом"}, status=status.HTTP_400_BAD_REQUEST)
        if age < 18:
            return Response(data={"message": "иди домой школьник"}, status=status.HTTP_400_BAD_REQUEST)

        customer = Customer.objects.create(fio=fio, age=age)
        return Response(data={
            "id": customer.id,
            "fio": customer.fio,
            "age": customer.age
        }, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        fio = request.GET.get('fio')
        if fio and not isinstance(fio, str):
            return Response(data={"message": "fio должно быть строкой"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Customer.objects
        if fio:
            queryset = queryset.filter(fio__icontains=fio)  # incontains (like/ilike)

        queryset = queryset.all()
        data = [
            {
                'id': i.id,
                'fio': i.fio,
                'age': i.age
            } for i in queryset
        ]
        return Response({'result': data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk, *args, **kwargs):
        customer = Customer.objects.filter(id=pk).first()
        if not customer:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(
            {
                'id': customer.id,
                'fio': customer.fio,
                'age': customer.age
            }, status=status.HTTP_200_OK)

    def destroy(self, request, pk, *args, **kwargs):
        customer = Customer.objects.filter(id=pk).first()
        if not customer:
            return Response(status=status.HTTP_404_NOT_FOUND)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk, *args, **kwargs):
        customer = Customer.objects.filter(id=pk).first()
        if not customer:
            return Response(status=status.HTTP_404_NOT_FOUND)

        customer.fio = request.data.get('fio')
        customer.age = request.data.get('age')
        customer.save()
        return Response(
            {
                'id': customer.id,
                'fio': customer.fio,
                'age': customer.age
            }, status=status.HTTP_200_OK)

    def partial_update(self, request, pk, *args, **kwargs):
        customer = Customer.objects.filter(id=pk).first()
        if not customer:
            return Response(status=status.HTTP_404_NOT_FOUND)
        fio = request.data.get('fio')
        if fio:
            customer.fio = fio
        age = request.data.get('age')
        if age:
            customer.age = age
        customer.save()
        return Response(
            {
                'id': customer.id,
                'fio': customer.fio,
                'age': customer.age
            }, status=status.HTTP_200_OK)


class ShopViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        if not isinstance(name, str):  # валидация
            return Response(data={"message": "имя должно быть строкой"}, status=status.HTTP_400_BAD_REQUEST)
        if not name:
            return Response(data={"message": "поле имени не может быть пустым"}, status=status.HTTP_400_BAD_REQUEST)

        address = request.data.get('address')
        if not isinstance(address, str):
            return Response(data={'поле адреса не может быть пустым'}, status=status.HTTP_400_BAD_REQUEST)
        if not address:
            return Response(data={'поле адреса не может быть пустым'}, status=status.HTTP_400_BAD_REQUEST)

        open_time = request.data.get('open_time')
        close_time = request.data.get('close_time')

        shop = Shop.objects.create(name=name, address=address, open_time=open_time, close_time=close_time)
        return Response(data={
            'id': shop.id,
            'name': shop.name,
            'address': shop.address,
            'open_time': shop.open_time,
            'close_time': shop.close_time
        }, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        name = request.GET.get('name')
        if not isinstance(name, str):
            return Response(data={'поле имени должно быть строкой'})
        if not name:
            return Response(data={'поле имени не может быть пустым'})

        address = request.GET.get('address')
        if not isinstance(address, str):
            return Response(data={'поле адреса не может быть пустым '})
        if not address:
            return Response(data={'поле адреса не может быть пустым'})

        open_time_lte = request.GET.get('open_time_lte')
        close_time_gte = request.GET.get('close_time_gte')
        if open_time_lte and close_time_gte and open_time_lte < close_time_gte:
            return Response(data={'время открытия не может быть позже времени закрытия'})

        open_time_gte = request.GET.get('open_time_gte')
        close_time_lte = request.GET.get('close_time_lte')
        if open_time_gte and close_time_lte and open_time_gte < close_time_lte:
            return Response(data={'время открытия не может быть позже времени закрытия'})

        queryset = Shop.objects
        if name:
            queryset = queryset.filter(name__icontains=name)
        if address:
            queryset = queryset.filter(address__icontains=address)
        if open_time_lte:
            queryset = queryset.filter(open_time__icontains=open_time_lte)
        if close_time_gte:
            queryset = queryset.filter(close_time__icontains=close_time_gte)
        if open_time_gte:
            queryset = queryset.filter(open_time_gte__incontains=open_time_gte)
        if close_time_lte:
            queryset = queryset.filter(close_time_lte__incontains=close_time_lte)
        queryset = queryset.all()
        data = [
            {
                'id': i.id,
                'name': i.name,
                'address': i.address,
                'open_time': i.open_time,
                'close_time': i.close_time
            } for i in queryset
        ]
        return Response({data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk, *args, **kwargs):
        shop = Shop.objects.filter(id=pk).first()
        if not shop:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(
            {
                'id': shop.id,
                'name': shop.name,
                'address': shop.address,
                'open_time': shop.open_time,
                'close_time': shop.close_time
            }, status=status.HTTP_200_OK)

    def destroy(self, request, pk, *args, **kwargs):
        shop = Shop.objects.filter(id=pk).first()
        if not shop:
            return Response(status=status.HTTP_404_NOT_FOUND)
        shop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk, *args, **kwargs):
        shop = Shop.objects.filter(id=pk).first()
        if not shop:
            return Response(status=status.HTTP_404_NOT_FOUND)

        shop.name = request.data.get('name')
        shop.address = request.data.get('address')
        shop.open_time = request.data.get('open_time')
        shop.close_time = request.data.get('close_time')
        shop.save()
        return Response(
            {
                'id': shop.id,
                'name': shop.name,
                'address': shop.address,
                'open_time': shop.open_time,
                'close_time': shop.close_time
            }, status=status.HTTP_200_OK)

    def partial_update(self, request, pk, *args, **kwargs):
        shop = Shop.objects.filter(id=pk).first()
        if not shop:
            return Response(status=status.HTTP_404_NOT_FOUND)

        name = request.data.get('name')
        if name:
            shop.name = name
        address = request.data.get('address')
        if address:
            shop.address = address
        open_time = request.data.get('open_time')
        if open_time:
            shop.open_time = open_time
        close_time = request.data.get('close_time')
        if close_time:
            shop.close_time = close_time
        shop.save()
        return Response(
            {
                'id': shop.id,
                'name': shop.name,
                'address': shop.address,
                'open_time': shop.open_time,
                'close_time': shop.close_time
            }, status=status.HTTP_200_OK)


class CartViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        customer_id = request.data.get('customer_id')
        shop_id = request.data.get('shop_id')

        cart = Cart.objects.filter(shop_id=shop_id, customer_id=customer_id).first()
        if cart:
            return Response({'в одном магазине не может быть более одной корзины'}, status=status.HTTP_409_CONFLICT)

        cart = Cart.objects.create(customer_id=customer_id, shop_id=shop_id)
        return Response(data={
            'id': cart.id,
            'customer_id': cart.customer_id,
            'shop_id': cart.shop_id
        }, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        customer_id = request.GET.get('customer_id')
        shop_id = request.GET.get('shop_id')

        queryset = Cart.objects
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
        queryset = queryset.all()
        data = [
            {
                'id': i.id,
                'customer_id': i.customer_id,
                'shop_id': i.shop_id
            } for i in queryset
        ]
        return Response({data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk, *args, **kwargs):
        cart = Cart.objects.filter(id=pk).first()
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart.delete()
        return Response(status=status.HTTP_200_OK)

    def update(self, request, pk, *args, **kwargs):
        cart = Cart.objects.filter(id=pk).first()
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart.customer_id = request.data.get('customer_id')
        cart.shop_id = request.data.get('shop_id')
        cart.save()
        return Response(
            {
                'id': cart.id,
                'customer_id': cart.customer_id,
                'shop_id': cart.shop_id
            }, status=status.HTTP_200_OK)

    def partial_update(self, request, pk, *args, **kwargs):
        cart = Cart.objects.filter(id=pk).first()
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)

        customer_id = request.data.get('customer_id')
        if customer_id:
            cart.customer_id = customer_id
        shop_id = request.data.get('shop_id')
        if shop_id:
            cart.shop_id = shop_id
        cart.save()
        return Response({
            'result':
                {
                    'id': cart.id,
                    'customer_id': cart.customer_id,
                    'shop_id': cart.shop_id
                }
        }, status=status.HTTP_200_OK)


class ProductViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        if not isinstance(name, str):  # валидация
            return Response(data={"message": "имя должно быть строкой"}, status=status.HTTP_400_BAD_REQUEST)
        if not name:
            return Response(data={"message": "поле имени не может быть пустым"}, status=status.HTTP_400_BAD_REQUEST)

        price = request.data.get('price')
        if not isinstance(price, int):
            return Response(data={"message": "стоимость должно быть числом"}, status=status.HTTP_400_BAD_REQUEST)
        if price < 0:
            return Response(data={"message": "товар не может ничего не стоить, цените свой труд"},
                            status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.create(name=name, price=price)
        return Response(data={
            'id': product.id,
            'name': product.name,
            'price': product.price
        }, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        name = request.GET.get('name')
        if not isinstance(name, int):
            return Response(data={"message": "стоимость должно быть числом"}, status=status.HTTP_400_BAD_REQUEST)

        price = request.GET.get('price')
        if not isinstance(price, int):
            return Response(data={"message": "стоимость должно быть числом"}, status=status.HTTP_400_BAD_REQUEST)
        if price < 0:
            return Response(data={"message": "товар не может ничего не стоить, цените свой труд"},
                            status=status.HTTP_400_BAD_REQUEST)

        queryset = Product.objects
        if name:
            queryset = queryset.filter(name__icontains=name)
        if price:
            queryset = queryset.filter(price__icontains=price)
        queryset = queryset.all()
        data = [
            {
                'id': i.id,
                'name': i.name,
                'price': i.price
            } for i in queryset
        ]
        return Response({data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk, *args, **kwargs):
        product = Product.objects.filter(id=pk).first()
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({
            'result':
                {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price
                }
        }, status=status.HTTP_200_OK)

    def destroy(self, request, pk, *args, **kwargs):
        product = Product.objects.filter(id=pk).first()
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk, *args, **kwargs):
        product = Product.objects.filter(id=pk).first()
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)

        product.name = request.data.get('name')
        product.price = request.data.get('price')
        product.save()
        return Response({
            'result':
                {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price
                }
        }, status=status.HTTP_200_OK)

    def partial_update(self, request, pk, *args, **kwargs):
        product = Product.objects.filter(id=pk).first()
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        price = request.data.get('price')
        name = request.data.get('name')
        if name:
            product.name = name
        if price:
            product.price = price
        product.save()

        return Response({
            'result':
                {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price
                }
        }, status=status.HTTP_200_OK)


class CartItemViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        cart_id = request.data.get('cart_id')
        if not isinstance(cart_id, int):
            return Response(data={"message": "id корзины должно быть числом"}, status=status.HTTP_400_BAD_REQUEST)

        product_id = request.data.get('product_id')
        if not isinstance(product_id, int):
            return Response(data={"message": "id подукта должно быть числом"}, status=status.HTTP_400_BAD_REQUEST)
        count = request.data.get('count')
        if not isinstance(count, int):
            return Response(data={"message": "стоимость должно быть числом"}, status=status.HTTP_400_BAD_REQUEST)
        if count < 0:
            return Response(data={"message": "товар не может ничего не стоить, цените свой труд"},
                            status=status.HTTP_400_BAD_REQUEST)

        cart_item = CartItem.objects.create(cart_id=cart_id, product_id=product_id, count=count)
        return Response(data={
            'id': cart_item.id,
            'product_id': cart_item.product_id,
            'count': cart_item.count
        }, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        cart_id = request.data.get('cart_id')
        if not isinstance(cart_id, int):
            return Response(data={"message": "id корзины должно быть числом"}, status=status.HTTP_400_BAD_REQUEST)

        product_id = request.data.get('product_id')
        if not isinstance(product_id, int):
            return Response(data={"message": "id подукта должно быть числом"}, status=status.HTTP_400_BAD_REQUEST)

        count = request.data.get('count')
        if not isinstance(count, int):
            return Response(data={"message": "стоимость должно быть числом"}, status=status.HTTP_400_BAD_REQUEST)
        if count < 0:
            return Response(data={"message": "товар не может ничего не стоить, цените свой труд"},
                            status=status.HTTP_400_BAD_REQUEST)

        queryset = CartItem.objects
        if cart_id:
            queryset = queryset.filter(cart_id=cart_id)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        if count:
            queryset = queryset.filter(count=count)
        queryset = queryset.all()
        data = [
            {
                'id': i.id,
                'cart_id': i.cart_id,
                'product_id': i.product_id,
                'count': i.count
            } for i in queryset
        ]
        return Response({data}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk, *args, **kwargs):
        cart_item = CartItem.objects.filter(id=pk).first()
        if not cart_item:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk, *args, **kwargs):
        cart_item = CartItem.objects.filter(id=pk).first()
        if not cart_item:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart_item.cart_id = request.data.get('cart_id')
        cart_item.product_id = request.data.get('product_id')
        cart_item.count = request.data.get('count')
        cart_item.save()
        return Response({
            'result':
                {
                    'id': cart_item.id,
                    'cart_id': cart_item.cart_id,
                    'product_id': cart_item.product_id,
                    'count': cart_item.count
                }
        }, status=status.HTTP_200_OK)

    def partial_update(self, request, pk, *args, **kwargs):
        cart_item = CartItem.objects.filter(id=pk).first()
        if not cart_item:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart_id = request.data.get('cart_id')
        if cart_id:
            cart_item.cart_id = cart_id

        product_id = request.data.get('product_id')
        if product_id:
            cart_item.cart_id = cart_id

        count = request.data.get('count')
        if count:
            cart_item.count = count
        cart_item.save()
        return Response({
            'result':
                {
                    'id': cart_item.id,
                    'cart_id': cart_item.cart_id,
                    'product_id': cart_item.product_id,
                    'count': cart_item.count
                }
        }, status=status.HTTP_200_OK)
