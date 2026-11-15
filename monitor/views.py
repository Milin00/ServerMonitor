from django.shortcuts import render
from .system_info import get_system_info

def index(request):

    system_info=get_system_info()

    params={
        'system_info': system_info,
    }

    return render(request, 'monitor/index.html', params)