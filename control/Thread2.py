import threading
import time
from model.Alarm import Alarm

# this new thread is created to associate with Alarm to send Mail to users
class Daemon:
    def __init__(self):
        pass

    def daemon_task(self):
        while True:
            al = Alarm()
            al.alarm()
            time.sleep(3)  # avoid the over occupied of the CPU

    #create and start
    def create_daemon(self):
        daemon_thread = threading.Thread(target=self.daemon_task)
        daemon_thread.daemon = True
        daemon_thread.start()
