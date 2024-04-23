from rest_framework import viewsets, mixins
from .models import Notification
from .serializers import NotificationSerlizer


class NotificationViewSet(
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):

    serializer_class = NotificationSerlizer

    def get_queryset(self):
        notifications = Notification.objects.all()
        owner_id = self.request.query_params.get('owner_id')
        notification_id = self.request.query_params.get('notification_id')

        if owner_id is not None and notification_id is None:
            return notifications.filter(
                document__vehicle__owner__id=owner_id)
        elif owner_id is not None and notification_id is not None:
            return notifications.filter(
                document__vehicle__owner__id=owner_id, id=notification_id)

        return []
