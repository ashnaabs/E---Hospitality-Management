from django.urls import path
from . import views

urlpatterns=[
path('index/',views.appointment,name='index'),
path('index2/',views.Index2,name='index2'),
path('doctor/index2/',views.Index2,name='index2'),
path('reg/',views.patient_reg,name='reg'),
path('reg/list',views.patient_reg_list,name='reg_list'),
path('reg/delete_list/<int:book_id>/',views.deletebook,name='delete_list'),
path('doctor/slot',views.slots,name='slot'),
path('slot/list',views.slot_list,name='list'),
    path('slot/update_slot/<int:pat_id>/',views.update_slot,name='update_slot'),
path('slot/delete_slot/<int:pat_id>/',views.delete_slot,name='delete_slot'),
path('user_list/',views.user_slot_list,name='user_list'),
path('login_slot/',views.login_patient_slot,name='login_slot'),
path('user_list_result/<int:doc_id>/<str:patient_name>/',views.slot_list_result,name='user_list_result'),
path('doctor/doc_index',views.doctor_index,name='doctor_index'),
path('doctor/prescription',views.prescription,name='prescription'),
path('doctor/doctor',views.createdoctor,name='doctor'),
path('login/',views.login_patient,name='login'),
path('doctor/history',views.history_medical,name='history'),
path('doctor/history_list',views.hist_list,name='history_list'),
path('doctor/update/<int:pat_id>/',views.updatehistory,name='update'),
path('history_list_id/<str:patient_name>/',views.hist_list_id,name='history_list_id'),
path('billing/',views.payment,name='billing'),

    path('billing/make_payment/', views.process_payment, name='make_payment'),
    path('billing/make_payment/payment_success/', views.payment_success, name='payment_success'),
    path('billing/payment_error/', views.payment_error, name='payment_error'),
    path('login_patient_payment/',views.login_patient_payment,name='login_patient_payment'),
path('billing/make_payment/payment_list', views.payment_list, name='payment_list'),
    path('',views.Index,name='app'),
    path('slot_whole_list/',views.slot_whole_list,name='slot_whole_list'),
    path('doctor/pharm',views.pharmacy,name='pharm'),
    path('doctor/pharm_success',views.pharm_success,name='pharm_success'),
    path('doctor/patient_list',views.patient_list,name='patient_list'),

path('admin_index/',views.admin_index,name='admin_index'),
path('admin_index/reg_list',views.admin_patient_reg_list,name='admin_reg_list'),
path('admin_index/admin_patient_list',views.admin_patient_list,name='admin_patient_list'),
path('admin_index/admin_user_send/<str:patient_name>/',views.admin_user_send,name='admin_user_send'),
path('admin_index/admin_user_send/<str:patient_name>/admin_mail_box',views.admin_mail_box,name='admin_mail_box'),
path('admin_index/admin_user_send/<str:patient_name>/admin_mail_result',views.admin_mail_result,name='admin_mail_result'),
path('admin_index/admin_resource',views.admin_panel,name='admin_resource'),
path('admin_index/admin_resource/resource',views.resource,name='resource'),
path('admin_index/admin_resource/update<int:ad_id>/',views.update_resource,name='update_resource'),
    path('admin_index/admin_payment_list',views.admin_payment_list,name='admin_payment_list'),
path('resource/',views.patient_resource,name='pat_resource'),
path('connect_doctor/',views.connect_doctor,name='connect_doctor'),
path('connect_admin/',views.connect_admin,name='connect_admin'),

]
