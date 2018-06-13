from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    name = models.CharField(max_length=100)
    image_filename = models.CharField(max_length=255, blank=True)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(
        max_length=1,
        help_text='gender; Enetr, (m) Male, (f) Female, (u) Unknown'
        )
    size = models.CharField(
        max_length=2,
        help_text=(
                    'size; Enter, (s) Small, (m) Medium, (l) Large,'
                    '(xl) Extra Large'
        ))

    def __str__(self):
        return self.name


class UserDog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1,
        help_text='status; Enter, (l) Liked, (d) Disliked, (u) Undecided'
        )

    def __str__(self):
        return self.user.username + ' ' + self.dog.name


class UserPref(models.Model):
    ''' this needs to fixed max_lenght is too much, need to strip blanks
    use signals pre_save()
    '''    
    user = models.OneToOneField(User,
                                related_name='preferences',
                                on_delete=models.CASCADE,
                                help_text=(
                                            'Can only have one set of'
                                            'prefrences per user'),
                                null=True
                                )
    age = models.CharField(
        max_length=10,
        help_text=(
                    'age; Enter, (b) Baby, (y) Young, (a) Adult,'
                    ' (s) Senior or a combaination seperated by a comma.')
    )
    gender = models.CharField(
        max_length=10,
        help_text=(
                    'gender; Enter, (m) Male, (f) Female,'
                    ' (s) Senior or a combaination seperated by a comma.'
                    )
    )                    
    size = models.CharField(
        max_length=10,
        help_text=(
                    'size; Enter, (s) Small, (m) Medium, (l) Large,'
                    '(xl) Extra Large or a combination seperated by a comma.'
                    )
    )

    def __str__(self):
        return (self.user.username + ' ages ({0.age}),'
                ' genders ({0.gender}), sizes ({0.size})'.format(self))

