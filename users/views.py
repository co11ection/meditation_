import json
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, JsonResponse
from rest_framework.response import Response
from rest_framework import status

import users.db_communication as db
from .models import Users
from users import utils


@api_view(['POST'])
@csrf_exempt
def registration(request: HttpRequest):
    try:
        values = json.loads(request.body)
        # if not utils.check_gender(values['gender']):
        #     return HttpResponseBadRequest("gender must be male or female")
        # if not (utils.is_phone_number(values['login']) or utils.is_email(values['login'])):
        #     return HttpResponseBadRequest("login must be email or phone number")
        login = values['login']
        if utils.is_phone_number(login):
            if Users.objects.filter(phone_number__contains=utils.ru_phone(login)):
                user = db.get_user(login=login)
                user.fcm_token = values['fcm_token']
                user.save()
                return JsonResponse({
                    'authorized': True,
                    'token': user.token,
                    "id": user.id,
                })
        token, user = db.add_user(values, request.GET.get('ref'))
        return JsonResponse({
            "token": token,
            "id": user.id,
        })
    except Exception as err:
        return Response({"error": f"Something goes wrong: {err}"}, status=status.HTTP_400_BAD_REQUEST)
