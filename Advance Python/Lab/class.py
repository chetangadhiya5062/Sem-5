from time import sleep
from threading import Thread

def task():
    sleep(1)
    print("this is from another thread")

thread = Thread(target=task)
thread.start()

print("waiting for the thread..")
thread.join()
