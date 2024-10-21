import io
import unittest
from src.InvertedIndexes import normalize_text, check_consecutive_words, process_file_for_phrase, search_phrase_with_scores
from collections import defaultdict
import os
from contextlib import redirect_stdout

class TestInvertedIndex(unittest.TestCase):

    def test_normalize_text(self):
        """
        Test the normalize_text function to ensure it removes punctuation, collapses spaces, and converts to lowercase.
        """
        self.assertEqual(normalize_text("Hello, world!"), "hello world")
        self.assertEqual(normalize_text("  This    is    a  test   "), "this is a test")
        self.assertEqual(normalize_text("Normalize? Text. With Punctuation!"), "normalize text with punctuation")

    def test_check_consecutive_words(self):
        """
        Test that check_consecutive_words correctly identifies if a phrase appears consecutively in a line.
        """
        line = "This is a simple sentence."
        phrase = "this is"
        self.assertTrue(check_consecutive_words(line, phrase))

        phrase = "simple sentence"
        self.assertTrue(check_consecutive_words(line, phrase))

        phrase = "not in line"
        self.assertFalse(check_consecutive_words(line, phrase))

    def test_process_file_for_phrase(self):
        """
        Test the process_file_for_phrase function to ensure it correctly finds occurrences of a phrase in specific lines.
        """
        # Simulating a file content
        filename = 'test.txt'
        directory = 'test_directory'
        phrase = "this is"
        line_numbers = [1, 3]

        # Ensure the directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Mocking the file content
        with open(f"{directory}/{filename}", 'w') as f:
            f.write("This is a simple test file.\n")
            f.write("It has several lines of text.\n")
            f.write("This is the third line.\n")

        result = process_file_for_phrase(filename, line_numbers, phrase, directory)

        # Expected results for the phrase "this is"
        expected_results = [
            (filename, 1, "This is a simple test file."),
            (filename, 3, "This is the third line.")
        ]
        self.assertEqual(result, expected_results)

    def test_search_phrase(self):
        """
        Test the search_phrase function to ensure it works correctly.
        """
        # Creating a mock inverted index
        inverted_index = defaultdict(list)
        inverted_index['this'].append(('test.txt', 1))
        inverted_index['is'].append(('test.txt', 1))
        inverted_index['a'].append(('test.txt', 1))
        inverted_index['test'].append(('test.txt', 1))

        directory = 'test_directory'
        phrase = "this is"

        # Ensure the directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Create a test file in the directory
        with open(f"{directory}/test.txt", 'w') as f:
            f.write("This is a test line in a test file.\n")

        # Capture output during search using contextlib.redirect_stdout
        captured_output = io.StringIO()  # Create StringIO object to capture print output
        with redirect_stdout(captured_output):  # Redirect stdout to captured_output
            search_phrase_with_scores(phrase, inverted_index, directory)  # Run the function

        output = captured_output.getvalue()  # Retrieve the printed output

        # Check if the output contains the expected line
        self.assertIn("File: test.txt, Line 1: This is a test line in a test file.", output)