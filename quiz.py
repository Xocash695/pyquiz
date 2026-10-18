import json
import functools
import yaml
import sys
import pathlib

REQUIRED_KEYS = ("id", "code", "options", "answer") #things we are looking for
LETTERS = ("A", "B", "C", "D") # anwser keys
OPTIONAL_KEYS = ("topic", "why")
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

        question_id = item["id"]
        if not isinstance(question_id, int):
            raise QuizError(f"item {n}: id must be an integer, got {type(question_id).__name__}")
        if question_id != n:
            raise QuizError(f"item {n}: expected id {n}, got {question_id}")
    def check_keys(item, n):
        """Check that the correct keys are present"""
        allowed = set(REQUIRED_KEYS) | set(OPTIONAL_KEYS)
        missing = set(REQUIRED_KEYS) - item.keys()
        unknown = item.keys() - allowed
        if missing:
            raise QuizError(f"item {n}: missing key(s) {', '.join(sorted(missing))}")
        if unknown:
            raise QuizError(f"item {n}: unknown key(s) {', '.join(sorted(unknown))}")

    def check_options(item, n):
        options = item["options"]
        if not isinstance(options, dict):
            raise QuizError(f"item {n}: options must be a mapping, got {type(options).__name__}")
        if len(options) < 2:
            raise QuizError(f"item {n}: need at least 2 options, got {len(options)}")
        expected = LETTERS[:len(options)]
        if tuple(options.keys()) != expected:
            raise QuizError(f"item {n}: option labels must be {', '.join(expected)} in order, got {', '.join(map(str, options.keys()))}")
        for label, text in options.items():
            if not isinstance(text, str) or text.strip() == "":
                raise QuizError(f"item {n}: option {label} must be non-empty text")
    def check_answer(item, n):
        answer = item["answer"]
        valid = tuple(item["options"].keys())
        if isinstance(answer, str):
            answer = [answer]
        if not isinstance(answer, list) or len(answer) == 0:
            raise QuizError(f"item {n}: answer must be a list of letters, got {answer!r}")
        for letter in answer:
            if letter not in valid:
                raise QuizError(f"item {n}: answer must be one of {', '.join(valid)}, got {letter!r}")
        if len(set(answer)) != len(answer):
            raise QuizError(f"item {n}: answer lists the same letter twice")
    def check_text(item, n, key):
        value = item[key]
        if not isinstance(value, str):
            raise QuizError(f"item {n}: {key} must be text, got {type(value).__name__}")
        if value.strip() == "":
            raise QuizError(f"item {n}: {key} must not be empty")
    def drop_blank_optional(item, n):
        for key in OPTIONAL_KEYS:
            if key not in item:
                continue
            value = item[key]
            if value is None or (isinstance(value, str) and value.strip() == ""):
                del item[key]
            elif not isinstance(value, str):
                raise QuizError(f"item {n}: {key} must be text, got {type(value).__name__}")


    if not isinstance(raw, list):
        raise QuizError(f"top level must be a list, got {type(raw).__name__}")
    if len(raw) == 0:
        raise QuizError("the file contains nothing")
    for n, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise QuizError(f"item {n}: expected a mapping, got {type(item).__name__}")
        check_keys(item, n) # check that the essential keys are there
        check_id(item, n) # check that the id of the item works fine
        drop_blank_optional(item, n) # if any optionals are left empty then delete it from the item cause it doesn't matter
        check_text(item, n, "code") # check that the code portion has something there to quiz the person
        check_options(item, n) # check that there is valid options labeled in capital letters "A", "B", "C", etc
        check_answer(item, n) # check that there is valid anwser option like "A"
        # print(item, "\n")

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
