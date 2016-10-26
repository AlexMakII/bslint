import os
import unittest

import bslint
import bslint.error_messages.handler as error
import bslint.error_messages.constants as err_const
from bslint.lexer.lexer import Lexer as Lexer
from filepaths import TEST_CONFIG_FILE_PATH
from filepaths import STYLING_TEST_FILES_PATH
from filepaths import COMMENTS_CONFIG_PATH


class TestCommentFormat(unittest.TestCase):
    WARNINGS = 'Warnings'
    STATUS = 'Status'
    SUCCESS = 'Success'

    @classmethod
    def setUpClass(cls):
        cls.valid_comment_single_quote_no_todo_file_path = os.path.join(STYLING_TEST_FILES_PATH,
                                                                    'valid-comment-single-quote-no-TODO.txt')

    def test_no_comment_check(self):
        bslint.load_config_file(default_filepath=TEST_CONFIG_FILE_PATH)
        file_name = self.valid_comment_single_quote_no_todo_file_path
        chars = open(file_name, "r+").read()
        self.assertNotEqual(chars, "")
        exp_res = []
        result = Lexer().lex(chars)
        self.assertEqual(result[self.WARNINGS], exp_res)
        self.assertEqual(result[self.STATUS], self.SUCCESS)

    def test_todo_comment(self):
        todo_comment_config_path = os.path.join(COMMENTS_CONFIG_PATH, 'TODO-comment-config.json')
        bslint.load_config_file(user_filepath=todo_comment_config_path, default_filepath=TEST_CONFIG_FILE_PATH)
        file_name = self.valid_comment_single_quote_no_todo_file_path
        chars = open(file_name, "r+").read()
        self.assertNotEqual(chars, "")
        exp_res = [error.get_message(err_const.NON_CONVENTIONAL_TODO, [17])]
        result = Lexer().lex(chars)
        self.assertEqual(result[self.WARNINGS], exp_res)
        self.assertEqual(result[self.STATUS], self.SUCCESS)

    def test_todo_no_comment(self):
        valid_comment_single_quote_no_todo_config_path = os.path.join(COMMENTS_CONFIG_PATH,
                                                                      'valid-comment-single-quote-no-TODO.json')
        bslint.load_config_file(user_filepath=valid_comment_single_quote_no_todo_config_path,
                                default_filepath=TEST_CONFIG_FILE_PATH)
        file_name = self.valid_comment_single_quote_no_todo_file_path
        chars = open(file_name, "r+").read()
        self.assertNotEqual(chars, "")
        exp_res = [error.get_message(err_const.NON_CONVENTIONAL_TODO_AND_NO_COMMENTS, [11]),
                   error.get_message(err_const.NON_CONVENTIONAL_TODO_AND_NO_COMMENTS, [12]),
                   error.get_message(err_const.NON_CONVENTIONAL_TODO_AND_NO_COMMENTS, [17])]
        result = Lexer().lex(chars)
        self.assertEqual(result[self.WARNINGS], exp_res)
        self.assertEqual(result[self.STATUS], self.SUCCESS)

    def test_no_todo_comment(self):
        no_todo_comment_config_path = os.path.join(COMMENTS_CONFIG_PATH, 'no-TODO-comment-config.json')
        bslint.load_config_file(user_filepath=no_todo_comment_config_path, default_filepath=TEST_CONFIG_FILE_PATH)
        file_name = self.valid_comment_single_quote_no_todo_file_path
        chars = open(file_name, "r+").read()
        self.assertNotEqual(chars, "")
        exp_res = [error.get_message(err_const.NO_TODOS, [1]),
                   error.get_message(err_const.NO_TODOS, [17])]
        result = Lexer().lex(chars)
        self.assertEqual(result[self.WARNINGS], exp_res)
        self.assertEqual(result[self.STATUS], self.SUCCESS)

    def test_no_todo_no_comment(self):
        no_todo_no_comment_config_path = os.path.join(COMMENTS_CONFIG_PATH, 'no-TODO-no-comment-config.json')
        bslint.load_config_file(user_filepath=no_todo_no_comment_config_path, default_filepath=TEST_CONFIG_FILE_PATH)
        file_name = self.valid_comment_single_quote_no_todo_file_path
        chars = open(file_name, "r+").read()
        self.assertNotEqual(chars, "")
        exp_res = [
            error.get_message(err_const.COMMENTS_NOT_ALLOWED, [1]),
            error.get_message(err_const.COMMENTS_NOT_ALLOWED, [11]),
            error.get_message(err_const.COMMENTS_NOT_ALLOWED, [12]),
            error.get_message(err_const.COMMENTS_NOT_ALLOWED, [17])]
        result = Lexer().lex(chars)
        self.assertEqual(result[self.WARNINGS], exp_res)
        self.assertEqual(result[self.STATUS], self.SUCCESS)