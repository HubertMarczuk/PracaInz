from tkinter import *
from tkinter import messagebox
import numpy as np
import io
import pandas as pd


class EmptyFieldError(Exception):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class NonIntegerError(Exception):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class NonFractionalError(Exception):
    def __init__(self, name):
        self.name = name


class NotTheLetterError(Exception):
    def __init__(self, name):
        self.name = name


class OutOfRangeError(Exception):
    def __init__(self, name, type, min, max):
        self.name = name
        self.type = type
        self.min = min
        self.max = max


class CarRecommendation(object):
    def __init__(self):
        self.window = Tk()
        self.window.geometry("600x600")
        self.window.title("Rekomendacja samochodów")
        self.ReadData()
        self.CountMinMax()
        self.BuildWindow()
        self.window.mainloop()

    def ReadData(self):
        self.data = Readcsv("Dane.csv")
        self.features = Readtxt("Cechy.txt")
        self.names = Readtxt("Nazwy aut.txt")

        self.features.insert(2, "Kryterium główne")

    def Readcsv(path):
        CSV = open(path)
        data = np.loadtxt(CSV, delimiter=";")
        return data

    def Readtxt(path):
        stream = io.open(path, "rt", encoding="utf8")
        text = stream.readlines()
        for i in range(len(text)):
            text[i] = text[i].replace("\n", "")
        return text

    def CountMinMax(self):
        self.min = []
        self.max = []
        for i in range(len(self.data[0])):
            min_tmp = self.data[0][i]
            max_tmp = self.data[0][i]
            for j in range(len(self.data)):
                if self.data[j][i] < min_tmp:
                    min_tmp = self.data[j][i]
                if self.data[j][i] > max_tmp:
                    max_tmp = self.data[j][i]
            self.min.append(min_tmp)
            self.max.append(max_tmp)

    def BuildWindow(self):
        field_width = 20
        self.success_text = "Zrekomendowano!"
        self.labels = [None] * 18
        self.etiquettes = [None] * 18
        self.text = [
            "Rok produkcji",
            "Segment",
            "Pojemność silnika [l]",
            "Liczba cylindrów",
            "Moc [KM]",
            "Liczba miejsc",
            "Liczba drzwi",
            "Przyspieszenie 0-100km/h [s]",
            "Prędkość maksymalna [km/h]",
            "Moment obrotowy [Nm]",
            "Masa własna [kg]",
            "Pojemnośc bagażnika [l]",
            "Pojemność baku [l]",
            "Długość [cm]",
            "Szerokość [cm]",
            "Wysokość [cm]",
            "Rozstaw osi [cm]",
            "Liczba biegów",
        ]
        for i in range(len(self.etiquettes)):
            min = self.min[i]
            max = self.max[i]
            if i != 2 and i != 7:
                min = int(min)
                max = int(max)
            if i == 1:
                self.etiquettes[i] = self.text[i] + " (A,B,...,F,S):"
            else:
                self.etiquettes[i] = (
                    self.text[i] + " (" + str(min) + "-" + str(max) + "):"
                )

        self.user_values = [0] * 18
        self.gap = [0] * 18
        self.weights = [0] * 18

        self.label_criteria_names = Label(self.window)
        self.label_criteria_names["text"] = "Nazwy kryteriów do podania"
        self.label_criteria_names.grid(row=0, column=0, sticky=W)

        self.label_criteria_value = Label(self.window)
        self.label_criteria_value["text"] = "Wartości kryteriów"
        self.label_criteria_value.grid(row=0, column=1, sticky=W)

        self.label_criteria_weights = Label(self.window)
        self.label_criteria_weights["text"] = "Wagi kryteriów (0-3)"
        self.label_criteria_weights.grid(row=0, column=3, sticky=W)

        for i in range(18):
            self.labels[i] = Label(self.window)
            self.labels[i]["text"] = self.etiquettes[i]
            self.labels[i].grid(row=i + 1, column=0, sticky=W)

            self.user_values[i] = Entry(self.window, width=field_width)
            self.user_values[i].grid(row=i + 1, column=1, sticky=W)

            self.gap[i] = Label(self.window)
            self.gap[i]["text"] = "      "
            self.gap[i].grid(row=i + 1, column=2, sticky=W)

            self.weights[i] = Entry(self.window, width=field_width)
            self.weights[i].grid(row=i + 1, column=3, sticky=W)

        self.gap1 = Label(self.window)
        self.gap1["text"] = ""
        self.gap1.grid(row=19, column=0, sticky=W)

        self.length_label = Label(self.window)
        self.length_label["text"] = (
            "Liczba rekomendowanych aut (1-" + str(len(self.data)) + "):"
        )
        self.length_label.grid(row=20, column=0, sticky=W)

        self.length = Entry(self.window, width=field_width)
        self.length.grid(row=20, column=1, sticky=W)

        self.gap2 = Label(self.window)
        self.gap2["text"] = ""
        self.gap2.grid(row=21, column=0, sticky=W)

        self.accept_button = Button(self.window, width=field_width)
        self.accept_button["text"] = "Rekomenduj"
        self.accept_button["command"] = self.CheckErrors
        self.accept_button.grid(row=22, column=0, sticky=W)

        self.done_text = Label(self.window)
        self.done_text["text"] = ""
        self.done_text.grid(row=22, column=1, sticky=W)

    def CheckErrors(self):
        try:
            for i in range(18):
                if self.user_values[i].get() == "":
                    raise EmptyFieldError(self.text[i], "Wartość")
                if self.weights[i].get() == "":
                    raise EmptyFieldError(self.text[i], "Waga")
                if i == 1:
                    if (
                        self.user_values[i].get() != "A"
                        and self.user_values[i].get() != "B"
                        and self.user_values[i].get() != "C"
                        and self.user_values[i].get() != "D"
                        and self.user_values[i].get() != "E"
                        and self.user_values[i].get() != "F"
                        and self.user_values[i].get() != "S"
                    ):
                        raise NotTheLetterError("e")
                elif i == 2 or i == 7:
                    if self.user_values[i].get().find(".") == -1:
                        raise NonFractionalError(self.text[i])
                    if (
                        float(self.user_values[i].get()) > self.max[i]
                        or float(self.user_values[i].get()) < self.min[i]
                    ):
                        raise OutOfRangeError(
                            self.text[i], "Wartość", self.min[i], self.max[i]
                        )
                else:
                    if self.user_values[i].get().find(".") != -1:
                        print(self.user_values[i].get())
                        print(self.user_values[i].get()).find(".")
                        raise NonIntegerError(self.text[i], "Wartość")
                    if (
                        int(self.user_values[i].get()) > self.max[i]
                        or int(self.user_values[i].get()) < self.min[i]
                    ):
                        raise OutOfRangeError(
                            self.text[i], "Wartość", int(self.min[i]), int(self.max[i])
                        )
                if self.weights[i].get().find(".") != -1:
                    raise NonIntegerError(self.text[i], "Waga")
                if int(self.weights[i].get()) > 3 or int(self.weights[i].get()) < 0:
                    raise OutOfRangeError(self.text[i], "Waga", 0, 3)
            if self.length.get() == "":
                raise EmptyFieldError("Liczba rekomendowanych aut", "Wartość")
            if self.length.get().find(".") != -1:
                raise NonIntegerError("Liczba rekomendowanych aut", "Wartość")
            if int(self.length.get()) < 0 or int(self.length.get()) > len(self.data):
                raise OutOfRangeError(
                    "Liczba rekomendowanych aut", "Wartość", 0, len(self.data)
                )
            # else:
            # self.Rekomenduj()

        except EmptyFieldError as e:
            messagebox.showerror(
                "Błąd", e.type + " kryterium " + e.name + " nie może być pusta!"
            )

        except ValueError as e:
            messagebox.showerror(
                "Błąd",
                "Wszystkie wartości poza wartością kryterium Segment oraz wszystkie wagi muszą być liczbami!",
            )

        except NonFractionalError as e:
            messagebox.showerror(
                "Błąd",
                "Wartość kryterium "
                + e.name
                + " musi być liczbą niecałkowitą z jednym miejscem po kropce!",
            )

        except NonIntegerError as e:
            messagebox.showerror(
                "Błąd",
                e.type
                + " kryterium "
                + e.name
                + " musi być całkowitą, pisaną bez kropki!",
            )

        except NotTheLetterError as e:
            messagebox.showerror(
                "Błąd",
                "Wartość kryterium Segment musi być literą z zakresu (A,B,...,F,S)!",
            )

        except OutOfRangeError as e:
            messagebox.showerror(
                "Błąd",
                e.type
                + " kryterium "
                + e.name
                + " musi mieścić się w zakresie ("
                + str(e.min)
                + "-"
                + str(e.max)
                + ")!",
            )

    def Rekomenduj():
        data = np.vstack([user_values, data])
        names.insert(0, "Wartości użytkownika")

        data = Clonetolist(data)

        normalized = Normalize(data)
        user_values_norm = normalized[0]

        dist = Distance(user_values_norm, weights, normalized)
        pearson = Pearson(user_values_norm, weights, normalized)
        kendall = Kendall(user_values_norm, weights, normalized)

        id = list(range(len(data)))

        sorted_names_d, sorted_dist = Quicksort(names, dist)
        sorted_data_d, sorted_dist = Quicksort(data, dist)
        sorted_id_d, sorted_dist = Quicksort(id, dist)

        sorted_names_p, sorted_pear = Quicksort(names, pearson)
        sorted_data_p, sorted_pear = Quicksort(data, pearson)
        sorted_id_p, sorted_pear = Quicksort(id, pearson)

        sorted_names_p.reverse()
        sorted_data_p.reverse()
        sorted_id_p.reverse()
        sorted_pear.reverse()

        sorted_names_k, sorted_kend = Quicksort(names, kendall)
        sorted_data_k, sorted_kend = Quicksort(data, kendall)
        sorted_id_k, sorted_kend = Quicksort(id, kendall)

        sorted_names_k.reverse()
        sorted_data_k.reverse()
        sorted_id_k.reverse()
        sorted_kend.reverse()

        data_d = Merge_data(
            sorted_id_d, sorted_names_d, sorted_dist, sorted_data_d, features
        )
        data_p = Merge_data(
            sorted_id_p, sorted_names_p, sorted_pear, sorted_data_p, features
        )
        data_k = Merge_data(
            sorted_id_k, sorted_names_k, sorted_kend, sorted_data_k, features
        )

        data_d = Change_format(data_d[:length][:])
        data_p = Change_format(data_p[:length][:])
        data_k = Change_format(data_k[:length][:])

        data_d[0][3] = "Odleglość"
        data_p[0][3] = "Podobieństwo"
        data_k[0][3] = "Estymator tau"

        Display(data_d)
        Display(data_p)
        Display(data_k)

        Writetoexcel(data_d, "wyniki_odleglosc.xlsx")
        Writetoexcel(data_p, "wyniki_pearson.xlsx")
        Writetoexcel(data_k, "wyniki_kendall.xlsx")

    def Clonetolist(data):
        Y = len(data)
        X = len(data[0])
        new = [[0 for i in range(X)] for j in range(Y)]
        for i in range(X):
            for j in range(Y):
                new[j][i] = data[j][i]
        return new

    def Normalize(data):
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

    def Distance(user_pick, weights, data):
        Y = len(data)
        X = len(data[0])
        dist = []
        for j in range(Y):
            tmp = 0
            for i in range(X):
                if weights[i] != 0:
                    tmp += pow(np.abs(data[j][i] - user_pick[i]) / weights[i], 2)
            tmp = pow(tmp, 0.5)
            tmp = round(tmp, 3)
            dist.append(tmp)
        return dist

    def Pearson(user_pick, weights, data):
        Y = len(data)
        X = len(data[0])
        data = Multiply_weights_2dim(data, weights)
        user_pick = Multiply_weights(user_pick, weights)
        factors = []
        avg_user = Average(user_pick)
        sum_den_user = 0
        for i in range(X):
            sum_den_user += pow(user_pick[i] - avg_user, 2)
        sum_den_user = pow(sum_den_user, 0.5)
        for j in range(Y):
            sum_num = 0
            sum_den_x = 0
            avg_x = Average(data[j])
            for i in range(X):
                sum_num += (data[j][i] - avg_x) * (user_pick[i] - avg_user)
                sum_den_x += pow(data[j][i] - avg_x, 2)
            sum_den_x = pow(sum_den_x, 0.5)
            tmp = sum_num / (sum_den_x * sum_den_user)
            tmp = round(tmp, 6)
            factors.append(tmp)
        return factors

    def Kendall(user_pick, weights, data):
        Y = len(data)
        X = len(data[0])
        data = Multiply_weights_2dim(data, weights)
        user_pick = Multiply_weights(user_pick, weights)
        tau = []
        tau.append(1)
        for j in range(1, Y):
            P = 0
            Q = 0
            T = 0
            for i in range(X):
                for k in range(X):
                    if i > k:
                        det = (data[j][i] - data[j][k]) * (user_pick[i] - user_pick[k])
                        if det == 0:
                            T += 1
                        if det > 0:
                            P += 1
                        else:
                            Q += 1
            tmp = (P - Q) / (P + Q + T)
            tmp = round(tmp, 6)
            tau.append(tmp)
        return tau

    def Multiply_weights_2dim(data, weights):
        for j in range(len(data)):
            for i in range(len(data[0])):
                data[j][i] *= weights[i] / 3
        return data

    def Multiply_weights(tab, weights):
        for i in range(len(tab)):
            tab[i] *= weights[i] / 3
        return tab

    def Average(tab):
        sum = 0
        for i in range(len(tab)):
            sum += tab[i]
        return sum / len(tab)

    def Quicksort(tab, key):
        return Quicksort_a(tab[:], key[:], 0, len(key) - 1)

    def Quicksort_a(tab, key, left, right):
        if right <= left:
            return tab, key
        pivot = key[int((left + right) / 2)]
        i = left - 1
        j = right + 1
        while 1:
            while 1:
                i += 1
                if pivot <= key[i]:
                    break
            while 1:
                j -= 1
                if pivot >= key[j]:
                    break
            if i <= j:
                temp = tab[i]
                tab[i] = tab[j]
                tab[j] = temp
                temp = key[i]
                key[i] = key[j]
                key[j] = temp
            else:
                break
        if j > left:
            tab, key = Quicksort_a(tab, key, left, j)
        if i < right:
            tab, key = Quicksort_a(tab, key, i, right)
        return tab, key

    def Merge_data(id, names, criterion, data, features_arg):
        data = Clonetolist(data)
        features = features_arg.copy()
        for i in range(0, len(id)):
            data[i].insert(0, criterion[i])
            data[i].insert(0, names[i])
            data[i].insert(0, id[i])
            data[i].insert(0, i)
        features.insert(0, "Pozycja")
        data.insert(0, features)
        return data

    def Change_format(data):
        for i in range(1, len(data)):
            data[i][4] = int(data[i][4])
            if data[i][5] == 7:
                data[i][5] = "S"
            else:
                data[i][5] = chr(int(data[i][5]) + 64)
            data[i][7] = int(data[i][7])
            data[i][8] = int(data[i][8])
            data[i][9] = int(data[i][9])
            data[i][10] = int(data[i][10])
            data[i][12] = int(data[i][12])
            data[i][13] = int(data[i][13])
            data[i][14] = int(data[i][14])
            data[i][15] = int(data[i][15])
            data[i][16] = int(data[i][16])
            data[i][17] = int(data[i][17])
            data[i][18] = int(data[i][18])
            data[i][19] = int(data[i][19])
            data[i][20] = int(data[i][20])
        return data

    def Display(data):
        for row in data:
            print(row)
        print()

    def Writetoexcel(data, path):
        df = pd.DataFrame(data)
        df.to_excel(excel_writer=path, sheet_name="ranking", index=False, header=False)
        print("Result saved")


