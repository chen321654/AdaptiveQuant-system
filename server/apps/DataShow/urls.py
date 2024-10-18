from django.urls import path
from apps.DataShow.views import DataGetView, DataShowView

urlpatterns = [
    path("dataget/", DataGetView.as_view()),
    path("k_line/", DataShowView.as_view()),

]
