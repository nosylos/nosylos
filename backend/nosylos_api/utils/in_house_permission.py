from django.conf import settings
from django.http.request import split_domain_port
from rest_framework import permissions


class InHousePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        host = split_domain_port(request.get_host())[0]
        host = "localhost" if host == "127.0.0.1" else host
        return host in settings.ALLOWED_HOSTS
