from django.shortcuts import redirect, render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

from django.contrib.auth.decorators import login_required

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        empresa = getattr(self.request.user, 'empresa', None)
        return Notification.objects.filter(empresa=empresa).select_related('content_type').order_by('-criado_em')

class NotificationMarkReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()

    def patch(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.visualizado = True
        obj.save(update_fields=['visualizado'])
        return Response(self.get_serializer(obj).data, status=status.HTTP_200_OK)
    

@login_required(login_url='/auth/login/')
def mark_read(request, id):
    empresa = request.user.empresa
    try:
        notification = Notification.objects.get(id=id, empresa=empresa)
        notification.visualizado = True
        notification.save()
    except Notification.DoesNotExist:
        pass
    return redirect(request.META.get('HTTP_REFERER', '/'))