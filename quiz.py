import json
import functools
import yaml
import sys
import pathlib

REQUIRED_KEYS = ("id", "topic", "code", "options", "answer", "why") #things we are looking for
LETTERS = ("A", "B", "C", "D") # anwser keys

class QuizError(Exception):
    """Questions are improperly formatted"""


def logged(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        shown = [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()] # formating things to be shown
        print(f"CALL {func.__name__}({', '.join(shown)})")
        result = func(*args, **kwargs) # get the result of the function
        print(f"RESULT: {result}") # show the result
        return result
    return wrapper


class Question:
    def __init__(self, data):

        pass

    def is_correct(self, letter):
        pass

def validate_questions(raw):

    def check_id(item, n):
        if "id" not in item:
            raise QuizError(f"item {n}: missing 'id'")
        question_id = item["id"]
        if not isinstance(question_id, int):
            raise QuizError(f"item {n}: id must be an integer, got {type(question_id).__name__}")
        if question_id != n:
            raise QuizError(f"item {n}: expected id {n}, got {question_id}")

    if not isinstance(raw, list):
        raise QuizError(f"top level must be a list, got {type(raw).__name__}")
    if len(raw) == 0:
        raise QuizError("the file contains nothing")
    for n, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise QuizError(f"item {n}: expected a mapping, got {type(item).__name__}")
        check_id(item, n)

    return raw


def load_questions(path):
    try:
        with open(path, 'r') as f:          # open the file
            raw = yaml.load(f, Loader=yaml.SafeLoader)       # parse the YAML from f
    except OSError as e:            # file problems (missing, unreadable, a folder)
        raise QuizError(f"cannot read {path}: {e}") from e
    except yaml.YAMLError as e:            # the file opened but the YAML is broken
        raise QuizError(f"invalid YAML in {path}: {e}") from e
    return raw



def ask(question):
    pass


def run_round(questions):
    pass


def save_results(path, scores):
    pass


def log_attempt(path, line):
    pass

def get_questions_fileName():
    """Get the name of the questions file """
    numArg = len(sys.argv) # get the max number
    if numArg != 2 :
        print("usage: python PA1_Kallumkal.py QUESTIONS.YAML") # show the correct usage
        sys.exit(2) #give the exit code 2 if not correct
    return sys.argv[1]

def file_exists(filename):
    """Checks if the file actually exists"""
    if not pathlib.Path(filename).exists():
        print("File does not exist: ", filename)
        sys.exit(1)

def main():
    file_name = get_questions_fileName()
    file_exists(file_name)
    try:
        questions = load_questions(file_name)
        validate_questions(questions)
    except QuizError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)


    # validate_questions("hello")               # fails the first check: top level
    #validate_questions([{"id": 1}, "oops"])   # passes the first, fails the second: item 2



if __name__ == "__main__":
    main()
