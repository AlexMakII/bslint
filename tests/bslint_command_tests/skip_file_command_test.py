import unittest
import os
import bslint
import bslint.error_messages.handler as err
import bslint.error_messages.constants as err_const
from bslint.lexer.lexer import Lexer as Lexer
from filepaths import BSLINT_COMMAND_CONFIG_PATH


class TestSkipFileCommand(unittest.TestCase):

    WARNINGS = 'Warnings'

    def test_skip_file_command_skip_start(self):
        active_skip_file_config_path = os.path.join(BSLINT_COMMAND_CONFIG_PATH, 'active-skip-file-config.json')
        bslint.load_config_file(user_filepath=active_skip_file_config_path)
        exp_result = []
        result = Lexer().lex("'BSLint_skip_file \nxgygu= 22\n  y=4\n sdfsf=2 \n")
        self.assertEqual(exp_result, result[self.WARNINGS])

    def test_skip_file_command_skip_half_way(self):
        exp_result = []
        result = Lexer().lex("one = 22\ntwo = 4\n'BSLint_skip_file \n sdfsf=2 \n")
        self.assertEqual(exp_result, result[self.WARNINGS])

    def test_skip_file_command_skip_start_inactive(self):
        inactive_skip_file_config_path = os.path.join(BSLINT_COMMAND_CONFIG_PATH, 'inactive-skip-file-config.json')
        bslint.load_config_file(user_filepath=inactive_skip_file_config_path)
        exp_result = [err.get_message(err_const.TYPO_IN_CODE, [2]),
                      err.get_message(err_const.NO_SPACE_AROUND_OPERATORS, [1, 2])]
        result = Lexer().lex("'BSLint_skip_file\nxgygu =22\ny = 4")
        self.assertEqual(exp_result, result[self.WARNINGS])

    def test_skip_file_command_skip_halfway_inactive(self):
        exp_result = []
        result = Lexer().lex("one = 22\ntwo = 4\n'BSLint_skip_file\ntwo= 2\n")
        self.assertEqual(exp_result, result[self.WARNINGS])