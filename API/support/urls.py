from django.urls import path

from .views import ReportProblemView

app_name = "support"

urlpatterns = [
    path("report-problem/", ReportProblemView.as_view(), name="report-problem"),
]
