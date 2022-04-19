import json

from django.db.models import Q
from django.http      import JsonResponse
from django.views     import View
from datetime         import datetime

from core.utils      import signin_decorator
from users.models    import User
from products.models import Product, Detail


class ProductView(View):
    @signin_decorator
    def post(self, request):
        try:
            user = request.user
            data = json.loads(request.body)
            title = data['title']
            description = data['description']
            total_target_amount = data['total_target_amount']
            end_date = data['end_date']
            funding_amount = data['funding_amount']
            
            pid = Product.objects.create(
                user = user,
                title = title,
                description = description,
                total_target_amount = total_target_amount,
                end_date = end_date,
                funding_amount = funding_amount
            )

            Detail.objects.create(
                product_id = pid,
                total_sponsor = 0,
                current_funding_amount  = 0,
                target_rate = 0
            )

            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'message':'PRODUCT_DOES_NOT_EXIST'}, status = 404)

            product = Product.objects.select_related('detail').get(id=product_id)
            # detail = Detail.objects.get(id=product_id)

            result = {
                'nickname' : product.user.nickname,
                'title' : product.title,
                'description' : product.description,
                'total_target_amount' : product.total_target_amount,
                'funding_amount' : product.funding_amount,
                'total_sponsor' : product.detail.total_sponsor,
                'current_funding_amount' : product.detail.current_funding_amount,
                'target_rate' : product.detail.target_rate,
                'end_date' : product.end_date,
                'd-day' : (f'{(product.end_date - datetime.now().date()).days}일 남았습니다')
            }

            return JsonResponse({'result':result}, status = 200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)    

    @signin_decorator
    def patch(self, request, product_id):
        try:
            user = request.user
            data = json.loads(request.body)
            product = Product.objects.get(id=product_id)

            if not Product.objects.filter(user=user).exists():
                return JsonResponse({'message':'INVALID_USER'}, status=403)

            title = data['title']
            description = data['description']
            funding_amount = data['funding_amount']
            end_date = data['end_date']
        
            product.title = title
            product.description = description
            product.funding_amount = funding_amount
            product.end_date = end_date
            product.save()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        except Product.DoesNotExist:
            return JsonResponse({'message':'PRODUCT_DOES_NOT_EXIST'}, status = 404)
            
    @signin_decorator
    def delete(self, request, product_id):
        try:
            user = request.user
            product = Product.objects.get(id=product_id)

            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'message':'DOES_NOT_EXISTS'}, status=404)

            if not product.user == user:
                return JsonResponse({'MESSAGE':'INVALID_USER'}, status=403)
            
            product.delete()

            return JsonResponse({'message':'SUCCESS'}, status =204)

        except Product.DoesNotExist:
            return JsonResponse({'message':'PRODUCT_DOES_NOT_EXIST'}, status = 404)

# class ProductListView(View):
#     def get(self):