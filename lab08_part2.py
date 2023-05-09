import threading
def task1():
    for i in range(5):
        print("Task 1 running")
def task2():
    for i in range(5):
        print("Task 2 running")
# Create two Thread objects for each task
thread1 = threading.Thread(target=task1)
thread2 = threading.Thread(target=task2)
# Start the threads
thread1.start()
thread2.start()
# Wait for the threads to finish executing
thread1.join()
thread2.join()
# Main thread continues here after both threads have finished
print("Done")
