import numpy as np
import io
import pandas as pd


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


def arraytolist(data):
    Y = len(data)
    X = len(data[0])
    new = [[0 for i in range(X)] for j in range(Y)]
    for i in range(X):
        for j in range(Y):
            new[j][i] = data[j][i]
    return new


def normalize(data):
    Y = len(data)
    X = len(data[0])
    new = [[0 for i in range(X)] for j in range(Y)]
    for i in range(X):
        MIN = np.min(data[:][i])
        MAX = np.max(data[:][i])
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
            if wages[i] != 0:
                tmp += np.abs(data[j][i] - user_pick[i]) / wages[i]
        tmp /= np.sum(wages)
        tmp = round(tmp, 6)
        diff.append(tmp)
    return diff


def Pearson(user_pick, wages, data):
    Y = len(data)
    X = len(data[0])
    factors = []
    for j in range(Y):
        tmp = 0
        for i in range(X):
            i
    # return factors


def quicksort(tab, key):
    tab1 = tab[:]
    key1 = key[:]
    return quicksort_a(tab1, key1, 0, len(key) - 1)


def quicksort_a(tab, key, left, right):
    if right - 1 <= left:
        return tab, key
    pivot = key[int((left + right) / 2)]
    i = left
    j = right
    while 1:
        while pivot > key[i]:
            i = i + 1
        while pivot < key[j]:
            j = j - 1
        if i < j:
            temp = tab[i]
            tab[i] = tab[j]
            tab[j] = temp
            temp = key[i]
            key[i] = key[j]
            key[j] = temp
        else:
            break
    if j > left:
        tab, key = quicksort_a(tab, key, left, j)
    if i < right:
        tab, key = quicksort_a(tab, key, i, right)
    return tab, key


def merge_data(id, names, diff, data, features):
    for i in range(0, len(id)):
        data[i].insert(0, diff[i])
        data[i].insert(0, names[i])
        data[i].insert(0, id[i])
    data.insert(0, features)
    return data


def change_format(data):
    data[0].insert(0, "Pozycja")
    print(data[0])
    licznik = 0
    for i in range(1, len(data)):
        data[i][3] = int(data[i][3])
        if data[i][4] == 7:
            data[i][4] = "S"
        else:
            data[i][4] = chr(int(data[i][4]) + 64)
        data[i][6] = int(data[i][6])
        data[i][7] = int(data[i][7])
        data[i][8] = int(data[i][8])
        data[i][9] = int(data[i][9])
        data[i][11] = int(data[i][11])
        data[i][12] = int(data[i][12])
        data[i][13] = int(data[i][13])
        data[i][14] = int(data[i][14])
        data[i][15] = int(data[i][15])
        data[i][16] = int(data[i][16])
        data[i][17] = int(data[i][17])
        data[i][18] = int(data[i][18])
        data[i][19] = int(data[i][19])
        data[i][20] = int(data[i][20])
        data[i].insert(0, licznik)
        licznik += 1
        print(data[i])
    return data


def writetoexcel(data, path):
    df = pd.DataFrame(data)
    df.to_excel(excel_writer=path, sheet_name="ranking", index=False, header=False)

    print("Result saved")


data = readcsv("Dane.csv")
features = readtxt("Cechy.txt")
names = readtxt("Nazwy aut.txt")

features.insert(2, "Różnica (0-1)")

wages = [  # [0-3]
    1,  # year of production
    1,  # segment
    1,  # engine capacity
    1,  # number of cylinders
    1,  # power
    1,  # number of seats
    1,  # number of doors
    1,  # acceleration 0-100
    1,  # maximum speed
    1,  # torque
    1,  # curb weight
    1,  # trunk capacity
    1,  # tank capacity
    1,  # length
    1,  # width
    1,  # height
    1,  # wheelbase
    1,  # number of gears
]
user_values = [
    2010,  # year of production  [1955-2023]
    4,  # segment             [0-6]
    3,  # engine capacity     [0.0-8.4]
    6,  # number of cylinders [2-16]
    350,  # power               [76-1600]
    4,  # number of seats     [2-6]
    2,  # number of doors     [2-5]
    6.0,  # acceleration 0-100  [2.4-15.0]
    260,  # maximum speed       [154-492]
    450,  # torque              [107-1600]
    1600,  # curb weight         [655-2695]
    400,  # trunk capacity      [0-813]
    60,  # tank capacity       [0-159]
    450,  # length              [305-542]
    180,  # width               [140-223]
    130,  # height              [98-154]
    270,  # wheelbase           [204-305]
    6,  # number of gears     [2-9]
]
length = 251  # [3-251] number of records in the result

data = np.vstack([user_values, data])
names.insert(0, "Wartości użytkownika")

data = arraytolist(data)

normalized = normalize(data)
user_values_norm = normalized[0]

diff = difference(user_values_norm, wages, normalized)

id = list(range(len(diff)))

sorted_names, sorted_diff1 = quicksort(names, diff)
sorted_data, sorted_diff2 = quicksort(data, diff)
sorted_id, sorted_diff3 = quicksort(id, diff)

data = merge_data(sorted_id, sorted_names, sorted_diff1, sorted_data, features)

data = change_format(data[:length][:])

writetoexcel(data, "wyniki.xlsx")
