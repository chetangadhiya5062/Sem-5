import schedule
def my_task():
    print("Task Executed")
schedule.every(5).seconds.do(my_task)

while True:
    schedule.run_pending()