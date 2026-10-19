import json
import functools
import yaml
import random

REQUIRED_KEYS = ("id", "question", "options", "answer") #things we are looking for
LETTERS = ("A", "B", "C", "D") # anwser keys
OPTIONAL_KEYS = ("topic", "why")
DEFAULT_SETTINGS = {"shuffle_questions": False, "shuffle_options": False}

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
        self.id = data["id"]
        self.question = data["question"]
        self.options = data["options"]
        self.answer = data["answer"] # this means that it should exist
        self.topic = data.get("topic")
        self.why = data.get("why") # .get basically says that this may not exist if it doesn't it gives none

    def is_correct(self, letter):
        pass



def validate_file(raw):
    def check_settings(settings):
        if not isinstance(settings, dict):
            raise QuizError(f"settings must be a mapping, got {type(settings).__name__}")
        unknown = settings.keys() - DEFAULT_SETTINGS.keys()
        if unknown:
            raise QuizError(f"settings: unknown key(s) {', '.join(sorted(unknown))}")
        for key, value in settings.items():
            if not isinstance(value, bool):
                raise QuizError(f"settings: {key} must be true or false, got {type(value).__name__}")
    if not isinstance(raw, dict):
        raise QuizError(f"top level must be a mapping, got {type(raw).__name__}")
    if "questions" not in raw:
        raise QuizError("missing 'questions'")

    settings = raw.get("settings", {})
    check_settings(settings)

    questions = validate_questions(raw["questions"]) # we pass the questions portion to the question validation system

    merged_settings = dict(DEFAULT_SETTINGS) # create dict with the current settings
    merged_settings.update(settings) # update the settings based on what we have
    return merged_settings, questions # return the settings and the questions seperatly


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
        check_text(item, n, "question") # check that the question portion has something there to quiz the person
        check_options(item, n) # check that there is valid options labeled in capital letters "A", "B", "C", etc
        check_answer(item, n) # check that there is valid anwser option like "A"
        # print(item, "\n")

    return raw


def load_questions(path):
    try:
        with open(path, 'r') as f:
            raw = yaml.safe_load(f)
    except OSError as e:
        raise QuizError(f"cannot read {path}: {e}") from e
    except yaml.YAMLError as e:
        raise QuizError(f"invalid YAML in {path}: {e}") from e

    settings, validated = validate_file(raw) # run all the validation and get back the settings and the validated questions
    questions = [Question(item) for item in validated] # create objects of Question

    if settings["shuffle_questions"]:
        questions = random.sample(questions, len(questions)) #return

    return settings, questions



def ask(question):

    pass


def run_round(questions):
    pass


def save_results(path, scores):
    pass


def log_attempt(path, line):
    pass
