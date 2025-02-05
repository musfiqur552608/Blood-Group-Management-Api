from rest_framework import serializers  
from django.contrib.auth.models import User
from .models import BloodGroup, UserProfile


class BloodGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodGroup
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','email','password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    blood_group = BloodGroupSerializer(read_only=True)
    blood_group_id = serializers.PrimaryKeyRelatedField(queryset=BloodGroup.objects.all(), source='blood_group', write_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'blood_group', 'blood_group_id', 'area', 'phone']

        

