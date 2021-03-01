import pyautogui
import threading
import time
import sys
import keyboard

time.sleep(2)
f = ['hello', 'hello', 'hello', 'hello', 'hello', 'hello']
if __name__ == '__main__':
    for word in f:
        if keyboard.is_pressed('q'):
            sys.exit()
        pyautogui.typewrite(word)
        time.sleep(3)
