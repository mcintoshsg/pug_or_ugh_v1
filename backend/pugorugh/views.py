from functools import reduce
import operator

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

from rest_framework import generics, status, views
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from . import models
from . import serializers

import pdb

class UserRegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class ListCreateDogView(generics.ListCreateAPIView):
    ''' lists out all dogs in the Dog model and gives 
        the user, if authorised, the ability to create 
        a new Doggie
    ''' 
    queryset = models.Dog.objects.all() 
    serializer_class = serializers.DogSerializer


class RetrieveUpdateDestroyDogView(generics.RetrieveUpdateDestroyAPIView):
    ''' this class expects a primary key of the Dog in the URL. 
        Allows the ability to get, update and destroy a single 
        record in our Dog model 
    '''     
    queryset = models.Dog.objects.all() 
    serializer_class = serializers.DogSerializer


class RetrieveUpdateUserPrefView(generics.RetrieveUpdateAPIView):
    ''' Retrieve update the logged in user preferences.
    '''
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        ''' override the queryset with the logged in users
            prefs 
        '''
        return self.get_queryset().get(user=self.request.user)

    def put(self, *args, **kwargs):
        ''' override the put request - the reason being is that
            on the first pass we can create all the undecdeid dogs
            for the newly registered user to view
        '''
        # firstly lets get if the current userprefs exist.
        try:
            userprefs = self.get_queryset().get(user=self.request.user)
            for key, value in self.request.data.items():
                setattr(userprefs, key, value)
            userprefs.save()
        except models.UserPref.DoesNotExist:
            new_values = self.request.data
            userprefs = models.UserPref(**new_values)
            userprefs.save()

        # secondly take the opportunity to update all dogs that
        # match the new userprefs with an undecided status
        qs = self.build_queryset(self.request.user)

        # get all the dogs that we are going to filter against      
        all_dogs = models.Dog.objects.filter(reduce(operator.or_, qs))

        # give each of the dog in the queryset an value of undecided
        for dog in all_dogs:
            d = models.UserDog.objects.create(
                                user=self.request.user, 
                                dog=dog, status='u'
                                )
            d.save()

        serializer = serializers.UserPrefSerializer()
        return Response(serializer.data)


    def build_queryset(self, user):
        ''' dynamically create a queryset to use '''
        age_filters = {}
        age_range = {'b': (0, 6), 'y': (6, 48),  # arbitary ages of dogs
                        'a': (48, 84), 's': (84, 240)}
        reg_user_prefs = models.UserPref.objects.get(user=user)
        
        # part 1 build the query based on size and gender
        g_s_query = (Q(gender__in=reg_user_prefs.gender) &
                    Q(size__in=reg_user_prefs.size))
        
        # part 2 build the query based on age
        ages = reg_user_prefs.age.split(',')
        for a in ages:
            a = a.strip() # this ugly should do a pre-save on model
            if a in age_range.keys():
                age_filters.update({a:age_range[a]})

        # part 3 combine the 2 queries
        query = ([Q(age__range=value) for value in age_filters.values()])
        query.append(g_s_query)
        return query  
    

class RetrieveUpdateLDUDogView(views.APIView):
    ''' Retrieve doggies liked, disliked or undecided based on 
        the logged in user preferences.
    '''
    # queryset = models.Dog.objects.all()
    # serializer_class = serializers.DogSerializer

    def get(self, *args, **kwargs):
        ''' Filter and return a single Doogie base on the incoming url or
            incoming argument of liked, disliked, undecided and the asscocitaed
            pk - which is the record in the table -1 being the first, 1 being 
            the second
        '''
        like_dislike_undecided = self.kwargs.get('ldu_decision')[:1]
        status_data = models.Dog.objects.all().filter(
                                userdog__user=self.request.user,
                                userdog__status=like_dislike_undecided
                                )
        if status_data:
            if self.kwargs.get('pk') == '-1':
                serializer = serializers.DogSerializer(status_data[0])
                return Response(serializer.data)
            else:    
                try:
                    user_dog = status_data[int(self.kwargs.get('pk'))]
                except IndexError:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                serializer = serializers.DogSerializer(user_dog)
                return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)    

    def put(self, *args, **kwargs):
        ''' PUT updated statuses for dogs 
        '''
        like_dislike_undecided = self.kwargs.get('ldu_decision')[:1]
        pk = int(self.kwargs.get('pk'))
        try:
            user_dog = models.UserDog.objects.get(id=pk)
        except ObjectDoesNotExist:
            Response(status=status.HTTP_404_NOT_FOUND)    
        else:
            user_dog.status = like_dislike_undecided
            user_dog.save()
        
        updated_dog = get_object_or_404(models.Dog, pk=pk)
        serializer = serializers.DogSerializer(updated_dog)
        return Response(serializer.data)
        