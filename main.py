from time import sleep

def job(minutes):
    print("Start working!!")
    sleep(25*minutes)

def pause(minutes):
    print("Pause")
    sleep(5 * minutes)

def asking():  #will ask user about new session
    answer = input("Do you want to start a new session? [y/n]: ").lower()
    return answer == 'y'  #will finish program if answer = False

def save_history(n, s):  #name, session_count
    with open('history.txt', 'w') as file:
        file.write(f"Name = {n}\nNumber of sessions: {s}")

name = input("Enter your name: ")
minute = 60  #how many seconds in one minute
session_count = 0  #number of sessions
is_running = True

while is_running:
    job(minute)
    session_count += 1  #one session was finished
    pause(minute)
    is_running = asking()

save_history(name, session_count)

