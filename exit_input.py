import sys
import time
import msvcrt


def edit_last_response(statement):
    new_response = input('edit> ')
    print(f'learn response "{new_response}" for input "{statement}" ')
    return new_response


def readInput(prompt, default='', timeout=5, edit=edit_last_response, last_input=None):
    start_time = time.time()
    sys.stdout.write(f'{prompt}')
    sys.stdout.flush()
    user_input = ''
    while True:
        if msvcrt.kbhit():
            chr = msvcrt.getche()
            if ord(chr) == 18:
                edit(last_input)
                break
            if ord(chr) == 13:  # enter_key
                break
            elif ord(chr) >= 32:  # space_char
                user_input += str(chr, 'utf-8')
        if len(user_input) == 0 and (time.time() - start_time) > timeout:
            break

    print('')  # needed to move to next line
    if len(user_input) > 0:
        return user_input
    else:
        return default


# and some examples of usage
input_statement = None
while True:
    input_statement = readInput('> ', timeout=30, last_input=input_statement)
    if input_statement:
        print('response')
