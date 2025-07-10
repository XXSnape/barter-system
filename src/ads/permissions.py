from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.user == request.user
        )


class IsReceiverOrSender(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if not request.user:
            return False
        if request.method in permissions.SAFE_METHODS and request.user in (
            obj.ad_receiver.user,
            obj.ad_sender.user,
        ):
            return True
        if request.method == "DELETE":
            return request.user == obj.ad_sender.user
        return obj.ad_receiver.user == request.user
