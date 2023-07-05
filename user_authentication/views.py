from django.contrib.auth.hashers import check_password

from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Session
from django.utils import timezone
from datetime import timedelta

@api_view(['POST'])
def user_register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    full_name = request.data.get('full_name')
    phone_number = request.data.get('phone_number')
    organization = request.data.get('organization')
    role = request.data.get('role')
    
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'User with this email already exists.'}, status=400)

    user = User(
        email=email, 
        full_name=full_name, 
        phone_number=phone_number, 
        organization=organization, 
        role=role
    )
    user.set_password(password)
    user.save()

    return JsonResponse({'message': 'User created successfully.'}, status=201)

@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.filter(email=email).first()

    if user is None:
        return Response('User not found', status=404)

    if not check_password(password, user.password):
        return Response('Wrong password', status=400)

    refresh = RefreshToken.for_user(user)
    
    # Create session
    session = Session(user=user)
    session.save()
    
    res = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    return JsonResponse(res)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    user = request.user
    # Update session
    session = Session.objects.filter(user=user).order_by('-start_time').first()
    if session:
        session.end_time = timezone.now()
        session.duration = session.end_time - session.start_time
        session.save()
    return Response('Logout successful', status=200)

