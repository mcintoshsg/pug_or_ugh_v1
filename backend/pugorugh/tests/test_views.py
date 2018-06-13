
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from pugorugh.models import Dog, UserDog, UserPref


class BaseTestCase(APITestCase):
    '''SETUP '''
    def setUp(self):
        self.client = APIClient()

        ''' create users to be used in our dummy data '''
        self.user_1 = User.objects.create(
                                    username='test_user_1',
                                    email='test_user_1@example.com',
                                    password='password'
                                    )
        self.user1_token = Token.objects.create(user=self.user_1)

        self.user_2 = User.objects.create(
                                    username='test_user_2',
                                    email='test_user_2@example.com',
                                    password='password'
                                    )
        self.user2_token = Token.objects.create(user=self.user_2)

        ''' setup up dummy data for the Dog model '''
        dog_1 = {
                'name': 'dog_1',
                'image_filename': '1.jpg',
                'breed': 'mutt',
                'age': 12,
                'gender': 'm',
                'size': 'm'
        }

        dog_2 = {
                'name': 'dog_2',
                'image_filename': '2.jpg',
                'breed': 'mutt',
                'age': 48,
                'gender': 'f',
                'size': 'l'
        }
        self.dog_1 = Dog.objects.create(**dog_1)
        self.dog_2 = Dog.objects.create(**dog_2)

        ''' set up dummy data for UserPerf Model '''
        user_pref_1 = {
                        'user': self.user_1,
                        'age': 'b,y',
                        'gender': 'm,f',
                        'size': 'l, xl'
                        }

        user_pref_2 = {
                        'user': self.user_2,
                        'age': 'a,s',
                        'gender': 'm',
                        'size': 's, m'
                        }

        self.user_pref_1 = UserPref.objects.create(**user_pref_1)
        self.user_pref_2 = UserPref.objects.create(**user_pref_2)

        ''' setup up dummy data for the UserDog model '''
        user_dog_1 = {
                        'user': self.user_1,
                        'dog': self.dog_1,
                        'status': 'd'
                        }

        user_dog_2 = {
                        'user': self.user_2,
                        'dog': self.dog_2,
                        'status': 'l'
                        }

        self.user_dog_1 = UserDog.objects.create(**user_dog_1)
        self.user_dog_2 = UserDog.objects.create(**user_dog_2)


# url : /api/user/
class UserViewsTests(BaseTestCase):
    def test_register_bad_user(self):
        response = self.client.post('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)                           

    def test_register_good_user(self):
        response = self.client.post('/api/user/',
                                    {'username': 'test',
                                        'password': 'password'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'test')
        self.assertEqual(response.data['is_active'], True)

    def test_login_bad_user(self):
        response = self.client.post('/api/user/login/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)                        

    def test_login_good_user(self):
        response = self.client.post('/api/user/',
                                    {'username': 'test',
                                        'password': 'password'})

        self.user_token = Token.objects.get(user__username='test')
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user_token.key
            )

        response = self.client.post('/api/user/login/',
                                    {'username': 'test',
                                        'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(self.user_token.key, response.data['token'])


# url : /api/user/prefernces/
class UserPrefViewTests(BaseTestCase):
    ''' test the retreval of the user prefernences '''

    def test_get_user_prefernces(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user1_token.key
            )
        response = self.client.get('/api/user/preferences/')
        self.assertEqual(response.data['age'], 'b,y')

    def test_put_user_preferences(self):
        data = {'size': 's,m,l'}
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user1_token.key
            )
        response = self.client.put('/api/user/preferences/', data=data)
        self.assertEqual(response.data['size'], 's,m,l')

# url : /api/dog/-?<pk>/<ldu_decision>/next?/
class LDUDogViewTests(BaseTestCase):
    ''' test the retreval of the liked dogs '''

    def test_get_liked_dogs(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user2_token.key
            )
        response = self.client.get('/api/dog/-1/liked/next/')
        self.assertEqual(response.data['name'], self.dog_2.name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_disliked_dogs(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user1_token.key
            )
        response = self.client.get('/api/dog/-1/disliked/next/')
        self.assertEqual(response.data['name'], self.dog_1.name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pk_bad(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user1_token.key
            )
        response = self.client.get('/api/dog/22/disliked/next/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_staus_bad(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user2_token.key
            )
        response = self.client.get('/api/dog/-1/undecided/next/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_status(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user1_token.key
            )
        response = self.client.put('/api/dog/1/liked/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(self.dog_1.userdog__status, 'l')
        # print(self.user_dog_1.status)
