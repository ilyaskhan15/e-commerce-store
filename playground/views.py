from django.shortcuts import render
from rest_framework.views import APIView
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import requests
from rest_framework.response import Response
from django.utils.decorators import method_decorator


class HelloView(APIView):
    @method_decorator(cache_page(60 * 15))  # Cache the view for 15 minutes 
    def get(self, request):
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        return render(request, 'hello.html', {'name': "Mosh"})

# @cache_page(60 * 15)  # Cache the view for 15 minutes
# def say_hello(request):
#     response = requests.get('https://httpbin.org/delay/2')
#     data = response.json()
#     return render(request, 'hello.html', {'name': data})
