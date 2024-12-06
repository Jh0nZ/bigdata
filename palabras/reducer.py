import sys
from collections import defaultdict

word_counts = defaultdict(int)

for line in sys.stdin:
    try:
        word, count = line.strip().split("\t")
        word_counts[word] += int(count)
    except Exception as e:
        continue

# Encontrar la palabra más mencionada
most_common_word = max(word_counts.items(), key=lambda x: x[1])

print(f"{most_common_word[0]}\t{most_common_word[1]}")
