from rest_framework import viewsets, mixins
from .models import Notification
from .serializers import NotificationSerlizer
from django.contrib.auth import get_user_model
from rest_framework.routers import Response
from rest_framework import status

User = get_user_model()


class NotificationViewSet(
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):

    serializer_class = NotificationSerlizer

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        owner = User.objects.get(id=user_id)

        cur_notifications = Notification.objects.filter(
            document__vehicle__owner=owner)

        if not cur_notifications.exists():
            return Response([])

        notifications = NotificationSerlizer(cur_notifications, many=True)
        return Response(notifications.data)

    def retrieve(self, request, *args, **kwargs):
        notification_id = kwargs.get('pk')

        try:
            current_notification = Notification.objects.get(id=notification_id)
        except Notification.DoesNotExist:
            return Response({"Message": "Notification with the given id not found"}, status=status.HTTP_404_NOT_FOUND)

        notification_serializer = NotificationSerlizer(current_notification)
        return Response(notification_serializer.data)

    def update(self, request, *args, **kwargs):
        notification_id = kwargs.get('pk')

        try:
            current_notification = Notification.objects.get(id=notification_id)
        except Notification.DoesNotExist:
            return Response({"Message": "Notification with the given id not found"}, status=status.HTTP_404_NOT_FOUND)

        current_notification.seen = True
        current_notification.save()

        notification = NotificationSerlizer(current_notification)

        return Response(notification.data)

    def destroy(self, request, *args, **kwargs):
        notification_id = kwargs.get('pk')

        try:
            current_notification = Notification.objects.get(id=notification_id)
        except Notification.DoesNotExist:
            return Response({"Message": "Notification with the given id not found"}, status=status.HTTP_404_NOT_FOUND)

        current_notification.delete()
        return Response({"Message": "Notification deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