def Readcsv(path):
    CSV = open(path)
    data = np.loadtxt(CSV, delimiter=";")
    return data


def Readtxt(path):
    stream = io.open(path, "rt", encoding="utf8")
    text = stream.readlines()
    for i in range(len(text)):
        text[i] = text[i].replace("\n", "")
    return text


def Clonetolist(data):
    Y = len(data)
    X = len(data[0])
    new = [[0 for i in range(X)] for j in range(Y)]
    for i in range(X):
        for j in range(Y):
            new[j][i] = data[j][i]
    return new


def Normalize(data):
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


def Distance(user_pick, weights, data):
    Y = len(data)
    X = len(data[0])
    dist = []
    for j in range(Y):
        tmp = 0
        for i in range(X):
            if weights[i] != 0:
                tmp += pow(np.abs(data[j][i] - user_pick[i]) / weights[i], 2)
        tmp = pow(tmp, 0.5)
        tmp = round(tmp, 3)
        dist.append(tmp)
    return dist


def Pearson(user_pick, weights, data):
    Y = len(data)
    X = len(data[0])
    data = Multiply_weights_2dim(data, weights)
    user_pick = Multiply_weights(user_pick, weights)
    factors = []
    avg_user = Average(user_pick)
    sum_den_user = 0
    for i in range(X):
        sum_den_user += pow(user_pick[i] - avg_user, 2)
    sum_den_user = pow(sum_den_user, 0.5)
    for j in range(Y):
        sum_num = 0
        sum_den_x = 0
        avg_x = Average(data[j])
        for i in range(X):
            sum_num += (data[j][i] - avg_x) * (user_pick[i] - avg_user)
            sum_den_x += pow(data[j][i] - avg_x, 2)
        sum_den_x = pow(sum_den_x, 0.5)
        tmp = sum_num / (sum_den_x * sum_den_user)
        tmp = round(tmp, 6)
        factors.append(tmp)
    return factors


