# Waits for key press
import keyboard
print('> ', end='')
event = keyboard.read_event()
if event.event_type == keyboard.KEY_DOWN:
    key = event.name
    print(f'Pressed: {key}')
print('here')
