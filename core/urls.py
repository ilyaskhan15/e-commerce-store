from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    # path('hello/', say_hello, name='hello'),
    path('', TemplateView.as_view(template_name='core/index.html')),
]