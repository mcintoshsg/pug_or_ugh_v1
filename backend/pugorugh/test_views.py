from django.contrib.auth.models import User
from django.test import TestCase

from pugorugh.models import Dog, UserDog, UserPref
from pugorugh.views import (UserRegisterView, 
                                ListCreateDogView, 
                                RetrieveUpdateDestroyDogView,
                                RetrieveUpdateUserPrefView,
                                RetrieveUpdateLDUDogView,
                                )

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
