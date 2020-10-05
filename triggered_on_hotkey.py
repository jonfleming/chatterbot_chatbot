# Triggered on hotkey press
import keyboard


def edit():
    print('ctrl+e was pressed')


keyboard.add_hotkey('ctrl + e', edit)
print('here. waiing for input')
text = input()
print(text)
