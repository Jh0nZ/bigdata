import sys
import re
from itertools import groupby

def mapper():
    for line in sys.stdin:
        palabras = line.split()
        for palabra in palabras:
            palabra = palabra.lower()
            palabra = palabra.strip('.,!?"\'')
            if palabra:
                print(f"{palabra}\t1")

def reducer():
    current_word = None
    current_count = 0
    for line in sys.stdin:
        palabra, count = line.strip().split('\t')
        count = int(count)
        if current_word == palabra:
            current_count += count
        else:
            if current_word:
                print(f"{current_word}\t{current_count}")
            current_word = palabra
            current_count = count
    if current_word == palabra:
        print(f"{current_word}\t{current_count}")

if __name__ == "__main__":
    if sys.argv[1] == '-m':
        mapper()
    elif sys.argv[1] == '-r':
        reducer()