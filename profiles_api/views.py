from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from . import models
from . import permissions
from . import serializers
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError



# Create your views here.

class HelloApiView(APIView):
    """Test API View."""
    serializers_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features."""
        an_apiview = [
            'User HTTP methods as function (get, post, patch, put delete)',
            'It is similar to a traditional Django view',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message':'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a Hello Message with our name."""
        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handles updating an object."""
        return Response({'method':'put'})

    def patch(self, request, pk=None):
        """Patch request, only updates fields provided in the request."""

        return Response({'method':'patch'})

    def delete(self, request, pk=None):
        """Deletes an object."""

        return Response({'method':'delete'})

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet."""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message."""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code.'
        ]

        return Response({'message':'Hello!', 'a_viewset':a_viewset})

    def create(self, request):
        """Create a new hello message."""
        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        """Handles getting any object by its ID."""
        return Response({'http_method':'GET'})

    def update(self, request, pk=None):
        """Handles updating an object."""

        return Response({'http_method':'PUT'})

    def partial_update(self, request, pk=None):
        """Handles updating part of an object. """
        return Response({'http_method':'PATCH'})
    def destroy(self, request, pk=None):
        """Handles removing an object."""
        return Response({'http_method':"DELETE"})



class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profiles."""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token."""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token."""

        return ObtainAuthToken().post(request)

class PostViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and upating post feed items."""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.PostSerializer
    queryset = models.Post.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""
        serializer.save(user_profile=self.request.user)

class ReviewViewSet(viewsets.ViewSet):
    """Handles creating, reading and upating Review items."""
    serializer_class = serializers.ReviewSerializer
    authentication_classes = (TokenAuthentication,)
    
    def get_permissions(self):
        if self.action in ('list','create', None):
            permission_classes = (permissions.ReviewPostPer, IsAuthenticatedOrReadOnly)
        else:
            permission_classes = (permissions.PostOwnStatus,permissions.ReviewPostPer, permissions.ReviewPer, IsAuthenticatedOrReadOnly)

        return [permission() for permission in permission_classes]


    def list(self, request, pid):
        queryset = models.Review.objects.filter(post_id=pid)
        serializer = serializers.ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request,pid):
        """Create a new hello message."""
        serializer = serializers.ReviewSerializer(data=request.data)

        if serializer.is_valid():
            try:
                post  = models.Post.objects.get(id = pid)
            except ObjectDoesNotExist:
                return Response({'message': 'Post does not exist'})
            try:
                serializer.save(post_id=post,user_profile=self.request.user)
                return Response(serializer.data)
            except IntegrityError:
                return Response({'message': 'You can not review more than once'})

            
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request,pid, pk=None):
        """Handles getting any object by its ID."""
        query = models.Review.objects.get(post_id=pid, pk=pk)
        serializer = serializers.ReviewSerializer(query)
        return Response(serializer.data)
            

    def update(self, request, pid, pk=None):

        query = models.Review.objects.get(post_id=pid, pk=pk)
        serializer = serializers.ReviewSerializer(query,data=request.data)
        if serializer.is_valid():
            try:
                post  = models.Post.objects.get(id = pid)
            except ObjectDoesNotExist:
                return Response({'message': 'Post does not exist'})
            serializer.save(post_id=post,user_profile=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

    def partial_update(self, request,pid, pk=None):

        query = models.Review.objects.get(post_id=pid, pk=pk)
        serializer = serializers.ReviewSerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                post  = models.Post.objects.get(id = pid)
            except ObjectDoesNotExist:
                return Response({'message': 'Post does not exist'})
            serializer.save(post_id=post,user_profile=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

    def destroy(self, request, pid, pk=None):
        
        query = models.Review.objects.get(post_id=pid, pk=pk)
        query.delete()
        return Response({'message':'object deleted'})
        

