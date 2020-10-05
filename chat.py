from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_first_response
from chatterbot.conversation import Statement

import keyboard
import logging
import sys
import time
import msvcrt

logging.basicConfig(level=logging.ERROR)


class TerminalInput(object):

    bot = ChatBot(
        'Terminal',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            {
                'import_path': 'fact_adapter.FactLogicAdapter'
            },
            'chatterbot.logic.MathematicalEvaluation',
            'chatterbot.logic.TimeLogicAdapter',
            'chatterbot.logic.UnitConversion',
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I am sorry, but I do not understand.',
                'maximum_similarity_threshold': 0.90
            }
        ],
        response_selection_method=get_first_response,
        database_uri='sqlite:///database.db'
    )

    # trainer = ChatterBotCorpusTrainer(bot)
    # trainer.train("chatterbot.corpus.english")

    def __init__(self, edit_hot_key, prompt='> '):
        self._edit_hot_key = edit_hot_key
        self._prompt = prompt
        self._bot_response = None
        self._input_statement = None
        print(f'[Press {edit_hot_key} to edit response]')

    def asc(self, string):
        if len(string) == 1:
            return ord(string)
        elif string.startswith('ctrl+'):
            return ord(string[-1]) - ord('`')

    def edit_response(self):
        print(f'if "{self._bot_response.text}" is a bad response, please input a correct response for "{self._input_statement.text}"')
        self._correct_response = Statement(text=input('Response: '))
        self._input_statement.search_text = self._input_statement.text

        TerminalInput.bot.learn_response(
            self._input_statement, self._correct_response)
        output = f'Response "{self._correct_response.text}" added for "{self._input_statement.text}"'
        print(output)

    def read_input(self, prompt='> ', default='', timeout=30, edit=None):
        start_time = time.time()
        sys.stdout.write(f'{prompt}')
        sys.stdout.flush()
        user_input = ''

        if edit is None:
            edit = self.edit_response

        while True:
            if msvcrt.kbhit():
                chr = msvcrt.getch()
                if ord(chr) == self.asc(self._edit_hot_key):
                    edit()
                    break
                if ord(chr) == 8 and len(user_input) > 0:
                    user_input = user_input[:-1]
                    print('\b \b', end='')
                if ord(chr) == 13:  # enter_key
                    break
                elif ord(chr) >= 32:  # space_char
                    letter = str(chr, 'utf-8')
                    sys.stdout.write(f'{letter}')
                    sys.stdout.flush()
                    user_input += letter
            if len(user_input) == 0 and (time.time() - start_time) > timeout:
                break

        print('')  # needed to move to next line
        if len(user_input) > 0:
            return user_input
        else:
            return default

    def get_input_and_response(self):
        input_statement = Statement(text=self.read_input())
        if input_statement and input_statement.text:
            self._input_statement = input_statement

            try:
                bot_response = TerminalInput.bot.generate_response(
                    self._input_statement)
                if bot_response:
                    self._bot_response = bot_response
                else:
                    self._bot_response = None
                return bot_response
            except:
                e = sys.exc_info()
                print(e)
        else:
            return None

    @property
    def input_statement(self):
        return self._input_statement

    @input_statement.setter
    def input_statement(self, statement):
        self._input_statement = statement

    @property
    def bot_response(self):
        return self._bot_response

    @bot_response.setter
    def bot_response(self, statement):
        self._bot_response = statement


def main():

    ti = TerminalInput(edit_hot_key='ctrl+r')
    while True:
        try:
            response = ti.get_input_and_response()
            if response:
                print('Bot: ' + response.text)
        # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break


print('Type something to begin...')
main()
