from django.urls import path
from . import views

urlpatterns = [
    path('', views.options, name='api_options'),
    path('login/', views.login, name='login'),
    path('userInfo/', views.getUserInfo, name='userInfo'),
    path('receptionist/appointments/', views.getReceptionistAppointments,
         name="receptionistAppointment"),
    path('doctor/appointments/', views.getDoctorAppointments,
         name="doctorAppointment"),
    path('doctor/tests/', views.getDoctorTests, name="doctorTests"),
    path('doctor/surgery/', views.getDoctorSurgery, name="doctorSurgery"),
    path('doctor/diagnosis/', views.docDiagnosis, name="docDiagnosis"),
    path('doctor/testResults/', views.getServiceResults, name="testResults"),
    path('doctor/upcomingSurgeries/',
         views.showUpcomingSurgeries, name="upcomingSurgeries"),
    path('technician/tests/', views.technicianTests, name="technicianTests"),
    path('technician/test/result/', views.technicianTestResult, name = "technicianTestResult"),
]
