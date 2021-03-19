import threading
import time

class myThread(threading.Thread):
    def __init__(self, ID, name, counter):
        threading.Thread.__init__(self)
        self.threadID=IDself.name = name
        self.counter= counter

    def run(self):
        print("Empiezo" + self.name)
        self.print_time(self.name, 5, self.counter)
        print("Termino" + self.name)
    
    def print_time(threadName, counter, delay):
        while counter>0:
        time.sleep(delay)
        print (threadName)
        counter -= 1

thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

thread1.start()
thread2.start()