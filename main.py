from tkinter import *
from tkinter import messagebox
from numpy import abs, loadtxt, vstack, max, min
from pandas import DataFrame
from io import open


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
        self.window.geometry("495x450")
        self.window.title("Rekomendacja samochodów")
        self.ReadData()
        self.CountMinMax()
        self.BuildWindow()
        self.window.mainloop()

    def ReadData(self):
        self.data = self.Readcsv("Dane.csv")
        self.features = self.Readtxt("Cechy.txt")
        self.names = self.Readtxt("Nazwy aut.txt")

        self.features.insert(2, "Kryterium główne")

    def Readcsv(self, path):
        CSV = open(path)
        data = loadtxt(CSV, delimiter=";")
        return data

    def Readtxt(self, path):
        stream = open(path, "rt", encoding="utf8")
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

        self.values = [0] * 18
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

            self.values[i] = Entry(self.window, width=field_width)
            self.values[i].grid(row=i + 1, column=1, sticky=W)

            self.gap[i] = Label(self.window)
            self.gap[i]["text"] = "      "
            self.gap[i].grid(row=i + 1, column=2, sticky=W)

            self.weights[i] = Entry(self.window, width=field_width)
            self.weights[i].grid(row=i + 1, column=3, sticky=W)

        self.gap = Label(self.window)
        self.gap["text"] = ""
        self.gap.grid(row=19, column=0, sticky=W)

        self.length_label = Label(self.window)
        self.length_label["text"] = (
            "Liczba rekomendowanych aut (1-" + str(len(self.data)) + "):"
        )
        self.length_label.grid(row=20, column=0, sticky=W)

        self.length = Entry(self.window, width=field_width)
        self.length.grid(row=20, column=1, sticky=W)

        self.accept_button = Button(self.window, width=16)
        self.accept_button["text"] = "Rekomenduj"
        self.accept_button["command"] = self.CheckErrors
        self.accept_button.grid(row=20, column=3, sticky=W)

    def CheckErrors(self):
        try:
            for i in range(18):
                if self.values[i].get() == "":
                    raise EmptyFieldError(self.text[i], "Wartość")
                if self.weights[i].get() == "":
                    raise EmptyFieldError(self.text[i], "Waga")
                if i == 1:
                    if (
                        self.values[i].get() != "A"
                        and self.values[i].get() != "B"
                        and self.values[i].get() != "C"
                        and self.values[i].get() != "D"
                        and self.values[i].get() != "E"
                        and self.values[i].get() != "F"
                        and self.values[i].get() != "S"
                    ):
                        raise NotTheLetterError("e")
                elif i == 2 or i == 7:
                    if (
                        self.values[i].get().find(".") == -1
                        or self.values[i].get()[len(self.values[i].get()) - 2] != "."
                    ):
                        raise NonFractionalError(self.text[i])
                    if (
                        float(self.values[i].get()) > self.max[i]
                        or float(self.values[i].get()) < self.min[i]
                    ):
                        raise OutOfRangeError(
                            self.text[i], "Wartość", self.min[i], self.max[i]
                        )
                else:
                    if self.values[i].get().find(".") != -1:
                        raise NonIntegerError(self.text[i], "Wartość")
                    if (
                        int(self.values[i].get()) > self.max[i]
                        or int(self.values[i].get()) < self.min[i]
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
            else:
                self.Recommend()

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

    def Recommend(self):
        self.CopyUserData()

        self.data = vstack([self.user_values, self.data])
        self.names.insert(0, "Wartości użytkownika")

        self.data = self.Clonetolist(self.data)

        normalized = self.Normalize(self.data)
        user_values_norm = normalized[0]

        dist = self.Distance(user_values_norm, self.user_weights, normalized)
        pearson = self.Pearson(user_values_norm, self.user_weights, normalized)
        kendall = self.Kendall(user_values_norm, self.user_weights, normalized)

        id = list(range(len(self.data)))

        sorted_names_d, sorted_dist = self.Quicksort(self.names, dist)
        sorted_data_d, sorted_dist = self.Quicksort(self.data, dist)
        sorted_id_d, sorted_dist = self.Quicksort(id, dist)

        sorted_names_p, sorted_pear = self.Quicksort(self.names, pearson)
        sorted_data_p, sorted_pear = self.Quicksort(self.data, pearson)
        sorted_id_p, sorted_pear = self.Quicksort(id, pearson)

        sorted_names_p.reverse()
        sorted_data_p.reverse()
        sorted_id_p.reverse()
        sorted_pear.reverse()

        sorted_names_k, sorted_kend = self.Quicksort(self.names, kendall)
        sorted_data_k, sorted_kend = self.Quicksort(self.data, kendall)
        sorted_id_k, sorted_kend = self.Quicksort(id, kendall)

        sorted_names_k.reverse()
        sorted_data_k.reverse()
        sorted_id_k.reverse()
        sorted_kend.reverse()

        data_d = self.Merge_data(
            sorted_id_d, sorted_names_d, sorted_dist, sorted_data_d, self.features
        )
        data_p = self.Merge_data(
            sorted_id_p, sorted_names_p, sorted_pear, sorted_data_p, self.features
        )
        data_k = self.Merge_data(
            sorted_id_k, sorted_names_k, sorted_kend, sorted_data_k, self.features
        )

        data_d = self.Change_format(data_d[: self.user_length][:], self.user_weights)
        data_p = self.Change_format(data_p[: self.user_length][:], self.user_weights)
        data_k = self.Change_format(data_k[: self.user_length][:], self.user_weights)

        data_d[1][3] = "Odleglość"
        data_p[1][3] = "Podobieństwo"
        data_k[1][3] = "Estymator tau"

        self.Writetoexcel(data_d, "wyniki_odleglosc.xlsx")
        self.Writetoexcel(data_p, "wyniki_pearson.xlsx")
        self.Writetoexcel(data_k, "wyniki_kendall.xlsx")

        messagebox.showinfo(
            "Zapisano",
            "Rekomendacja zakończona sukcesem!\n\n"
            + "Wyniki zostały zapisane w katalogu tej aplikacji w plikach:\n"
            + '"wyniki_odleglosc.xlsx" obliczone za pomocą odległości w przestrzeni euklidesowej;\n'
            + '"wyniki_pearson.xlsx" obliczone za pomocą współczynnika korelacji Pearsona;\n'
            + '"wyniki_kendall.xlsx" obliczone za pomocą tau Kendalla.\n',
        )

    def CopyUserData(self):
        self.user_weights = []
        self.user_values = []
        for i in range(len(self.values)):
            if i == 1:
                if self.values[i].get() == "S":
                    self.user_values.append(7)
                else:
                    char_arr = list(self.values[i].get())
                    self.user_values.append(int(ord(char_arr[0])) - 64)
            elif i == 2 or i == 7:
                self.user_values.append(float(self.values[i].get()))
            else:
                self.user_values.append(int(float(self.values[i].get())))
            self.user_weights.append(int(float(self.weights[i].get())))
        self.user_length = int(float(self.length.get())) + 2

    def Clonetolist(self, data):
        Y = len(data)
        X = len(data[0])
        new = [[0 for i in range(X)] for j in range(Y)]
        for i in range(X):
            for j in range(Y):
                new[j][i] = data[j][i]
        return new

    def Normalize(self, data):
        Y = len(data)
        X = len(data[0])
        new = [[0 for i in range(X)] for j in range(Y)]
        for i in range(X):
            MIN = min(data[:][i])
            MAX = max(data[:][i])
            for j in range(Y):
                tmp = (data[j][i] - MIN) / (MAX - MIN)
                new[j][i] = tmp
        return new

    def Distance(self, user_pick, weights, data):
        Y = len(data)
        X = len(data[0])
        dist = []
        for j in range(Y):
            tmp = 0
            for i in range(X):
                if weights[i] != 0:
                    tmp += pow(abs(data[j][i] - user_pick[i]) / weights[i], 2)
            tmp = pow(tmp, 0.5)
            tmp = round(tmp, 3)
            dist.append(tmp)
        return dist

    def Pearson(self, user_pick, weights, data):
        Y = len(data)
        X = len(data[0])
        data = self.Multiply_weights_2dim(data, weights)
        user_pick = self.Multiply_weights(user_pick, weights)
        factors = []
        avg_user = self.Average(user_pick)
        sum_den_user = 0
        for i in range(X):
            sum_den_user += pow(user_pick[i] - avg_user, 2)
        sum_den_user = pow(sum_den_user, 0.5)
        for j in range(Y):
            sum_num = 0
            sum_den_x = 0
            avg_x = self.Average(data[j])
            for i in range(X):
                sum_num += (data[j][i] - avg_x) * (user_pick[i] - avg_user)
                sum_den_x += pow(data[j][i] - avg_x, 2)
            sum_den_x = pow(sum_den_x, 0.5)
            tmp = sum_num / (sum_den_x * sum_den_user)
            tmp = round(tmp, 6)
            factors.append(tmp)
        return factors

    def Kendall(self, user_pick, weights, data):
        Y = len(data)
        X = len(data[0])
        data = self.Multiply_weights_2dim(data, weights)
        user_pick = self.Multiply_weights(user_pick, weights)
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

    def Multiply_weights_2dim(self, data, weights):
        for j in range(len(data)):
            for i in range(len(data[0])):
                data[j][i] *= weights[i] / 3
        return data

    def Multiply_weights(self, tab, weights):
        for i in range(len(tab)):
            tab[i] *= weights[i] / 3
        return tab

    def Average(self, tab):
        sum = 0
        for i in range(len(tab)):
            sum += tab[i]
        return sum / len(tab)

    def Quicksort(self, tab, key):
        return self.Quicksort_a(tab[:], key[:], 0, len(key) - 1)

    def Quicksort_a(self, tab, key, left, right):
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
            tab, key = self.Quicksort_a(tab, key, left, j)
        if i < right:
            tab, key = self.Quicksort_a(tab, key, i, right)
        return tab, key

    def Merge_data(self, id, names, criterion, data, features_arg):
        data = self.Clonetolist(data)
        features = features_arg.copy()
        for i in range(0, len(id)):
            data[i].insert(0, criterion[i])
            data[i].insert(0, names[i])
            data[i].insert(0, id[i])
            data[i].insert(0, i)
        features.insert(0, "Pozycja")
        data.insert(0, features)
        return data

    def Change_format(self, data, weights):
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
        weights_out = []
        for i in range(len(data[0])):
            if i == 0:
                weights_out.append("Wagi kryteriów:")
            elif i > 0 and i < 4:
                weights_out.append("-")
            else:
                weights_out.append(weights[i - 4])
        data.insert(0, weights_out)
        return data

    def Writetoexcel(self, data, path):
        df = DataFrame(data)
        df.to_excel(excel_writer=path, sheet_name="ranking", index=False, header=False)


cr = CarRecommendation()
