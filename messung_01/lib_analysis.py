# This script is a fork of analysis.py from the following repository:
# https://github.com/c-mahn/test-sensor-data-analysis

# Import of libraries
# -----------------------------------------------------------------------------

import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
import math as m
import sys
import os
from scipy.fft import fft, fftfreq
from scipy import signal


# Functions
# -----------------------------------------------------------------------------

def plot_werte(datenreihen, name=["Messwerte"]):
    """
    Diese Funktion nimmt Datenreihen und plottet diese in ein Diagramm.
    """
    for i, datenreihe in enumerate(datenreihen):
        zeit = range(len(datenreihe))
        plt.plot(zeit, datenreihe)
    plt.legend(name)
    plt.grid()
    plt.xlabel("")
    plt.ylabel("")
    plt.title(name[0])
    plt.show()


def plot_xy(datenreihen, name=["Messwerte"], x="X", y="Y", title=None):
    """
    Diese Funktion nimmt je zwei Datenreihen und plottet diese in Abhängigkeit
    zueinander in ein Diagramm.
    """
    for i, datenreihe in enumerate(datenreihen):
        plt.plot(datenreihe[0], datenreihe[1])
    plt.legend(name)
    plt.grid()
    plt.xlabel(x)
    plt.ylabel(y)
    if(title != None):
        plt.title(title)
    else:
        plt.title(name[0])
    plt.show()


def fill_nan(A):
    '''
    interpolate to fill nan values
    '''
    A = np.array(A)
    inds = np.arange(A.shape[0])
    good = np.where(np.isfinite(A))
    f = interpolate.interp1d(inds[good], A[good],bounds_error=False)
    B = np.where(np.isfinite(A),A,f(inds))
    return B


def low_pass_filter(datenreihe, filterungsgrad):
    """
    Diese Funktion macht einen vereinfachten Low-Pass-Filter, indem die letzten
    x Sensorwerte gemittelt werden.
    """
    ausgabe = []
    for i, e in enumerate(datenreihe):
        divisor = filterungsgrad
        summe = 0
        for j in range(filterungsgrad):
            ji = i-j
            if(ji < 0):  # Wenn Wert ausserhalb der Datenreihe, ändern des Divisors
                divisor = divisor - 1
            else:
                summe = summe + float(datenreihe[ji])
        temp = summe/divisor
        ausgabe.append(temp)
    return(ausgabe)

def high_pass_filter(datenreihe, datenreihe_low_pass):
    """
    Diese Funktion macht einen vereinfachten High-Pass-Filter, indem die
    Low-Pass-Datenreihe von der Originaldatenreihe abgezogen wird.
    """
    ausgabe = []
    for i, e in enumerate(datenreihe):
        ausgabe.append(datenreihe[i] - datenreihe_low_pass[i])
    return(ausgabe)

