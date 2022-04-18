import json, jwt, bcrypt

from django.views import View
from django.http  import JsonResponse
from django.conf  import settings

from .models      import User
from .utils       import validate_email, validate_password 

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']
            nickname = data['nickname']

            if not validate_email(email):
                return JsonResponse({'message':'EMAIL_VALIDATION_ERROR'}, status=400)

            if not validate_password(password):
                return JsonResponse({'message':'PW_VALIDATION_ERROR'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message':'ALREADY_EXISTS_EMAIL'}, status=409)
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email = email,
                password = hashed_password,
                nickname = nickname,
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class LoginView(View):
    def post(self, request):        
        try: 
            data = json.loads(request.body)
            email = data['email']
            password = data['password']
            user = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            access_token = jwt.encode({'user_id':user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

            return JsonResponse({'message':'SUCCESS', 'access_token':access_token}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message':'USER_DOES_NOT_EXISTS'}, status=401)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)