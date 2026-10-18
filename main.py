import quiz
import sys
import pathlib

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
        settings, questions = quiz.load_questions(file_name)
    except quiz.QuizError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
    for n, q in enumerate(questions, start=1):
        print(f"{n}. {q.question}")


if __name__ == "__main__":
    main()
