from django.urls import path, include
from .views import indexView
from django.views.generic import TemplateView

urlpatterns = [
    path('',TemplateView.as_view(template_name ='homepage/index.html'))

]
