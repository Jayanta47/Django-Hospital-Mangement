from django.conf.urls import url
from django.urls import path
from firstapp import views

app_name = 'firstapp'


urlpatterns = [
    path('index', views.index, name ='index'),
    path('homepage', views.frontpage, name='homepage'),
    path('appointment', views.appointmentpage, name='appointment'),
    path('register',views.registerpage, name = 'register'),
    path('employee',views.employeepage,name = 'employee'),
    path('patient',views.patientpage, name ='patient'),
    path('test', views.testpage, name='test'),
    path('load_cities', views.loadcities, name='ajax_load_cities'),
    path('load_doc_select', views.loadDocSelect, name = 'ajax_load_docs'),
]
