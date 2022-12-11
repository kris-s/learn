
from pathlib import Path
import re


print("\n🎄 It's time to save Christmas. 🎄")


def load(path):
    path = Path(path)
    return path.read_text()


SAMPLE = load('sample.txt')
INPUT = load('input.txt')


def day_11(text):
    lines = text.splitlines()


day_11(SAMPLE)
# day_11(INPUT)
