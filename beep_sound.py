from playsound import playsound
from time import sleep

def play_beep():
    playsound("sound/beep.mp3", block=False)
    
play_beep()
sleep(1)