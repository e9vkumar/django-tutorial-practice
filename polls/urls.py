from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("",views.IndexView.as_view(),name="index"), # working
    path("<int:pk>/display/",views.DisplayView.as_view(),name="display"), #working
    # path("<int:pk>/getone/",views.get_one,name="getone"), #same as above
    path("<int:question_id>/vote/",views.vote,name="vote"), #working
    path("<int:pk>/results/",views.ResultsView.as_view(),name="results"), # working
]