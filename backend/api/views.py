from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Activity, UserEntry
from .serializers import ActivitySerializer, UserEntrySerializer

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
