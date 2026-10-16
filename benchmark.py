import time
import random
import matplotlib.pyplot as plt
import trie_index
import bst_index
import dict_index

SIZES = [1000, 5000, 10000, 50000, 100000, 500000]  # distinct words
TOTAL = 1000000
CHARS = [chr(i) for i in range(33, 127) if chr(i) not in ".,:;"]


def make_file(filename, distinct):
    vocab = set()
    while len(vocab) < distinct:
        vocab.add("".join(random.choices(CHARS, k=random.randint(4, 10))))
    vocab = list(vocab)
    words = vocab + random.choices(vocab, k=TOTAL - distinct)
    random.shuffle(words)
    f = open(filename, "w")
    for i in range(0, TOTAL, 10):
        f.write(" ".join(words[i:i + 10]) + "\n")
    f.close()
    return vocab


modules = {"Trie": trie_index, "BST": bst_index, "Dict": dict_index}
times = {}
for name in modules:
    times[name] = {"build": [], "search": [], "print": []}

for d in SIZES:
    filename = "words_" + str(d) + ".txt"
    vocab = make_file(filename, d)
    queries = random.choices(vocab, k=100000)
    print("Distinct words:", d)
    for name in modules:
        m = modules[name]

        t = time.time()
        index = m.build(filename)
        t_build = time.time() - t

        t = time.time()
        for w in queries:
            m.search(index, w)
        t_search = time.time() - t

        t = time.time()
        m.write(index, "out_" + name + ".txt")
        t_print = time.time() - t

        times[name]["build"].append(t_build)
        times[name]["search"].append(t_search)
        times[name]["print"].append(t_print)
        print(" ", name, round(t_build, 2), round(t_search, 2), round(t_print, 2))

titles = {"build": "Construction time", "search": "Search time", "print": "Printing time"}
plt.figure(figsize=(15, 4))
n = 1
for key in ["build", "search", "print"]:
    plt.subplot(1, 3, n)
    n += 1
    for name in modules:
        plt.plot(SIZES, times[name][key], marker="o", label=name)
    plt.title(titles[key])
    plt.xlabel("Distinct words")
    plt.ylabel("Time (s)")
    plt.xscale("log")
    plt.legend()
plt.tight_layout()
plt.savefig("performance.png")
plt.show()
