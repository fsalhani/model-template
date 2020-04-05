# coding: utf-8
from __future__ import unicode_literals

import json

from django.http import JsonResponse, HttpResponseNotAllowed
from .utils import routing

from . import models

# flask-style route decorators
url, urlpatterns = routing()


@url(r'^health_check/ping$')
def king(request):
    if request.method.upper() != 'GET':
        return HttpResponseNotAllowed(['GET'])  # List of allowed ones
    else:
        return JsonResponse({
            'message': 'pong',
        }, status=200)