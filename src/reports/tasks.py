from celery import shared_task
import time

@shared_task
def add(x, y):
    time.sleep(10)
    return x + y

@shared_task(bind=True)
def long_process_add(self, x, y):
    result_add = x + y
    total = 30
    for i in range(total):
        # Modify state
        self.update_state(state="PROGRESS",
         meta={
                "current": i,
                "total": total, 
                "status": "... Processing ..."
             })
        # Activities
        time.sleep(1)
    return {
        'current': 100, 
        'total': 100, 
        'status': 'Task Complete.',
        'result': result_add
    }