def Kendall(user_pick, weights, data):
    Y = len(data)
    X = len(data[0])
    data = Multiply_weights_2dim(data, weights)
    user_pick = Multiply_weights(user_pick, weights)
    tau = []
    tau.append(1)
    for j in range(1, Y):
        P = 0
        Q = 0
        T = 0
        for i in range(X):
            for k in range(X):
                if i > k:
                    det = (data[j][i] - data[j][k]) * (user_pick[i] - user_pick[k])
                    if det == 0:
                        T += 1
                    if det > 0:
                        P += 1
                    else:
                        Q += 1
        tmp = (P - Q) / (P + Q + T)
        tmp = round(tmp, 6)
        tau.append(tmp)
    return tau


def Multiply_weights_2dim(data, weights):
    for j in range(len(data)):
        for i in range(len(data[0])):
            data[j][i] *= weights[i] / 3
    return data


def Multiply_weights(tab, weights):
    for i in range(len(tab)):
        tab[i] *= weights[i] / 3
    return tab


def Average(tab):
    sum = 0
    for i in range(len(tab)):
        sum += tab[i]
    return sum / len(tab)


def Quicksort(tab, key):
    return Quicksort_a(tab[:], key[:], 0, len(key) - 1)


def Quicksort_a(tab, key, left, right):
    if right <= left:
        return tab, key
    pivot = key[int((left + right) / 2)]
    i = left - 1
    j = right + 1
    while 1:
        while 1:
            i += 1
            if pivot <= key[i]:
                break
        while 1:
            j -= 1
            if pivot >= key[j]:
                break
        if i <= j:
            temp = tab[i]
            tab[i] = tab[j]
            tab[j] = temp
            temp = key[i]
            key[i] = key[j]
            key[j] = temp
        else:
            break
    if j > left:
        tab, key = Quicksort_a(tab, key, left, j)
    if i < right:
        tab, key = Quicksort_a(tab, key, i, right)
    return tab, key


