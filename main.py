def quicksort_prot(tab):
    right = len(tab) - 1
    left = 0
    pivot = tab[int((left + right) / 2)]
    i = left
    j = right
    while 1:
        while pivot > tab[i]:
            i = i + 1
        while pivot < tab[j]:
            j = j - 1
        if i <= j:
            temp = tab[i]
            tab[i] = tab[j]
            tab[j] = temp
        else:
            break
    if j > left:
        quicksort_prot(tab, left, j)
    if j > left:
        quicksort_prot(tab, i, right)
    return tab


print(quicksort_prot([6, 2, 1, 3, 5, 9, 4, 8, 7]))
