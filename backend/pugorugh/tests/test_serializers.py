from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from pugorugh.serializers import (DogSerializer, UserPrefSerializer)


class DogSerializerTests(APITestCase):
    '''SETUP '''
    def setUp(self):

        ''' setup up dummy data for the Dog serializer '''
        self.dog_1_data = {
                'name': 'dog_1',
                'image_filename': '1.jpg',
                'breed': 'mutt',
                'age': 12,
                'gender': 'm',
                'size': 'm'
        }

    def test_get_correct_value(self):
        serializer = DogSerializer(data=self.dog_1_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
                        serializer.data['name'],
                        self.dog_1_data['name']
                        )


class UserPrefSerializerTests(APITestCase):
    '''SETUP '''
    def setUp(self):

        ''' create user to be used in our dummy data '''
        self.user_1 = User.objects.create(
                                    username='test_user_1',
                                    email='test_user_1@example.com',
                                    password='password'
                                    )

        ''' set up dummy data for UserPerf Serializer '''
        self.user_pref_1 = {
                        'user': self.user_1,
                        'age': 'b,y',
                        'gender': 'm,f',
                        'size': 'l, xl'
                        }

    def test_validate_userpref_bad_age(self):
        self.user_pref_1['age'] = 'z'
        serializer = UserPrefSerializer(data=self.user_pref_1)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['age']))

    def test_validate_userpref_good_age(self):
        self.user_pref_1['age'] = 's'
        serializer = UserPrefSerializer(data=self.user_pref_1)
        self.assertTrue(serializer.is_valid())

    def test_validate_userpref_bad_gender(self):
        self.user_pref_1['gender'] = 'z'
        serializer = UserPrefSerializer(data=self.user_pref_1)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['gender']))

    def test_validate_userpref_good_gender(self):
        self.user_pref_1['gender'] = 'm'
        serializer = UserPrefSerializer(data=self.user_pref_1)
        self.assertTrue(serializer.is_valid())

    def test_validate_userpref_bad_size(self):
        self.user_pref_1['size'] = 'z'
        serializer = UserPrefSerializer(data=self.user_pref_1)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['size']))

    def test_validate_userpref_good_size(self):
        self.user_pref_1['gender'] = 'm'
        serializer = UserPrefSerializer(data=self.user_pref_1)
        self.assertTrue(serializer.is_valid())
