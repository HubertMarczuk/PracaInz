import numpy as np
import io


def readcsv(path):
    CSV = open(path)
    data = np.loadtxt(CSV, delimiter=";")
    return data


def readtxt(path):
    stream = io.open(path, "rt", encoding="utf8")
    text = stream.readlines()
    for i in range(len(text)):
        text[i] = text[i].replace("\n", "")
    return text


def normalize(data):
    Y, X = data.shape
    new = [[0 for i in range(X)] for j in range(Y)]
    for i in range(X):
        MIN = np.min(data[:, i])
        MAX = max(data[:, i])
        for j in range(Y):
            tmp = (data[j][i] - MIN) / (MAX - MIN)
            new[j][i] = tmp
    return new


def difference(user_pick, wages, data):
    Y = len(data)
    X = len(data[0])
    print(Y, X)
    diff = []
    for j in range(Y):
        tmp = 0
        for i in range(X):
            tmp += wages[i] * np.abs(data[j][i] - user_pick[i])
        tmp /= np.sum(wages)
        diff.append(tmp)
    return diff


def quicksort_prot(tab, left, right):
    if right - 1 <= left:
        return
    pivot = tab[int((left + right) / 2)]
    i = left
    j = right
    while 1:
        while pivot > tab[i]:
            i = i + 1
        while pivot < tab[j]:
            j = j - 1
        if i < j:
            temp = tab[i]
            tab[i] = tab[j]
            tab[j] = temp
        else:
            break
    if j > left:
        quicksort_prot(tab, left, j)
    if i < right:
        quicksort_prot(tab, i, right)
    return tab


data = readcsv("Dane.csv")
features = readtxt("Cechy.txt")
names = readtxt("Nazwy aut.txt")

wages = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
user_values = [
    2010,
    4,
    3,
    6,
    350,
    4,
    2,
    6.0,
    260,
    450,
    1600,
    400,
    60,
    450,
    180,
    130,
    270,
    6,
]
length = 40

data = np.vstack([user_values, data])

normalized = normalize(data)
user_values_norm = normalized[0]

diff = difference(user_values_norm, wages, normalized)

# tab = quicksort_prot([9, 8, 7, 6, 5, 4, 3, 2], 0, 7)
# print(tab)
