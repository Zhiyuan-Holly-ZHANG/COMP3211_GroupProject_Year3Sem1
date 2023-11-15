import threading
import time
from model.Alarm import Alarm


class Daemon:
    def __init__(self):
        pass

    def daemon_task(self):
        while True:
            al = Alarm()
            al.alarm()
            time.sleep(3)  # 定时延迟，模拟任务执行

    def create_daemon(self):
        daemon_thread = threading.Thread(target=self.daemon_task)
        daemon_thread.daemon = True
        daemon_thread.start()
