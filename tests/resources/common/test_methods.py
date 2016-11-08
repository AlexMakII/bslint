import unittest

from filepaths import TEST_CONFIG_FILE_PATH
from bslint.parser.parser import Parser
import bslint.constants as const
import bslint.lexer.commands as commands
from bslint.lexer.lexer import Lexer as Lexer
import bslint.lexer.handlers.regex_handler as regex_handler
import bslint


class CommonMethods(unittest.TestCase):
    WARNINGS = 'Warnings'
    STATUS = 'Status'
    SUCCESS = 'Success'

    def status_error(self, str_to_parse):
        parser = Parser()
        result = parser.parse(str_to_parse)
        self.assertEqual("Error", result["Status"])

    def match_statement(self, characters, expected):
        parser = Parser()
        parser.parse(characters)
        self.assertEqual(expected, parser.all_statements[-1][0])

    def match_program(self, characters, expected):
        parser = Parser()
        result = parser.parse(characters)
        self.assertEqual("Success", result["Status"])
        self.assertEqual(expected, parser.line_reductions[-1][0])

    def lex_warnings_match(self, characters, exp_result):
        result = Lexer().lex(characters)
        self.assertEqual(exp_result, result[self.WARNINGS])

    def match_regex(self, identifier, match_group, lexer_type, parser_type):
        result = regex_handler.find_match(identifier)
        if match_group is None:
            self.assertEqual(result["match"].group(), identifier)
        else:
            self.assertEqual(result["match"].group(match_group), identifier)
        self.assertEqual(result["token_lexer_type"], lexer_type)
        self.assertEqual(result["token_parser_type"], parser_type)

    def directory_lexing(self, brs_file_path, exp_result):
        bslint.load_config_file(default_filepath=TEST_CONFIG_FILE_PATH)
        result = bslint.bslint.runner(brs_file_path).files
        self.assertEqual(exp_result, result)

    def spaces_around_operators(self, string, chars_index, exp_result):
        result = commands.check_spaces_around_operators(string, chars_index)
        self.assertEqual(result, exp_result)

    def spell_check(self, string, exp_result):
        result = commands.check_spelling(string, const.ID)
        self.assertEqual(result, exp_result)

    def lex_file(self, file, exp_result):
        file = open(file, "r+").read()
        result = Lexer().lex(file)
        self.assertEqual(result[self.WARNINGS], exp_result)
        self.assertEqual(result[self.STATUS], self.SUCCESS)

    def lex_string(self, string, exp_result):
        result = Lexer().lex(string)
        self.assertEqual(result[self.WARNINGS], exp_result)
        self.assertEqual(result[self.STATUS], self.SUCCESS)

    def lex_identifier(self, identifier, exp_result):
        lexer = Lexer()
        lexer.lex(identifier)
        self.assertEqual(lexer.statements_counter, exp_result)

    def match(self, identifier, match_group):
        result = regex_handler.find_match(identifier)
        self.assertEqual(result["match"].group(match_group), identifier)
        self.assertEqual(result["token_lexer_type"], const.ID)
        self.assertEqual(result["token_parser_type"], const.ID)
