from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *


urlpatterns = [

    path("search/",SearchAPIView.as_view(),name="search"),
    path("task-status/<str:task_id>/",TaskStatusAPIView.as_view(),name="task_status"),
]

urlpatterns = format_suffix_patterns(urlpatterns)



