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

