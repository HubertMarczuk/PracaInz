import numpy as np
import io
import pandas as pd
from tkinter import *
from tkinter import messagebox


class CarRecommendation(object):
    def __init__(self):
        self.window = Tk()
        self.window.geometry("800x800")
        self.window.title("Rekomendacja samochodów")
        self.BuildWindow()
        self.window.mainloop()

    def BuildWindow(self):
        field_width = 20

        self.label_criteria_names = Label(self.window)
        self.label_criteria_names["text"] = "Nazwy kryteriów do podania"
        self.label_criteria_names.grid(row=0, column=0, sticky=W)

        self.label_criteria_value = Label(self.window)
        self.label_criteria_value["text"] = "Wartości kryteriów"
        self.label_criteria_value.grid(row=0, column=1, sticky=W)

        self.label_criteria_weights = Label(self.window)
        self.label_criteria_weights["text"] = "Wagi kryteriów (0-3)"
        self.label_criteria_weights.grid(row=0, column=2, sticky=W)

        self.label_year = Label(self.window)
        self.label_year["text"] = "Rok produkcji (1955-2023)"
        self.label_year.grid(row=1, column=0, sticky=W)

        self.year_value = Entry(self.window, width=field_width)
        self.year_value.grid(row=1, column=1, sticky=W)

        self.year_weight = Entry(self.window, width=field_width)
        self.year_weight.grid(row=1, column=2, sticky=W)

        self.label_segment = Label(self.window)
        self.label_segment["text"] = "Segment (A,B,...,F,S)"
        self.label_segment.grid(row=2, column=0, sticky=W)

        self.segment_value = Entry(self.window, width=field_width)
        self.segment_value.grid(row=2, column=1, sticky=W)

        self.segment_weight = Entry(self.window, width=field_width)
        self.segment_weight.grid(row=2, column=2, sticky=W)

        self.label_engine_capacity = Label(self.window)
        self.label_engine_capacity["text"] = "Pojemność silnika [l] (0.0-8.4)"
        self.label_engine_capacity.grid(row=3, column=0, sticky=W)

        self.engine_capacity_value = Entry(self.window, width=field_width)
        self.engine_capacity_value.grid(row=3, column=1, sticky=W)

        self.engine_capacity_weight = Entry(self.window, width=field_width)
        self.engine_capacity_weight.grid(row=3, column=2, sticky=W)

        self.label_number_of_cylinders = Label(self.window)
        self.label_number_of_cylinders["text"] = "Liczba cylindrów (2-16)"
        self.label_number_of_cylinders.grid(row=4, column=0, sticky=W)

        self.number_of_cylinders_value = Entry(self.window, width=field_width)
        self.number_of_cylinders_value.grid(row=4, column=1, sticky=W)

        self.number_of_cylinders_weight = Entry(self.window, width=field_width)
        self.number_of_cylinders_weight.grid(row=4, column=2, sticky=W)

        self.label_power = Label(self.window)
        self.label_power["text"] = "Moc [KM] (76-1600)"
        self.label_power.grid(row=5, column=0, sticky=W)

        self.power_value = Entry(self.window, width=field_width)
        self.power_value.grid(row=5, column=1, sticky=W)

        self.power_weight = Entry(self.window, width=field_width)
        self.power_weight.grid(row=5, column=2, sticky=W)

        self.label_number_of_seats = Label(self.window)
        self.label_number_of_seats["text"] = "Liczba miejsc (2-6)"
        self.label_number_of_seats.grid(row=6, column=0, sticky=W)

        self.number_of_seats_value = Entry(self.window, width=field_width)
        self.number_of_seats_value.grid(row=6, column=1, sticky=W)

        self.number_of_seats_weight = Entry(self.window, width=field_width)
        self.number_of_seats_weight.grid(row=6, column=2, sticky=W)

        self.label_number_of_doors = Label(self.window)
        self.label_number_of_doors["text"] = "Liczba drzwi (2-5)"
        self.label_number_of_doors(row=7, column=0, sticky=W)

        self.number_of_doors_value = Entry(self.window, width=field_width)
        self.number_of_doors_value.grid(row=7, column=1, sticky=W)

        self.number_of_doors_weight = Entry(self.window, width=field_width)
        self.number_of_doors_weight.grid(row=7, column=2, sticky=W)

        self.label_0_100_acceleration = Label(self.window)
        self.label_0_100_acceleration[
            "text"
        ] = "Przyspieszenie 0-100km/h [s] (2.4-15.0)"
        self.label_0_100_acceleration.grid(row=8, column=0, sticky=W)

        self._0_100_acceleration_value = Entry(self.window, width=field_width)
        self._0_100_acceleration_value.grid(row=8, column=1, sticky=W)

        self._0_100_acceleration_weight = Entry(self.window, width=field_width)
        self._0_100_acceleration_weight.grid(row=8, column=2, sticky=W)

        self.label_maximum_speed = Label(self.window)
        self.label_maximum_speed["text"] = "Prędkość maksymalna [km/h] (154-492)"
        self.label_maximum_speed.grid(row=9, column=0, sticky=W)

        self.maximum_speed_value = Entry(self.window, width=field_width)
        self.maximum_speed_value.grid(row=9, column=1, sticky=W)

        self.maximum_speed_weight = Entry(self.window, width=field_width)
        self.maximum_speed_weight.grid(row=9, column=2, sticky=W)

        self.label_torque = Label(self.window)
        self.label_torque["text"] = "Moment obrotowy [Nm] (107-1600)"
        self.label_torque.grid(row=10, column=0, sticky=W)

        self.torque_value = Entry(self.window, width=field_width)
        self.torque_value.grid(row=10, column=1, sticky=W)

        self.torque_weight = Entry(self.window, width=field_width)
        self.torque_weight.grid(row=10, column=2, sticky=W)

        self.label_curb_weight = Label(self.window)
        self.label_curb_weight["text"] = "Masa własna [kg] (655-2695)"
        self.label_curb_weight.grid(row=11, column=0, sticky=W)

        self.curb_weight_value = Entry(self.window, width=field_width)
        self.curb_weight_value.grid(row=11, column=1, sticky=W)

        self.curb_weight_weight = Entry(self.window, width=field_width)
        self.curb_weight_weight.grid(row=11, column=2, sticky=W)

        self.label_trunk_capacity = Label(self.window)
        self.label_trunk_capacity["text"] = "Pojemnośc bagażnika [l] (0-813)"
        self.label_trunk_capacity.grid(row=12, column=0, sticky=W)

        self.trunk_capacity_value = Entry(self.window, width=field_width)
        self.trunk_capacity_value.grid(row=12, column=1, sticky=W)

        self.trunk_capacity_weight = Entry(self.window, width=field_width)
        self.trunk_capacity_weight.grid(row=12, column=2, sticky=W)

        self.label_tank_capacity = Label(self.window)
        self.label_tank_capacity["text"] = "Pojemność baku [l] (0-159)"
        self.label_tank_capacity.grid(row=13, column=0, sticky=W)

        self.tank_capacity_value = Entry(self.window, width=field_width)
        self.tank_capacity_value.grid(row=13, column=1, sticky=W)

        self.tank_capacity_weight = Entry(self.window, width=field_width)
        self.tank_capacity_weight.grid(row=13, column=2, sticky=W)

        self.label_length = Label(self.window)
        self.label_length["text"] = "Długość [cm] (305-542)"
        self.label_length.grid(row=14, column=0, sticky=W)

        self.length_value = Entry(self.window, width=field_width)
        self.length_value.grid(row=14, column=1, sticky=W)

        self.length_weight = Entry(self.window, width=field_width)
        self.length_weight.grid(row=14, column=2, sticky=W)

        self.label_width = Label(self.window)
        self.label_width["text"] = "Szerokość [cm] (140-223)"
        self.label_width.grid(row=15, column=0, sticky=W)

        self.width_value = Entry(self.window, width=field_width)
        self.width_value.grid(row=15, column=1, sticky=W)

        self.width_weight = Entry(self.window, width=field_width)
        self.width_weight.grid(row=15, column=2, sticky=W)

        self.label_height = Label(self.window)
        self.label_height["text"] = "Wysokość [cm] (98-154)"
        self.label_height.grid(row=16, column=0, sticky=W)

        self.height_value = Entry(self.window, width=field_width)
        self.height_value.grid(row=16, column=1, sticky=W)

        self.height_weight = Entry(self.window, width=field_width)
        self.height_weight.grid(row=16, column=2, sticky=W)

        self.label_wheelbase = Label(self.window)
        self.label_wheelbase["text"] = "Rozstaw osi [cm] (204-305)"
        self.label_wheelbase.grid(row=17, column=0, sticky=W)

        self.wheelbase_value = Entry(self.window, width=field_width)
        self.wheelbase_value.grid(row=17, column=1, sticky=W)

        self.wheelbase_weight = Entry(self.window, width=field_width)
        self.wheelbase_weight.grid(row=17, column=2, sticky=W)

        self.label_number_of_gears = Label(self.window)
        self.label_number_of_gears["text"] = "Liczba biegów (2-9)"
        self.label_number_of_gears.grid(row=18, column=0, sticky=W)

        self.number_of_gears_value = Entry(self.window, width=field_width)
        self.number_of_gears_value.grid(row=18, column=1, sticky=W)

        self.number_of_gears_weight = Entry(self.window, width=field_width)
        self.number_of_gears_weight.grid(row=18, column=2, sticky=W)


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
