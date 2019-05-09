# -*- coding: UTF-8 -*-
import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from apps.response.models import User


def getform(request):
    # all_infos = User.objects.filter(name='xz', user_id='1')
    # for i in all_infos:
    #     print(i.name)
    user_infos = User()
    user_infos.user_id = '2'
    user_infos.name = 'ldy'
    user_infos.email = ''
    user_infos.save()
    print('saved ')
    return render(request, 'test.html')


def response(request):
    print('response')
    info = User.objects.filter()[0]
    data = {"name": info.name}
    return HttpResponse(json.dumps(data))


def medic_details(request):
    if (request.method == 'POST'):
        print("the POST method")
        concat = request.POST
        postBody = request.body
        print(concat)
        print(type(postBody))
        print(postBody)
        json_result = json.loads(postBody)
        print(json_result)
    data = {}
    return {"name"}