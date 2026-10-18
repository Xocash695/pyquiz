import json

import yaml


class QuizError(Exception):
    """Questions are improperly formatted"""



class Question:
    def __init__(self, data):
        pass

    def is_correct(self, letter):
        pass


def load_questions(path):
    pass


def ask(question):
    pass


def run_round(questions):
    pass


def save_results(path, scores):
    pass


def log_attempt(path, line):
    pass


def main():
    pass


if __name__ == "__main__":
    main()
