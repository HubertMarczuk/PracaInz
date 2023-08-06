import pandas as pd


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


def readcsv(path):
    data = pd.read_csv(path, header=None)
    return data


# tab = quicksort_prot([9, 8, 7, 6, 5, 4, 3, 2], 0, 7)
# print(tab)

normalized = readcsv("Znormalizowane.csv")
features = readcsv("Cechy.csv")
names = readcsv("Nazwy aut.csv")

print(normalized)
print(features)
print(names)
