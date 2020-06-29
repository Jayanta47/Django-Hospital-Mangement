from django.urls import path
from firstapp import views

app_name = 'firstapp'


urlpatterns = [
    path('index', views.index, name='index'),
    path('homepage', views.frontpage, name='homepage'),
    path('appointment', views.appointmentpage, name='appointment'),
    path('register', views.register_page, name='register'),
    path('employee', views.employeepage, name='employee'),
    path('patient', views.patientpage, name='patient'),
    path('test', views.testpage, name='test'),
    path('load_cities', views.loadcities, name='ajax_load_cities'),
    path('load_doc_select', views.loadDocSelect, name='ajax_load_docs'),
    path('schedule/', views.schedule, name='design_schedule'),
    path('schedule/load_doc_info', views.doc_data, name='emp_date_data'),
    path('schedule/data_schedule_prev', views.doc_schedule, name='emp_schedule_data'),
    path('schedule/add_data', views.doc_save_schedule, name='save_schedule_data'),
    path('schedule/delete_schedule', views.doc_delete_schedule, name='delete_schedule_data'),
    path('load_pat_info', views.pat_data, name='pat_bio_data'),
    path('load_dept_doc', views.loadDocSelect, name='load_doc_list'),
    path('reg_temp_pat', views.patient_register, name='patient_register'),
    path('aux_app_reg', views.appointment_reg, name='app_register'),
    path('final_app_reg', views.app_reg_final, name='app_reg_final'),
]