def fast_fourier_transform(datenreihe, sample_rate):
    """
    Diese Funktion macht eine Fast-Fourier-Transformation und gibt die Frequenz-
    und Amplitudengraphen zurück.
    """
    N = len(datenreihe)
    T = 1.0 / sample_rate
    yf = fft(datenreihe)
    xf = fftfreq(N, T)[:N//2]
    return(xf, 2.0/N * np.abs(yf[0:N//2]))


def cross_correlation(x_red, y_red):
        Nx = len(x_red)
        if Nx != len(y_red):
            raise ValueError('x and y must be equal length')
        c = np.correlate(x_red, y_red, mode=2)
        c /= np.sqrt(np.dot(x_red, x_red) * np.dot(y_red, y_red))
        maxlags = Nx - 1
        if maxlags >= Nx or maxlags < 1:
            raise ValueError('maglags must be None or strictly '
                             'positive < %d' % Nx)
        lags = np.arange(-maxlags, maxlags + 1)
        c = c[Nx - 1 - maxlags:Nx + maxlags]
        return lags, c
    
def linear_regression(x, y):
    """
    Diese Funktion macht eine lineare Regression und gibt die Steigung und den
    y-Achsenabschnitt zurück.
    """
    x = np.array(x)
    y = np.array(y)
    m = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / (len(x)*np.sum(x*x) - np.sum(x) ** 2)
    b = (np.sum(y) - m *np.sum(x)) / len(x)
    return(m, b)


# Classes
# -----------------------------------------------------------------------------

# Beginning of the main program
# -----------------------------------------------------------------------------

if(__name__ == '__main__'):

    # Einlesen der Daten
    print(f"[{1}/{1}] Einlesen der Daten...", end="\r")
    with open(os.path.join("data", "time_series_converted.txt"), "r") as f:
        data = f.readlines()
    print("")
    
    # Datenbereinigung
    print(f"[{1}/{1}] Datenbereinigung...", end="\r")
    for i, e in enumerate(data):
        data[i] = e.split(";")
        for j, e in enumerate(data[i]):
            data[i][j] = float(e.strip())
    print("")

    # Umwandeln in Datenreihen
    print(f"[{1}/{1}] Datenkonvertierung...", end="\r")
    datenreihen = [[], [], []]
    for i in data:
        datenreihen[0].append(i[0])
        datenreihen[1].append(i[1])
        datenreihen[2].append(i[2])
    datenreihen_ohne_zeit = datenreihen[1:3]
    print("")
    plot_werte(datenreihen_ohne_zeit, ["Sensor 1", "Sensor 2"])

    # Füllen von Lücken in den Datenreihen
    print(f"[{1}/{1}] Datenlücken-Bereinigung...", end="\r")
    for i, e in enumerate(datenreihen):
        if(i != 0):
            datenreihen[i] = fill_nan(np.array(e))
    print("")
    
    # Berechnung der linearen Regression von Sensor 1
    x = np.array(datenreihen[0])
    y = np.array(datenreihen[1])
    steigung_1 = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / (len(x)*np.sum(x*x) - np.sum(x) ** 2)
    offset_1 = (np.sum(y) - steigung_1 *np.sum(x)) / len(x)
    print(f'[Sensor 1] Trend: ({steigung_1:.10f})x + ({offset_1:+.6f})')
    
    # Berechnung der linearen Regression von Sensor 2
    x = np.array(datenreihen[0])
    y = np.array(datenreihen[2])
    steigung_2 = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / (len(x)*np.sum(x*x) - np.sum(x) ** 2)
    offset_2 = (np.sum(y) - steigung_2 *np.sum(x)) / len(x)
    print(f'[Sensor 2] Trend: ({steigung_2:.10f})x + ({offset_2:+.6f})')

    # Erstellung Lineare Regression zum Plotten (Plot-Punkte)
    linearisierung = [[], []]
    for i in datenreihen[0]:
        linearisierung[0].append(i*steigung_1+offset_1)
        linearisierung[1].append(i*steigung_2+offset_2)
    # Plot der linearen Regression
    plot_werte([datenreihen[1], linearisierung[0]], ["Sensor 1", "Linearisierung"])
    plot_werte([datenreihen[2], linearisierung[1]], ["Sensor 2", "Linearisierung"])

    # Bereinigung des Trends beider Sensorreihen
    datenreihen_ohne_trend = [[], []]
    print(f"[{1}/{len(datenreihen_ohne_trend)}] Bereinigung des Trends...", end="\r")
    for i, e in enumerate(datenreihen[1]):
        datenreihen_ohne_trend[0].append(e - (steigung_1*(datenreihen[0][i])+offset_1))
    print(f"[{2}/{len(datenreihen_ohne_trend)}] Bereinigung des Trends...", end="\r")
    for i, e in enumerate(datenreihen[2]):
        datenreihen_ohne_trend[1].append(e - (steigung_2*(datenreihen[0][i])+offset_2))
    print("")
    # Plot der vom Trend bereinigten Sensorreihen
    plot_werte(datenreihen_ohne_trend, ["Sensor 1 (ohne Trend)", "Sensor 2 (ohne Trend)"])

    # Low-Pass-Filterung der Sensorreihen
    low_pass_strength = 500
    datenreihen_low_pass = []
    for i, e in enumerate(datenreihen_ohne_trend):
        print(f"[{i+1}/{len(datenreihen_ohne_trend)}] Low-Pass-Filterung (Strength {low_pass_strength})...", end="\r")
        datenreihen_low_pass.append(low_pass_filter(e, low_pass_strength))
    print("")
    # Plot der low-pass Sensorreihen
    plot_werte(datenreihen_low_pass, ["Sensor 1 (mit Low-Pass-Filter)", "Sensor 2 (mit Low-Pass-Filter)"])

    # Hoch-Pass-Filterung der Sensorreihen
    datenreihen_hoch_pass = [[], []]
    print(f"[{1}/{len(datenreihen_hoch_pass)}] Hoch-Pass-Filterung...", end="\r")
    for i, e in enumerate(datenreihen_low_pass[0]):
        datenreihen_hoch_pass[0].append(datenreihen_ohne_trend[0][i] - e)
    print(f"[{2}/{len(datenreihen_hoch_pass)}] Hoch-Pass-Filterung...", end="\r")
    for i, e in enumerate(datenreihen_low_pass[1]):
        datenreihen_hoch_pass[1].append(datenreihen_ohne_trend[1][i] - e)
    print("")
    # Plot der hoch-pass Sensorreihen
    plot_werte(datenreihen_hoch_pass, ["Sensor 1 (mit Hoch-Pass-Filter)", "Sensor 2 (mit Hoch-Pass-Filter)"])

    # Fourier-Transformation

    # Weitere Informationen:
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fft.html
    sample_frequenz = 1/10
    N = 36286*2
    print(f"[{1}/{len(datenreihen_ohne_trend)}] Fast-Fourier-Transformation...", end="\r")
    yf_1 = fft(datenreihen_low_pass[0])
    xf_1 = fftfreq(len(datenreihen_low_pass[0]), 1/sample_frequenz)
    print(f"[{2}/{len(datenreihen_ohne_trend)}] Fast-Fourier-Transformation...", end="\r")
    yf_2 = fft(datenreihen_low_pass[1])
    xf_2 = fftfreq(len(datenreihen_low_pass[1]), 1/sample_frequenz)
    print("")
    # Plot der Fourier-Transformation
    plt.plot(xf_1, 2.0/N * np.abs(yf_1[0:N//2]))
    plt.xlim(0, 0.0001)
    plt.grid()
    plt.show()

    plt.plot(xf_2, 2.0/N * np.abs(yf_2[0:N//2]))
    plt.xlim(0, 0.0001)
    plt.grid()
    plt.show()
    # plot_xy([[xf_1, yf_1],
    #          [xf_2, yf_2]],
    #         ["Fourier-Transformation (Sensor 1)",
    #          "Fourier-Transformation (Sensor 2)"])

    # Kreuz-Korrelation (trendbereinigte Funktion)

    # Weitere Informationen:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.correlate.html
    print(f"[{1}/{1}] Kreuz-Korrelation...", end="\r")
    kreuzkorrelation = cross_correlation(datenreihen_ohne_trend[0], datenreihen_ohne_trend[1])
    print("")
    plot_xy([kreuzkorrelation], ["kreuzkorrelation"])

    # Weitere Informationen:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
    print(f"[{1}/{1}] Kreuz-Korrelationsspitzen...", end="\r")
    korrelation_spitzen = signal.find_peaks(kreuzkorrelation[1], height=0.5, distance=100)
    print("")
    print("Korrelationsspitzen:")
    for i in korrelation_spitzen[0]:
        print(kreuzkorrelation[0][i]*10/60, end=", ")
    print("")

    # Kreuz-Korrelation (geglättete trendbereinigte Funktion)

    # Weitere Informationen:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.correlate.html
    print(f"[{1}/{1}] Kreuz-Korrelation...", end="\r")
    kreuzkorrelation = cross_correlation(datenreihen_low_pass[0], datenreihen_low_pass[1])
    print("")
    plot_xy([kreuzkorrelation], ["kreuzkorrelation"])

    # Weitere Informationen:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
    print(f"[{1}/{1}] Kreuz-Korrelationsspitzen...", end="\r")
    korrelation_spitzen = signal.find_peaks(kreuzkorrelation[1], height=0.5, distance=100)
    print("")
    print("Korrelationsspitzen:")
    for i in korrelation_spitzen[0]:
        print(kreuzkorrelation[0][i]*10/60, end=", ")
    print("")
