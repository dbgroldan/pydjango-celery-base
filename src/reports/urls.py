from django.urls import path
from .views import indexView, addView, getDataView,\
     longAddView, getTaskStatus

urlpatterns = [
    path('', indexView, name='index'),

    path('add/x<int:x>/y<int:y>', addView, name='simpleResp'),
    path('result_simple/<str:process>/<str:task_id>', getDataView, name='getData'),

    path('long_add/x<int:x>/y<int:y>', longAddView, name='initProgressResp'),
    path('result_long/<str:id_task>', getTaskStatus, name='getTaskStatus')
]