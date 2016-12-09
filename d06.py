from collections import Counter

test_input = ("eedadn\n"
              "drvtee\n"
              "eandsr\n"
              "raavrd\n"
              "atevrs\n"
              "tsrnev\n"
              "sdttsa\n"
              "rasrtv\n"
              "nssdts\n"
              "ntnada\n"
              "svetve\n"
              "tesnvt\n"
              "vntsnd\n"
              "vrdear\n"
              "dvrsen\n"
              "enarar")

with open('d06.txt') as f:
    real_input = f.read()

instr = real_input

letter_counts = [Counter() for _ in range(instr.find('\n'))]

for line in instr.splitlines():
    for c, count in zip(line, letter_counts):
        count.update(c)

most_common = [count.most_common()[-1] for count in letter_counts]
print(''.join(c for (c, n) in most_common), end='\n\n')
