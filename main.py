from time import sleep
import json
import os
from datetime import datetime


class Pomidor:

    def __init__(self, user_name, job_time=25, pause_time=5):  #standart values without configuration
        self.user_name = user_name
        self.job_time = job_time
        self.pause_time = pause_time
        self._minute = 2
        self.count_of_sessions = 0
        self.history = 'history.json'

    def time_config(self):  #configuration for time of job and break
        if input('Do you want to configurate time? [y/n]: ').lower() == 'y':
            self.job_time = int(input("How many minutes will you work: "))
            self.pause_time = int(input("How many minutes will you relax: "))
            return self.job_time, self.pause_time

    def job(self):
        print("Start working!!")
        sleep(self.job_time * self._minute)

    def pause(self):
        print("Pause")
        sleep(self.pause_time * self._minute)

    def check_history(self):  #func checks file exist. if not - creates new. Return data from file
        if not os.path.exists(self.history) or os.path.getsize(self.history) == 0:
            return {}
        with open(self.history, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}

    def save_history(self):
        data = self.check_history()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if self.user_name in data:
            data[self.user_name][0] += self.count_of_sessions
            data[self.user_name][1] = now
        else:
                data[self.user_name] = {'Session': self.count_of_sessions, 'Time':now}
            
        with open(self.history, 'w') as file:
            json.dump(data, file, indent=4)

    def session(self):
        is_running = True

        self.time_config()
        while is_running:
            self.job()
            self.count_of_sessions += 1  # one session was finished
            self.pause()
            answer = input("Start another session? [y/n]: ").lower()
            is_running = answer == "y"
        self.save_history()

if __name__ == '__main__':
    s = Pomidor(input("Enter your name: "))
    Pomidor.session(s)
    print('Bye!')

