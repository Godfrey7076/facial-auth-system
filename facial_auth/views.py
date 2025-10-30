from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from .models import UserProfile, SecurityArea, AccessLog, VisitorLog, SystemSettings
from .serializers import (
    UserProfileSerializer, AccessLogSerializer, VisitorLogSerializer,
    FaceRegistrationSerializer, AuthenticationSerializer, AdminUserCreateSerializer,
    SecurityAreaSerializer
)
from .utils.face_recognition import face_recognition
import json


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """API root endpoint with available endpoints"""
    return Response({
        'message': 'Security Pass Management System API',
        'system': 'High Security Area Access Control',
        'endpoints': {
            'register': '/api/register/',
            'authenticate': '/api/authenticate/',
            'capture_face': '/api/capture-face/',
            'profile': '/api/profile/',
            'access_logs': '/api/access-logs/',
            'visitor_logs': '/api/visitor-logs/',
            'security_areas': '/api/security-areas/',
        },
        'authentication_required': {
            'profile': True,
            'access_logs': True,
            'visitor_logs': True,
            'register': False,
            'authenticate': False,
            'capture_face': False,
            'security_areas': False
        }
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register new user with facial recognition and pass details"""
    serializer = FaceRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data['username']
        security_number = serializer.validated_data['security_number']
        face_data = serializer.validated_data['face_data']
        user_type = serializer.validated_data['user_type']
        access_level = serializer.validated_data['access_level']
        pass_duration_days = serializer.validated_data['pass_duration_days']

        # Check if username or security number already exists
        if User.objects.filter(username=username).exists():
            return Response({
                'error': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        if UserProfile.objects.filter(security_number=security_number).exists():
            return Response({
                'error': 'Security number already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        user = User.objects.create_user(
            username=username,
            password=security_number
        )

        # Calculate pass expiry
        pass_expires = datetime.now() + timedelta(days=pass_duration_days)

        # Create user profile with enhanced details
        user_profile = UserProfile.objects.create(
            user=user,
            security_number=security_number,
            user_type=user_type,
            access_level=access_level,
            face_encoding=json.dumps(face_data),
            pass_expires=pass_expires,
            is_verified=True
        )

        return Response({
            'message': 'User registered successfully',
            'user_id': user.id,
            'profile_id': user_profile.id,
            'pass_expires': pass_expires,
            'access_level': access_level
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def authenticate_user(request):
    """Authenticate user and log access attempt"""
    serializer = AuthenticationSerializer(data=request.data)

    if serializer.is_valid():
        security_number = serializer.validated_data['security_number']
        face_data = serializer.validated_data['face_data']
        security_area_id = serializer.validated_data.get('security_area_id')

        try:
            user_profile = UserProfile.objects.get(
                security_number=security_number)
            user = user_profile.user

            # Check if pass is valid
            if not user_profile.is_pass_valid():
                AccessLog.objects.create(
                    user=user,
                    security_area=SecurityArea.objects.first(
                    ) if not security_area_id else SecurityArea.objects.get(id=security_area_id),
                    access_granted=False,
                    reason_denied="Pass expired or inactive",
                    authentication_method='both'
                )
                return Response({
                    'error': 'Access denied - Pass expired or inactive'
                }, status=status.HTTP_403_FORBIDDEN)

            # Verify face
            stored_encoding = json.loads(user_profile.face_encoding)
            face_match, similarity = face_recognition.verify_face(
                stored_encoding, face_data)

            if face_match:
                # Check area access if specified
                security_area = None
                if security_area_id:
                    try:
                        security_area = SecurityArea.objects.get(
                            id=security_area_id)
                        if security_area.access_level > user_profile.access_level:
                            AccessLog.objects.create(
                                user=user,
                                security_area=security_area,
                                access_granted=False,
                                reason_denied="Insufficient access level",
                                authentication_method='both'
                            )
                            return Response({
                                'error': f'Access denied - Insufficient clearance for {security_area.name}'
                            }, status=status.HTTP_403_FORBIDDEN)
                    except SecurityArea.DoesNotExist:
                        pass

                # Authenticate user
                user = authenticate(username=user.username,
                                    password=security_number)

                if user is not None:
                    login(request, user)

                    # Log successful access
                    AccessLog.objects.create(
                        user=user,
                        security_area=security_area or SecurityArea.objects.first(),
                        access_granted=True,
                        authentication_method='both'
                    )

                    return Response({
                        'message': 'Authentication successful',
                        'user_id': user.id,
                        'username': user.username,
                        'user_type': user_profile.user_type,
                        'access_level': user_profile.access_level,
                        'similarity_score': float(similarity),
                        'pass_expires': user_profile.pass_expires
                    }, status=status.HTTP_200_OK)

            # Log failed authentication
            AccessLog.objects.create(
                user=user,
                security_area=SecurityArea.objects.first(
                ) if not security_area_id else SecurityArea.objects.get(id=security_area_id),
                access_granted=False,
                reason_denied="Face recognition failed",
                authentication_method='both'
            )

            return Response({
                'error': 'Authentication failed - Face not recognized',
                'similarity_score': float(similarity)
            }, status=status.HTTP_401_UNAUTHORIZED)

        except UserProfile.DoesNotExist:
            return Response({
                'error': 'Invalid security number'
            }, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def capture_face_encoding(request):
    """Capture face encoding from webcam"""
    try:
        face_encoding = face_recognition.capture_face_encoding()

        if face_encoding:
            return Response({
                'face_encoding': face_encoding,
                'message': 'Face captured successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Face capture cancelled or failed'
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            'error': f'Face capture error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Get current user's profile"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response({
            'error': 'Profile not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_access_logs(request):
    """Get access logs for current user"""
    logs = AccessLog.objects.filter(user=request.user)
    serializer = AccessLogSerializer(logs, many=True)
    return Response({
        'total_entries': logs.count(),
        'access_logs': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_visitor_logs(request):
    """Get visitor logs for current user"""
    logs = VisitorLog.objects.filter(user=request.user)
    serializer = VisitorLogSerializer(logs, many=True)
    return Response({
        'total_visits': logs.count(),
        'visitor_logs': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_security_areas(request):
    """Get list of all security areas"""
    areas = SecurityArea.objects.filter(is_active=True)
    serializer = SecurityAreaSerializer(areas, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_admin_user(request):
    """Create new admin user (only for existing admins)"""
    if not request.user.userprofile.user_type == 'admin':
        return Response({
            'error': 'Insufficient permissions'
        }, status=status.HTTP_403_FORBIDDEN)

    serializer = AdminUserCreateSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user_type = serializer.validated_data['user_type']

        if User.objects.filter(username=username).exists():
            return Response({
                'error': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=serializer.validated_data.get('first_name', ''),
            last_name=serializer.validated_data.get('last_name', '')
        )

        # Create user profile with admin privileges
        UserProfile.objects.create(
            user=user,
            security_number=f"ADMIN_{username}",
            user_type=user_type,
            access_level=5,  # Highest access level for admins
            face_encoding="[]",
            pass_expires=datetime.now() + timedelta(days=365*5)  # 5 years for admins
        )

        return Response({
            'message': f'{user_type.title()} user created successfully',
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
