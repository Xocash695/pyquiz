from quiz import NoAnswerError, retry

attempts = [0]

def flaky():
    attempts[0] += 1
    if attempts[0] < 3:
        raise NoAnswerError("nope")
    return "ok"

flaky = retry(times=3)(flaky)
print(flaky())
