import time

# for debug

IS_TIME_PRINT = True

class TaskTimer:
    def __init__(self):
        self.task_timers = {}

    def start(self, identifier):
        if not IS_TIME_PRINT:
            return
        self.task_timers[identifier] = time.time()

    def end(self, identifier):
        if not IS_TIME_PRINT:
            return
        if identifier not in self.task_timers:
            return
        end_time = time.time()
        try:
            elapsed_time = end_time - self.task_timers[identifier]
        except Exception:
            return
        print(f"TaskTimer: {identifier} : {elapsed_time:.2f} sec")
        del self.task_timers[identifier]


shigeTaskTimer = TaskTimer()

# Example usage
# shigeTaskTimer.start("task1")
# time.sleep(2)
# shigeTaskTimer.end("task1")

# shigeTaskTimer.start("task2")
# time.sleep(3)
# shigeTaskTimer.end("task2")