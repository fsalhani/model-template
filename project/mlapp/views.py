# coding: utf-8
from __future__ import unicode_literals

import json

from django.http import JsonResponse, HttpResponseNotAllowed
from .utils import routing

from . import models

# flask-style route decorators
url, urlpatterns = routing()

predictor = models.Predictor()

@url(r'^health_check/ping$')
def king(request):
    if request.method.upper() != 'GET':
        return HttpResponseNotAllowed(['GET'])  # List of allowed ones
    else:
        return JsonResponse({
            'message': 'pong',
        }, status=200)


@url(r'^predict$')
def predict(request):
    if request.method.upper() != 'POST':
        return HttpResponseNotAllowed(['POST'])  # List of allowed ones
    else:
        try:
            json_data = json.loads(request.body.decode('utf-8'))
        except:
            json_data = {}
        answer = predictor.predict(json_data)

        return JsonResponse(answer, safe=False, status=200)
