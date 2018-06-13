from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token 
from rest_framework import serializers


from . import models
import pdb


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()

        # create an initial set of preferences for the
        self.create_inital_preferences(user)

        # create a new token for the newly registered user
        self.create_user_token(user)

        return user

    def create_inital_preferences(self, user):
        ''' creates an inital set of preferences
            for the newly registered user
        '''
        inital_prefs = models.UserPref(
            user=user,
            age='b,y,a,s',
            gender='m,f',
            size='s,m,l,xl'
        )
        inital_prefs.save()

    def create_user_token(self, user):
        ''' creates a new token for the newly registered user
        '''
        new_token = Token(user=user)
        new_token.save()

    class Meta:
        fields = '__all__'
        model = get_user_model()


class DogSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'name',
            'image_filename',
            'breed',
            'age',
            'gender',
            'size',
        )
        model = models.Dog


class UserPrefSerializer(serializers.ModelSerializer):

    def get_validated_values(self, valid_entries, values, err_msg):
        # pdb.set_trace()
        values = values.replace(' ', '')
        for entry in values.split(','):
            if entry not in valid_entries:
                raise serializers.ValidationError(err_msg)
        return values

    def validate_age(self, value):
        valid_entries = ['b', 'y', 'a', 's']
        err_msg = (
                    'Age must be (b) Baby, (y) Young, (a) Adult,' 
                    ' (s) Senior or a combaination seperated by a comma.'
                    )
        return(self.get_validated_values(valid_entries, value, err_msg))

    def validate_gender(self, value):
        valid_entries = ['m', 'f']
        err_msg = (
                    'Gender must be (m) Male, (f) Female,'
                    'or a combaination seperated by a comma.'
                    )
        return(self.get_validated_values(valid_entries, value, err_msg))

    def validate_size(self, value):
        valid_entries = ['s', 'm', 'l', 'xl']
        err_msg = (
                    'Size must be  (s) Small, (m) Medium, (l) Large, '
                    '(xl) Extra Large  or a combination seperated '
                    'by a comma.'
                    )
        return(self.get_validated_values(valid_entries, value, err_msg))

    class Meta:
        fields = (
            'age',
            'gender',
            'size',
        )
        model = models.UserPref
