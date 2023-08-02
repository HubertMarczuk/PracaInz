def quicksort_prot(tab, left, right):
    print(right)
    print(left)
    if right <= left:
        return
    pivot = tab[int((left + right) / 2)]
    i = left
    j = right
    k = 0
    while 1:
        while pivot > tab[i]:
            i = i + 1
        while pivot < tab[j]:
            j = j - 1
        k += 1
        if i <= j:
            print(i)
            print(j)
            temp = tab[i]
            tab[i] = tab[j]
            tab[j] = temp
            print(tab)
        else:
            break
    if j > left:
        quicksort_prot(tab, left, j)
    if i < right:
        quicksort_prot(tab, i, right)
    return tab


print(
    quicksort_prot([5, 2, 1, 3, 6, 9, 4, 8, 7], 0, len([5, 2, 1, 3, 6, 9, 4, 8, 7]) - 1)
)
