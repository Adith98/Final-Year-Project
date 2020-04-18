from celery import shared_task, current_task
from time import sleep
import random
from celery_progress.backend import ProgressRecorder


@shared_task
def sleepy(duration):
    sleep(duration)
    return None


def do_work_item(work_item):
    sum = 1
    for i in range(1, work_item + 1):
        sum = sum * i
    print(sum)


@shared_task(bind=True)
def do_work(self):
    progress_recorder = ProgressRecorder(self)
    list_of_work = [10, 3, 4, 5, 10, 20, 5, 4, 6, 7, 9]
    total_work_to_do = len(list_of_work)
    for i in range(1, total_work_to_do + 1):
        do_work_item(list_of_work[i - 1])
        progress_recorder.set_progress(i, total_work_to_do)

    return "Work is done"