def Merge_data(id, names, criterion, data, features_arg):
    data = Clonetolist(data)
    features = features_arg.copy()
    for i in range(0, len(id)):
        data[i].insert(0, criterion[i])
        data[i].insert(0, names[i])
        data[i].insert(0, id[i])
        data[i].insert(0, i)
    features.insert(0, "Pozycja")
    data.insert(0, features)
    return data


def Change_format(data):
    for i in range(1, len(data)):
        data[i][4] = int(data[i][4])
        if data[i][5] == 7:
            data[i][5] = "S"
        else:
            data[i][5] = chr(int(data[i][5]) + 64)
        data[i][7] = int(data[i][7])
        data[i][8] = int(data[i][8])
        data[i][9] = int(data[i][9])
        data[i][10] = int(data[i][10])
        data[i][12] = int(data[i][12])
        data[i][13] = int(data[i][13])
        data[i][14] = int(data[i][14])
        data[i][15] = int(data[i][15])
        data[i][16] = int(data[i][16])
        data[i][17] = int(data[i][17])
        data[i][18] = int(data[i][18])
        data[i][19] = int(data[i][19])
        data[i][20] = int(data[i][20])
    return data


def Display(data):
    for row in data:
        print(row)
    print()


def Writetoexcel(data, path):
    df = pd.DataFrame(data)
    df.to_excel(excel_writer=path, sheet_name="ranking", index=False, header=False)
    print("Result saved")


