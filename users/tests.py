import jwt, bcrypt, json

from django.test     import Client, TestCase
from django.conf     import settings

from users.models import User

class SignupTest(TestCase):
    def setUp(self):
        User.objects.create(
            id = 1,
            email = 'test@velog.io',
            password = 'abcd1234!',
            nickname = 'test'
        )

    def tearDown(self) :
        User.objects.all().delete()
    #성공
    def test_SignupView_post_success(self):
        client = Client()
        user = {
            'email'     : 'fore0919@velog.io',
            'password'  : 'abcd1234!',
            'nickname'  : '포레'          
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.json(), {'message':'SUCCESS'})
        self.assertEqual(response.status_code,201)
    # 실패 - 유효하지 않은 이메일 형식
    def test_SignupView_post_success(self):
        client = Client()
        user = {
            'email'     : 'fore0919',
            'password'  : 'abcd1234!',
            'nickname'  : '포레'          
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.json(), {'message':'EMAIL_VALIDATION_ERROR'})
        self.assertEqual(response.status_code,400)
    # 실패 - 유효하지 않은 비밀번호 형식
    def test_SignupView_post_success(self):
        client = Client()
        user = {
            'email'     : 'fore0919@velog.io',
            'password'  : '1234',
            'nickname'  : '포레'          
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.json(), {'message':'PW_VALIDATION_ERROR'})
        self.assertEqual(response.status_code,400)    
    # 실패 - 이미 가입된 회원
    def test_SignupView_post_success(self):
        client = Client()
        user = {
            'email'     : 'test@velog.io',
            'password'  : 'abcd1234!',
            'nickname'  : '포레'          
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.json(), {'message':'ALREADY_EXISTS_EMAIL'})
        self.assertEqual(response.status_code,409)    
    # 실패 - 이메일 or 비밀번호 미입력
    def test_SignupView_post_success(self):
        client = Client()
        user = {
            'emai'     : 'fore0919@velog.io',
            'nickname'  : '포레'          
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})
        self.assertEqual(response.status_code,400)    

class LoginTest(TestCase):
    def setUp(self):
        User.objects.create(
            id = 1,
            email = 'test@velog.io',
            password = bcrypt.hashpw('abcd1234!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            nickname = 'test',
        )

    def tearDown(self) :
        User.objects.all().delete()
    #성공
    def test_LoginView_post_success(self):
        client = Client()

        user    = {
            'email'    : 'test@velog.io',
            'password' : 'abcd1234!',
        }

        response = client.post('/users/login', json.dumps(user), content_type = 'application/json')
        access_token = jwt.encode({'user_id':1}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
                'message':'SUCCESS',
                'access_token':access_token
        })
    #실패 - 틀린 비밀번호 입력
    def test_LoginView_post_success(self):
        client = Client()

        user    = {
            'email'    : 'test@velog.io',
            'password' : 'abcd1234',
        }

        response = client.post('/users/login', json.dumps(user), content_type = 'application/json')
        access_token = jwt.encode({'user_id':1}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message':'INVALID_USER'})
    #실패 - 이메일 or 비밀번호 미입력
    def test_LoginView_post_success(self):
        client = Client()

        user    = {
            'email'    : 'test@velog.io',
        }

        response = client.post('/users/login', json.dumps(user), content_type = 'application/json')
        access_token = jwt.encode({'user_id':1}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})
    #실패 - 존재하지 않는 회원 
    def test_LoginView_post_success(self):
        client = Client()

        user    = {
            'email'    : 'test@velog',
            'password' : 'abcd1234',
        }

        response = client.post('/users/login', json.dumps(user), content_type = 'application/json')
        access_token = jwt.encode({'user_id':1}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message':'USER_DOES_NOT_EXISTS'})
