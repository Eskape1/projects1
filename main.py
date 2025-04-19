from time import sleep
import json
import os

class Pomidor:

    def __init__(self, user_name, job_time=25, pause_time=5):
        self.user_name = user_name
        self.job_time = job_time
        self.pause_time = pause_time
        self._minute = 2
        self.count_of_sessions = 0
        self.history = 'history.json'

    def time_config(self):
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

    def check_history(self):
        if os.path.exists(self.history) and os.path.getsize(self.history) > 0:
            with open(self.history, "r") as file:
                try:
                    data = json.load(file)
                    return data
                except json.JSONDecodeError:
                    data = {}
                    return data

        else:
            data = {}
            return data

    def save_history(self):
        data = self.check_history()
        try:
            if data[self.user_name] in data.values():
                data[self.user_name] += self.count_of_sessions
                with open(self.history, 'w') as file:
                    json.dump(data, file, indent=4)
        except KeyError:
            with open(self.history, 'w') as file:
                data[self.user_name] = self.count_of_sessions
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

