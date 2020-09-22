from django.shortcuts import render
from django.http import JsonResponse
from celery.result import AsyncResult

from .tasks import add, long_process_add

def indexView(request):
    return JsonResponse({'message':'Hello Celery tasks'})

# First Case
def addView(request, x, y):
    task_res = add.delay(x, y)
    data = {
        'process':'Add',
        'x': x,
        'y':y,
        'result': '... Processing ...',
        'task': task_res.id
        }
    return JsonResponse(data)

def getDataView(request, process, task_id):
    tsk = AsyncResult(task_id)
    if tsk.state == "PENDING":
        response = {
            'state': tsk.state, 
            'status': 'Pending...'
            }
    elif tsk.state != "FAILURE":
        response = {
            'process': process,
            'state': tsk.state,
            'result': tsk.get()
        }
    else:
        response = {
            'process': process,
            "state": tsk.state,
            "status": str(tsk.info)
        }
    return JsonResponse(response)


# Second Case
def longAddView(request, x, y):
    task_res = long_process_add.apply_async(args=[x, y])
    data = {
        'process':'Add Long Process',
        'x': x,
        'y':y,
        'result': '... Processing ...',
        'task': task_res.id
        }
    return JsonResponse(data)

def getTaskStatus(request, id_task):
    task = AsyncResult(id_task)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info), 
        }
    return JsonResponse(response)