from rest_framework import serializers
from . import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView."""

    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
	""" A serializer for our user profiles objects. """
	class Meta:
		model = models.UserProfile
		fields = ('id', 'email', 'name', 'password')
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		"""Create and return a new user."""
		user = models.UserProfile(
			email = validated_data['email'],
			name = validated_data['name']
			)
		user.set_password(validated_data['password'])
		user.save()

		return user
	def update(self, instance, validated_data):
		for attr, value in validated_data.items():
			if attr == 'password':
				instance.set_password(value)
			else:
				setattr(instance, attr, value)
		instance.save()
		return instance


class PostSerializer(serializers.ModelSerializer):
	"""A serializer for post."""
	class Meta:
		model = models.Post
		fields = ('id', 'user_profile','title','description','created_at','updated_at')
		extra_kwargs = {'user_profile':{'read_only':True}}
		

class ReviewSerializer(serializers.ModelSerializer):
	"""A serializer for post."""
	class Meta:
		model = models.Review
		fields = ('id', 'user_profile','post_id','description','created_at','updated_at')
		extra_kwargs = {'user_profile':{'read_only':True}}