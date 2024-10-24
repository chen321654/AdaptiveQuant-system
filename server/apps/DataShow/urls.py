from django.urls import path
from apps.DataShow.views import DataGetView, KLineDataGetView, NewKLineDataGetView

urlpatterns = [
    path("dataget/", DataGetView.as_view()),
    path("k_line/", KLineDataGetView.as_view()),
    path("/newk_linedata/", NewKLineDataGetView.as_view()),
]
