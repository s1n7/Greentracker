from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Activity, UserEntry
from .serializers import ActivitySerializer, UserEntrySerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserEntryViewSet(viewsets.ModelViewSet):
    queryset = UserEntry.objects.all()
    serializer_class = UserEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # sets user automatically

    @action(detail=False, methods=['get'])
    def my_entries(self, request):
        """Return all entries of the current user"""
        user_entries = UserEntry.objects.filter(user=request.user)
        serializer = self.get_serializer(user_entries, many=True)
        return Response(serializer.data)

class RegisterUserView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")  
        password = request.data.get("password")

        if not username or not password or not email:
            return Response({"error": "Username, email, and password required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already in use"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        token = Token.objects.create(user=user)

        return Response({"token": token.key}, status=status.HTTP_201_CREATED)
    
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete() # delete the token to force a login
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)