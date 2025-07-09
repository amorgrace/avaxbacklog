from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import UserRegisterSerializer, UserSerializer
from dj_rest_auth.views import LoginView, LogoutView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RecentTransactionSerializer, ChangePasswordSerializer
from .models import RecentTransaction
from rest_framework.views import APIView
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # Explicitly disable authentication (including CSRF)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({
                'message': 'Registration successful.',
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Registration failed.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        print("🔥 CustomLoginView called")
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({
                'message': 'Login failed - Incorrect email or Password.',
                'errors': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.serializer = serializer
        self.login()

        response = self.get_response()
        response.data['message'] = 'Login is successful.'
        return response
    
    
class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data = {'message': 'Logout successful.'}
        return response


class UserRecentTransactionListView(generics.ListAPIView):
    serializer_class = RecentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RecentTransaction.objects.filter(user=self.request.user).order_by('-created_at')
    

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        current_password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']
        
        if not user.check_password(current_password):
            return Response({'error': 'Current Password is incorrect!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if not new_password or len(new_password) < 8:
            return Response({'error': 'New password must be at least 8 characters!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password updated successfully.'}, status=status.HTTP_200_OK)
