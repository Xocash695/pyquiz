import yaml
import quiz
print(repr(list(quiz.REQUIRED_KEYS)))
raw = yaml.safe_load(open("questions.yaml"))
print(raw[0].keys())
