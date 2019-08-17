from django.conf.urls import url
from employee_database_api import views

app_name = 'employee_database_api'





urlpatterns = [
    url(r'^employee_hire/$', views.EmployeeHire.as_view(), name='EmployeeHire')
]