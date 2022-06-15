from . import models, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import Permission
from rest_framework import status
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser 
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.sessions.models import Session
from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType



class UserView:

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get(request, id):

        user = request.user
        is_superuser = user.is_superuser
        is_staff = user.is_staff
        can_view_customuser = user.has_perm('account.view_customuser')

        if (user.pk != id) and (not is_superuser or not is_staff or not can_view_customuser):
            return Response({
                'detail': 'You do not have permission to peform this action.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            data = models.CustomUser.objects.get(pk=id)
            serializer = serializers.UserDetailSerializer(data, many=False)
        
            return Response({
                'message': 'Success!',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'message': '404 Not Found, ' + f'{str(e)}',
            }, status=status.HTTP_404_NOT_FOUND)
        
    
    @api_view(['GET'])
    @permission_classes([IsAuthenticated, IsAdminUser])
    def list(request):

        data = models.CustomUser.objects.exclude(pk=1)
        serializer = serializers.UserDetailSerializer(data, many=True)
        total_users = len(serializer.data)
       
        return Response({
            'message': 'Success!, ' + f'{total_users}' + ' user(s) found.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    
    @api_view(['POST'])
    @permission_classes([IsAuthenticated, IsAdminUser])
    def create(request):

        is_email = models.CustomUser.objects.filter(email=request.data['email'])

        if is_email.exists():
            return Response({
                'message': 'Email is already taken, please enter a different email address.',
                'data': request.data
            }, status=status.HTTP_409_CONFLICT)
       
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User added successfully!',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['POST'])
    def login_user(request):

        email = request.data['email']
        password = request.data['password']
        
        user = authenticate(request, username=email, password=password)
    
        if user is not None:

            login(request, user)

            try:
                token = Token.objects.get(user=user)
            except: 
                token = Token.objects.create(user=user)

            user.last_login = timezone.now()
            user.save(update_fields=['last_login',])

            return Response({
                'message': 'Login Success!',
                'data': {
                    'token': 'Token ' + f'{str(token)}'
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'message': 'Invalid username or password.' 
        }, status=status.HTTP_404_NOT_FOUND)    

    @api_view(['PATCH'])
    @permission_classes([IsAuthenticated, IsAdminUser])
    def update(request, id):

        user = request.user
        is_staff = user.is_staff
        is_superuser = user.is_superuser
        email = request.data['email']
        can_view_customuser = user.has_perm('account.view_customuser')

        if id == 1 and not is_superuser:
            return Response({
                'detail': 'You do not have permission to perform this action.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        if (user.pk != id) and (not is_superuser or not is_staff or not can_view_customuser):
            return Response({
                'detail': 'You do not have permission to peform this action.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        if models.CustomUser.objects.filter(~Q(pk=id) & Q(email=email)).exists():
            return Response({
                'message': 'Email is already taken, please enter a different email address.',
                'data': request.data
            }, status=status.HTTP_409_CONFLICT)

        instance = models.CustomUser.objects.get(pk=id) 
        serializer = serializers.UserUpdateSerializer(instance, data=request.data)            
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Updated Successful!',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'message': '400 Bad Request.'
        }, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['DELETE'])
    def logout_user(request):

        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        
        logout(request)

        return Response({
            'message': 'You are logged out.'
        }, status=status.HTTP_200_OK)

    @api_view(['POST'])
    @permission_classes([IsAuthenticated, IsAdminUser])
    def add_permission(request):

        user_id = request.data['id']
        user = request.user
        permission_list = request.data['permission_list']

        if user_id == 1 or not user.has_perm('account.add_permission'):
            return Response({
                'detail': 'You do not have permission to peform this action.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        user = models.CustomUser.objects.get(pk=user_id)
        content_type = ContentType.objects.get_for_model(models.CustomUser)

        added_permissions = []

        for perm in permission_list:        
            try:
                permission = Permission.objects.get(
                    codename=perm,
                    content_type=content_type,
                )
                user.user_permissions.add(permission)
                added_permissions.append(perm)
            except:
                pass

        return Response({
            'message': 'Permission(s) ' + f'{added_permissions}' + ' Added Successfully'
        }, status=status.HTTP_200_OK)