cr = CarRecommendation()

data = Readcsv("Dane.csv")
features = Readtxt("Cechy.txt")
names = Readtxt("Nazwy aut.txt")

features.insert(2, "Kryterium główne")

weights = [  # [0-3]
    1,  # year of production
    1,  # segment
    1,  # engine capacity
    1,  # number of cylinders
    1,  # power
    1,  # number of seats
    3,  # number of doors
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
length = 255  # [3-255] number of records in the result

data = np.vstack([user_values, data])
names.insert(0, "Wartości użytkownika")

data = Clonetolist(data)

normalized = Normalize(data)
user_values_norm = normalized[0]

dist = Distance(user_values_norm, weights, normalized)
pearson = Pearson(user_values_norm, weights, normalized)
kendall = Kendall(user_values_norm, weights, normalized)

id = list(range(len(data)))

sorted_names_d, sorted_dist = Quicksort(names, dist)
sorted_data_d, sorted_dist = Quicksort(data, dist)
sorted_id_d, sorted_dist = Quicksort(id, dist)

sorted_names_p, sorted_pear = Quicksort(names, pearson)
sorted_data_p, sorted_pear = Quicksort(data, pearson)
sorted_id_p, sorted_pear = Quicksort(id, pearson)

sorted_names_p.reverse()
sorted_data_p.reverse()
sorted_id_p.reverse()
sorted_pear.reverse()

sorted_names_k, sorted_kend = Quicksort(names, kendall)
sorted_data_k, sorted_kend = Quicksort(data, kendall)
sorted_id_k, sorted_kend = Quicksort(id, kendall)

sorted_names_k.reverse()
sorted_data_k.reverse()
sorted_id_k.reverse()
sorted_kend.reverse()

data_d = Merge_data(sorted_id_d, sorted_names_d, sorted_dist, sorted_data_d, features)
data_p = Merge_data(sorted_id_p, sorted_names_p, sorted_pear, sorted_data_p, features)
data_k = Merge_data(sorted_id_k, sorted_names_k, sorted_kend, sorted_data_k, features)

data_d = Change_format(data_d[:length][:])
data_p = Change_format(data_p[:length][:])
data_k = Change_format(data_k[:length][:])

data_d[0][3] = "Odleglość"
data_p[0][3] = "Podobieństwo"
data_k[0][3] = "Estymator tau"

Display(data_d)
Display(data_p)
Display(data_k)

Writetoexcel(data_d, "wyniki_odleglosc.xlsx")
Writetoexcel(data_p, "wyniki_pearson.xlsx")
Writetoexcel(data_k, "wyniki_kendall.xlsx")
