from time import sleep
import json
import os
from datetime import datetime, timedelta
#import json_handler


class Pomidor:

    def __init__(self, user_name, job_time=25, pause_time=5):  #standart values without configuration in minutes
        self.user_name = user_name
        self.job_time = job_time
        self.pause_time = pause_time
        self._sec_in_min = 60  #number of seconds
        self.count_of_sessions = 0
        self.history = 'history.json'  #short data
        self.log = 'log.json'  #data with start time, end time(more info)
        self.start_time = ''
        self.end_time = ''

    def configurate_time(self):  #configuration for time of job and break
        if input('Do you want to configurate time? [y/n]: ').lower() == 'y':
            self.job_time = int(input("How many minutes will you work: "))
            self.pause_time = int(input("How many minutes will you relax: "))
            return self.job_time, self.pause_time

    @staticmethod
    def get_time(fmt="%H:%M:%S"):
        return datetime.now().strftime(fmt)


    def timer(self):
        for seconds in range(self.job_time * self._sec_in_min, 0, -1):
            print(f'{int(seconds / 60):02}:{seconds % 60:02}')
            sleep(1)


    def job(self):
        print("Start working!!")
        self.timer()

    def pause(self):
        print("Pause")
        self.timer()
        print('break')

    def save_history(self):
        data = self.check_json(self.history)
        now = self.get_time("%Y-%m-%d %H:%M:%S")
        if self.user_name in data:
            data[self.user_name]['session'] += self.count_of_sessions
            data[self.user_name]['time'] = now
        else:
                data[self.user_name] = {'session': self.count_of_sessions, 'time':now}
        self.write_json(self.history, data)

    def save_log(self):
        data = self.check_json(self.log)
        now = self.get_time("%Y-%m-%d")
        duration = self.find_duration()
        if self.user_name in data:
            name = data[self.user_name]
            name.append({'date': now,
                         'start_time': self.start_time,
                         'end_time': self.end_time,
                         'duration': duration})
        else:
            data[self.user_name] = [{'date': now,
                                     'start_time': self.start_time,
                                     'end_time': self.end_time,
                                     'duration': duration}]
        self.write_json(self.log, data)

    @staticmethod
    def check_json(path):
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return {}
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    @staticmethod
    def write_json(path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    def find_duration(self):
        fmt = "%H:%M:%S"
        t1 = datetime.strptime(self.start_time, fmt)
        t2 = datetime.strptime(self.end_time, fmt)
        if t2 < t1:
            t2 += timedelta(days=1)
        delta = t2 - t1
        return int(delta.total_seconds() / 60)

    def session(self):
        is_running = True

        self.configurate_time()
        while is_running:
            self.start_time = self.get_time()
            self.job()
            self.end_time = self.get_time()
            self.count_of_sessions += 1  # one session was finished
            self.pause()
            self.save_log()
            answer = input("Start another session? [y/n]: ").lower()
            is_running = answer == "y"
        self.save_history()


if __name__ == '__main__':
    user = Pomidor(input("Enter your name: "))
    user.session()
    print('Bye!')