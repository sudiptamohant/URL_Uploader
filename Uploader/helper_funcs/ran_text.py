import random
import string


def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for _ in range(y))