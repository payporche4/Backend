import random


def generate_referal_code():
    return int("".join([str(random.randint(0, 10)) for _ in range(6)]))


def generate_otp():
    return int("".join([str(random.randint(0, 9)) for _ in range(5)]))
