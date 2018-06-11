from django.contrib.auth.models import User
from django.test import TestCase

from pugorugh.models import Dog, UserDog, UserPref

# 2. Test get all dogs
# 3. Test get single dog
# 4. Test delete single dog
# 5. Test update single dog
# 6. Test create user preferences
# 7. Test get user preferences
# 8. Test update user preferences
# 9. Test update new user prefernces - updates all dogs that match with U
# 10. Test validiators - bad entries
# 11. Test get all liked dogs
# 12. Test get all unliked dogs
# 13. Test get all undecided dogs
# 14. Test iterate through next like or disliked or undecided
# 15. Test new user creation - token creates
# 16. Test the URLS

###### test data for the dogs model ######
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

# create a base modeltest case the models
class ModelsBaseTestCase(TestCase):
    def setUp(self):
        ''' setup up dummy data for the Dog model '''
        self.dog_1 = Dog.objects.create(**dog_1)
        self.dog_2 = Dog.objects.create(**dog_2) 


    def tearDown(self):
        pass

class UserModelTestCase(ModelsBaseTestCase):
    ''' test cases for the user model '''
   
    @staticmethod
    def create_test_users(count=2):
        ''' this test creates 2 users in the database via a function called
        '''
        for i in range(count):
            User.objects.create(
                username='user_{}'.format(i),
                email='test_{}@example.com'.format(i),
                password='password'
            )

    def test_create_user(self):
        ''' test the creation of the user '''
        self.create_test_users()
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=1).password,'password')
            

class DogModelTests(ModelsBaseTestCase):
    ''' testing of the Dog model '''
    def test_dog_creation(self):
        ''' test out the creation of our model '''
        balto = Dog.objects.get(name="dog_1")
        self.assertEqual(balto, self.dog_1)
        alfie = Dog.objects.get(name="dog_2")
        self.assertEqual(alfie, self.dog_2)


class UserDogModelTests(ModelsBaseTestCase):
    ''' testing of the UserDog model '''
  
    def create_user_dogs(self):
        UserModelTestCase.create_test_users(2)
        self.user_1 = User.objects.get(id=1)
        self.user_2 = User.objects.get(id=2)
        UserDog.objects.create(user=self.user_1, dog=self.dog_1, status='u')
        UserDog.objects.create(user=self.user_1, dog=self.dog_2, status='u')
        UserDog.objects.create(user=self.user_2, dog=self.dog_1, status='u')
        UserDog.objects.create(user=self.user_2, dog=self.dog_2, status='u')
     
    def test_user_dog_creation(self):
        ''' test the creation of userdogs '''
        self.create_user_dogs()
        self.assertEqual(UserDog.objects.count(), 4)
        self.assertEqual(UserDog.objects.get(id=1).user, self.user_1)
        self.assertEqual(UserDog.objects.get(id=1).status, 'u')
    

class UserPrefModelTests(ModelsBaseTestCase):
    ''' testing of the UserDog model '''
  
    def create_user_prefs(self):
        UserModelTestCase.create_test_users(1)
        self.user_1 = User.objects.get(id=1)
        UserPref.objects.create(user=self.user_1,
                                age='b,y',
                                gender='m,f',
                                size='l,xl'
                                )
     
    def test_user_dog_creation(self):
        ''' test the creation of userdogs '''
        self.create_user_prefs()
        self.assertEqual(UserPref.objects.count(), 1)
        self.assertEqual(UserPref.objects.get(id=1).user, self.user_1)
        self.assertEqual(UserPref.objects.get(id=1).gender, 'm,f')
        
