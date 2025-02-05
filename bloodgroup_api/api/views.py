from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import BloodGroup, UserProfile
from .serializers import BloodGroupSerializer, UserSerializer, UserProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id, 'email': user.email}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      

class BloodGroupViewSet(viewsets.ModelViewSet):
    queryset = BloodGroup.objects.all()
    serializer_class = BloodGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        blood_group = request.query_params.get('blood_group', '')
        area = request.query_params.get('area', '')
        phone = request.query_params.get('phone', '')

        queryset = UserProfile.objects.all()
        if query:
            queryset = queryset.filter(user__username__icontains=query)
        if blood_group:
            queryset = queryset.filter(blood_group__name__iexact=blood_group)
        if area:
            queryset = queryset.filter(area__icontains=area)
        if phone:
            queryset = queryset.filter(phone__icontains=phone)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'search']:
            permission_classes = [permissions.isAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]