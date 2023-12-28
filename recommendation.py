from tkinter import *
from tkinter import messagebox
from numpy import abs, loadtxt, vstack, max, min, sign
from pandas import DataFrame
from os.path import isfile


# Error classes
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


class TooManyEmptyError(Exception):
    def __init__(self):
        self = self


# Class doing car recommendation
class CarRecommendation(object):
    # Constructor
    def __init__(self):
        self.window = Tk()
        self.window.geometry("495x450")
        self.window.title("Rekomendacja samochodów")
        self.ReadData()
        self.CountMinMax()
        self.BuildWindow()
        self.window.mainloop()

    # Function calling reading from files
    def ReadData(self):
        self.data = self.ReadFromCSV("Dane.csv")
        self.features = self.ReadFromTXT("Cechy.txt")
        self.names = self.ReadFromTXT("Nazwy aut.txt")

        self.features.insert(2, "Kryterium główne")

    # Function reading data from CSV file
    def ReadFromCSV(self, path):
        CSV = open(path)
        data = loadtxt(CSV, delimiter=";")
        return data

    # Function reading data from TXT file
    def ReadFromTXT(self, path):
        stream = open(path, "rt", encoding="utf8")
        text = stream.readlines()
        for i in range(len(text)):
            text[i] = text[i].replace("\n", "")
        return text

    # Function calculating the minimum and maximum of each feature from the data set
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

    # Function defining the structure of the window with user interface
    def BuildWindow(self):
        field_width = 20
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
        self.label_criteria_weights["text"] = "Wagi kryteriów (1-3)"
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

    # Function ckecking and signaling errors in the data provided by the user
    def CheckErrors(self):
        try:
            counter = 0
            for i in range(18):
                if self.values[i].get() == "" and self.weights[i].get() != "":
                    raise EmptyFieldError(self.text[i], "Wartość")
                if self.weights[i].get() == "" and self.values[i].get() != "":
                    raise EmptyFieldError(self.text[i], "Waga")
                if self.values[i].get() != "" and self.weights[i].get() != "":
                    counter += 1
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
                            or self.values[i].get()[len(self.values[i].get()) - 2]
                            != "."
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
                        if self.values[i].get().isnumeric() == False:
                            raise NonIntegerError(self.text[i], "Wartość")
                        if (
                            int(self.values[i].get()) > self.max[i]
                            or int(self.values[i].get()) < self.min[i]
                        ):
                            raise OutOfRangeError(
                                self.text[i],
                                "Wartość",
                                int(self.min[i]),
                                int(self.max[i]),
                            )
                    if self.weights[i].get().isnumeric() == False:
                        raise NonIntegerError(self.text[i], "Waga")
                    if int(self.weights[i].get()) > 3 or int(self.weights[i].get()) < 1:
                        raise OutOfRangeError(self.text[i], "Waga", 1, 3)
            if counter < 4:
                raise TooManyEmptyError()
            if self.length.get() == "":
                raise EmptyFieldError("Liczba rekomendowanych aut", "Wartość")
            if self.length.get().find(".") != -1:
                raise NonIntegerError("Liczba rekomendowanych aut", "Wartość")
            if int(self.length.get()) < 0 or int(self.length.get()) > len(self.data):
                raise OutOfRangeError(
                    "Liczba rekomendowanych aut", "Wartość", 0, len(self.data)
                )
            path = [
                "wyniki_odleglosc.xlsx",
                "wyniki_odleglosc_minkowskiego.xlsx",
                "wyniki_pearson.xlsx",
                "wyniki_kendall.xlsx",
            ]
            for i in range(len(path)):
                if isfile(path[i]):
                    f = open(path[i], "r+")
                    f.close()
            else:
                self.Recommend()

        except EmptyFieldError as e:
            messagebox.showerror(
                "Błąd", e.type + " kryterium " + e.name + " nie może być pusta!"
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
                + " musi być liczbą całkowitą, pisaną bez kropki!",
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
        except TooManyEmptyError as e:
            messagebox.showerror(
                "Błąd",
                "Co najmniej 4 kryteria powinny mieć wprowadzoną wartość oraz wagę!",
            )
        except IOError as e:
            messagebox.showerror(
                "Błąd!",
                "Plik excel z wynikami nie może być otwarty podczas rekomendacji!\n"
                + "Zamknij plik i rekomenduj ponownie.",
            )

    # Main car recommendation function
    def Recommend(self):
        self.CopyUserData()

        data = self.data.copy()
        names = self.names.copy()
        features = self.features.copy()

        data = vstack([self.user_values, data])
        names.insert(0, "Wartości użytkownika")

        data = self.CloneToList(data)

        normalized = self.Normalize(data)
        user_values_norm = normalized[0]

        dist = self.Distance(user_values_norm, self.user_weights, normalized, 2)
        dist2 = self.Distance(user_values_norm, self.user_weights, normalized, 4)
        pearson = self.Pearson(user_values_norm, self.user_weights, normalized)
        kendall = self.Kendall(user_values_norm, self.user_weights, normalized)

        id = list(range(len(data)))

        sorted_names_d, sorted_dist = self.Quicksort(names, dist)
        sorted_data_d, sorted_dist = self.Quicksort(data, dist)
        sorted_id_d, sorted_dist = self.Quicksort(id, dist)

        sorted_names_d2, sorted_dist2 = self.Quicksort(names, dist2)
        sorted_data_d2, sorted_dist2 = self.Quicksort(data, dist2)
        sorted_id_d2, sorted_dist2 = self.Quicksort(id, dist2)

        sorted_names_p, sorted_pear = self.Quicksort(names, pearson)
        sorted_data_p, sorted_pear = self.Quicksort(data, pearson)
        sorted_id_p, sorted_pear = self.Quicksort(id, pearson)

        sorted_names_p.reverse()
        sorted_data_p.reverse()
        sorted_id_p.reverse()
        sorted_pear.reverse()

        sorted_names_k, sorted_kend = self.Quicksort(names, kendall)
        sorted_data_k, sorted_kend = self.Quicksort(data, kendall)
        sorted_id_k, sorted_kend = self.Quicksort(id, kendall)

        sorted_names_k.reverse()
        sorted_data_k.reverse()
        sorted_id_k.reverse()
        sorted_kend.reverse()

        data_d = self.MergeData(
            sorted_id_d, sorted_names_d, sorted_dist, sorted_data_d, features
        )
        data_d2 = self.MergeData(
            sorted_id_d2, sorted_names_d2, sorted_dist2, sorted_data_d2, features
        )
        data_p = self.MergeData(
            sorted_id_p, sorted_names_p, sorted_pear, sorted_data_p, features
        )
        data_k = self.MergeData(
            sorted_id_k, sorted_names_k, sorted_kend, sorted_data_k, features
        )

        data_d = self.ChangeFormat(
            data_d[: self.user_length][:], self.user_weights, dist[0]
        )
        data_d2 = self.ChangeFormat(
            data_d2[: self.user_length][:], self.user_weights, dist2[0]
        )
        data_p = self.ChangeFormat(
            data_p[: self.user_length][:], self.user_weights, pearson[0]
        )
        data_k = self.ChangeFormat(
            data_k[: self.user_length][:], self.user_weights, kendall[0]
        )

        data_d[1][3] = "Odleglość"
        data_d2[1][3] = "Odległość Minkowskiego"
        data_p[1][3] = "Podobieństwo"
        data_k[1][3] = "Estymator tau"

        self.WriteToXLSX(data_d, "wyniki_odleglosc.xlsx")
        self.WriteToXLSX(data_d2, "wyniki_odleglosc_minkowskiego.xlsx")
        self.WriteToXLSX(data_p, "wyniki_pearson.xlsx")
        self.WriteToXLSX(data_k, "wyniki_kendall.xlsx")

        messagebox.showinfo(
            "Zapisano",
            "Rekomendacja zakończona sukcesem!\n\n"
            + "Wyniki zostały zapisane w katalogu tej aplikacji w plikach:\n"
            + '"wyniki_odleglosc.xlsx" obliczone za pomocą odległości w przestrzeni euklidesowej;\n'
            + '"wyniki_odleglosc_minkowskiego.xlsx" obliczone za pomocą odległości minkowskiego;\n'
            + '"wyniki_pearson.xlsx" obliczone za pomocą współczynnika korelacji Pearsona;\n'
            + '"wyniki_kendall.xlsx" obliczone za pomocą tau Kendalla.\n',
        )

    # Function that changes the format of user data for calculations
    def CopyUserData(self):
        self.user_weights = []
        self.user_values = []
        for i in range(len(self.values)):
            if self.values[i].get() != "":
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
            else:
                self.user_values.append(self.min[i])
                self.user_weights.append(0)

        self.user_length = int(float(self.length.get())) + 2

    # Function changing the format of car data from a numpy array to a 2-dimensional list
    def CloneToList(self, data):
        Y = len(data)
        X = len(data[0])
        new = [[0 for i in range(X)] for j in range(Y)]
        for i in range(X):
            for j in range(Y):
                new[j][i] = data[j][i]
        return new

    # Function normalizing car data
    def Normalize(self, data):
        Y = len(data)
        X = len(data[0])
        new = [[0 for i in range(X)] for j in range(Y)]
        for i in range(X):
            MIN = min([j[i] for j in data])
            MAX = max([j[i] for j in data])
            for j in range(Y):
                tmp = (data[j][i] - MIN) / (MAX - MIN)
                new[j][i] = tmp
        return new

    # Function calculating the distance in Euclidean space between the user requirements and the cars in the data
    def Distance(self, user_pick, weights, data, p):
        Y = len(data)
        X = len(data[0])
        dist = []
        for j in range(Y):
            tmp = 0
            for i in range(X):
                if weights[i] != 0:
                    tmp += pow(abs(data[j][i] - user_pick[i]), p) / weights[i]
            tmp = pow(tmp, 1 / p)
            dist.append(round(tmp, 10))
        return dist

    # Function calculating the Pearson correlation coefficient between user requirements and cars from the data
    def Pearson(self, user_pick, weights, data):
        Y = len(data)
        X = len(data[0])
        factors = []
        avg_user = self.Average_weight(user_pick, weights)
        sum_den_user = 0
        for i in range(X):
            sum_den_user += weights[i] * pow(user_pick[i] - avg_user, 2)
        sum_den_user = pow(sum_den_user, 0.5)
        for j in range(Y):
            sum_num = 0
            sum_den_x = 0
            avg_x = self.Average_weight(data[j], weights)
            for i in range(X):
                sum_num += weights[i] * (data[j][i] - avg_x) * (user_pick[i] - avg_user)
                sum_den_x += weights[i] * pow(data[j][i] - avg_x, 2)
            sum_den_x = pow(sum_den_x, 0.5)
            tmp = sum_num / (sum_den_x * sum_den_user)
            factors.append(round(tmp, 10))
        return factors

    # Function calculating the Kendall rank correlation coefficient between user requirements and cars from the data
    def Kendall(self, user_pick, weights, data):
        Y = len(data)
        X = len(data[0])
        tau = []
        sum_den = 0
        for i in range(X):
            for k in range(X):
                if i > k:
                    sum_den += weights[i] * weights[k]
        for j in range(Y):
            sum_num = 0
            for i in range(X):
                for k in range(X):
                    if i > k:
                        sum_num += (
                            weights[i]
                            * weights[k]
                            * sign(user_pick[i] - user_pick[k])
                            * sign(data[j][i] - data[j][k])
                        )
            tmp = sum_num / sum_den
            tau.append(round(tmp, 10))
        return tau

    # Function calculating the average of the list for elements with non-zero weight
    def Average_weight(self, tab, weights):
        sum = 0
        weight_sum = 0
        for i in range(len(tab)):
            weight_sum += weights[i]
            sum += tab[i] * weights[i]
        return sum / weight_sum

    # Function initiating quick sorting of the list by key
    def Quicksort(self, tab, key):
        return self.QuicksortA(tab[:], key[:], 0, len(key) - 1)

    # Proper reqursive function performing quick sort
    def QuicksortA(self, tab, key, left, right):
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
            tab, key = self.QuicksortA(tab, key, left, j)
        if i < right:
            tab, key = self.QuicksortA(tab, key, i, right)
        return tab, key

    # Function combining lists and data set into one 2-dimensional array to display as a result
    def MergeData(self, id, names, criterion, data, features_arg):
        new_data = self.CloneToList(data)
        features = features_arg.copy()
        for i in range(0, len(id)):
            new_data[i].insert(0, criterion[i])
            new_data[i].insert(0, names[i])
            new_data[i].insert(0, id[i])
            new_data[i].insert(0, i)
        features.insert(0, "Pozycja")
        new_data.insert(0, features)
        return new_data

    # Function changing the format of data to display result to the user
    def ChangeFormat(self, data, weights, criterion):
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
        if data[2][2] != "Wartości użytkownika":
            correction = [0, 0, "Wartości użytkownika", criterion]
            for i in range(len(self.values)):
                if self.values[i].get() == "":
                    correction.append("-")
                elif i == 1:
                    correction.append(self.values[i].get())
                elif i == 2 or i == 7:
                    correction.append(float(self.values[i].get()))
                else:
                    correction.append((int(float(self.values[i].get()))))
            data.insert(2, correction)
            counter = 0
            for i in range(2, len(data)):
                if data[i][2] == "Wartości użytkownika" and i != 2:
                    data.pop(i)
                    counter = 1
                    break
            if counter == 0:
                data.pop(len(data) - 1)
        else:
            for i in range(4, len(data[0])):
                if weights[i - 4] == 0:
                    data[2][i] = "-"
        for i in range(0, len(data) - 2):
            data[i + 2][0] = i
        return data

    # Function converting a 2-dimensional li of results into a pandas data frame and saves it to ans XLSX file
    def WriteToXLSX(self, data, path):
        df = DataFrame(data)
        df.to_excel(excel_writer=path, sheet_name="ranking", index=False, header=False)


cr = CarRecommendation()
