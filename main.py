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
    diff = []
    for j in range(Y):
        tmp = 0
        for i in range(X):
            tmp += wages[i] * np.abs(data[j][i] - user_pick[i])
        tmp /= np.sum(wages)
        diff.append(tmp)
    return diff


def quicksort(tab, key):
    tab1 = tab[:]
    key1 = key[:]
    return quicksort_a(tab1, key1, 0, len(key) - 1)


def quicksort_a(tab, key, left, right):
    if right - 1 <= left:
        return
    pivot = key[int((left + right) / 2)]
    i = left
    j = right
    while 1:
        while pivot > key[i]:
            i = i + 1
        while pivot < key[j]:
            j = j - 1
        if i < j:
            print(tab[i])
            print(tab[j])
            print()
            # temp = tab[i][:]
            # tab[i][:] = tab[j][:]
            # tab[j][:] = temp
            tab[[i, j]] = tab[[j, i]]
            temp = key[i]
            key[i] = key[j]
            key[j] = temp
            print(tab[i])
            print(tab[j])
            print()
        else:
            break
    if j > left:
        tab, key = quicksort_a(tab, key, left, j)
    if i < right:
        tab, key = quicksort_a(tab, key, i, right)
    return tab, key


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
length = 5

data = np.vstack([user_values, data])
names.insert(0, "Wartości użytkownika")

normalized = normalize(data)
user_values_norm = normalized[0]

diff = difference(user_values_norm, wages, normalized)

# sorted_normalized, sorted_diff = quicksort(normalized, diff)
# sorted_names, sorted_diff1 = quicksort(names, diff)
sorted_data, sorted_diff2 = quicksort(data, diff)
# print(sorted_normalized[:length][:])
# print()
# print(normalized[:length][:])
# print()
# print(sorted_names[:length][:])
# print(data[:length][:])
# print()
print(sorted_data[:length][:])
print()
print(data[:length][:])


# print(normalized[:length][:])
# normalized[[0, 1]] = normalized[[1, 0]]
# print()
# print(normalized[:length][:])
