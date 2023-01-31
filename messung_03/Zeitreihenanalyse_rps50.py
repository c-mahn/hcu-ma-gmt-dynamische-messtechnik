# -*- coding: utf-8 -*-
"""
Zeitreihenanalyse
"""
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
from scipy.stats import linregress
import numpy as np
from scipy.optimize import curve_fit
import os
rps = 50
write_prot = True 
    
def zeitreihe_erstellen(df, pnr, nachbarn):
    
    filtered_df = df[(df['PNR'] >= pnr-nachbarn) & (df['PNR'] <= pnr+nachbarn)]

    y_values = filtered_df.groupby(['ProfilNR'])['Y'].mean().tolist()
    z_values = filtered_df.groupby(['ProfilNR'])['Z'].mean().tolist()
    t = filtered_df.groupby(['ProfilNR'])['t'].mean().tolist()
    
    # Ersten und letzten 10 Profile entfernen, da hier oft Fehler auftreten
    y_values = y_values[9:(len(y_values)-10)]
    z_values = z_values[9:(len(z_values)-10)]
    t = t[9:(len(t)-10)]
    
    return y_values, z_values, np.array(t)

def trendreduzierung(zeitreihe, t, rps, brett):
    
    a, b, r, p, std = linregress(t,zeitreihe)
    #print(f'y = {np.round(a,3)} * x + {np.round(b,3)}')
    
    prot(f"Parameter der Trendgeraden: y = {a}*x+{b}\n")
    prot(f"Varianzen der Parameter: {std}\n\n")

    ax = plt.axes()
    ax.plot(t,zeitreihe,'.',label='Zeitreihe')
    ax.plot(t,a*t+b, label='Trendgeraden')

    reduzierte_zeitreihe =  np.array(zeitreihe) - np.array(a*t+b) 
    ax.plot(t,reduzierte_zeitreihe,'.', label='Reduzierte Zeitreihe')
    
    plt.legend()
    plt.ylabel('Z [m]')
    plt.xlabel('Zeit [s]')
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
    plt.savefig(f"Plots/brett{brett}_rps{rps}_reduzierung_zeitreihe.png")
    plt.show()
    return(reduzierte_zeitreihe)

def perform_stft(zeitreihe, segmente, rps, brett):
    
    f, t, Sxx = signal.stft(zeitreihe, 1/(1/50), nperseg=segmente)
    
    plt.pcolormesh(t, f, np.abs(Sxx), vmin=0, shading='gouraud')
    plt.colorbar()
    plt.ylabel('Frequenz [Hz]')
    plt.xlabel('Zeit [s]')
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.0f'))
    plt.savefig(f"Plots/brett{brett}_rps{rps}_spektogramm.png")
    plt.show()
    
    return(f, t, Sxx)


def fourier_reihe(x,*coefs): 
    # Funktion zur Generierung der Fourier Reihe in Abhängigkeit der Anzahl übergebener Koeffizienten
    series = coefs[0] + ( coefs[1] * np.sin( x ) + coefs[2] * np.cos( x ) ) 
    for i in range(3, len(coefs), 2):
        series += ( coefs[i] * np.sin( (i-1) * x ) + coefs[i+1] * np.cos( (i-1) * x ) )
    return  series

def fourier_approximation(t, zeitreihe, n_koeffizienten, von, bis, rps, brett):
    y = zeitreihe[von:bis]
    x = t[von:bis]
    
    p0 = [1 for i in range(n_koeffizienten)] # Näherungswerte für die Ausgleichung
    popt, pcov = curve_fit(fourier_reihe, x, y, p0=p0)
    
    plt.plot(x,y*100,'.',color='red', label='Zeitreihe')
    plt.plot(x, fourier_reihe(x, *popt)*100, color='darkblue', label = 'Approximation')
    plt.ylabel('Z-Abweichung [m]')
    plt.xlabel('Zeit [s]')
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%.0f'))
    plt.savefig(f"Plots/brett{brett}_rps{rps}_approx.png")
    plt.legend()
    plt.show()
    return(popt, pcov)
    
def check_ausreisser(zeitreihe):
    std = np.std(zeitreihe)
    for i in range(0,len(zeitreihe)-1,1):
        if np.abs(np.mean(zeitreihe)-zeitreihe[i]) > 3*std:
            #print("Ausreisser entdeckt")
            zeitreihe[i] = np.mean(zeitreihe[i-20:i+20])
    return(zeitreihe)

def prot(text):
    if write_prot == True:
        with open("Dateien/Protokoll.txt",'a') as out:
            out.write(text)

#%% Daten Einlesen
prot(f"Zeitreihenanalyse für den Datensatz rps{rps} \n\n")
df = pd.read_csv("Testdaten/rps50_synch.txt", sep=';', names=['ProfilNR','PNR','X','Y','Z','I','t'])

try:
    os.remove('Dateien/Protokoll.txt')# Protokoll clear
except:
    None
#%% Bretter identifizieren und Übersicht plotten

bretter = [3375, 4780, 11250, 13800, 16000, 17650]
#bretter = [3375]

prot(f"Interessante Punkte: {bretter} \n\n")
# Ein Profil mit allen Bretterpunkten als Übersicht plotten
y_base = np.array(df['Y'][0:20000])
z_base = np.array(df['Z'][0:20000])


base = plt.plot(y_base, z_base, '.', label='Beispielprofil' )
for brett in bretter:
    plt.plot(df['Y'][brett], df['Z'][brett],'.', color = 'red')
    plt.annotate(
              str(brett), 
             (df['Y'][brett], df['Z'][brett]),
             textcoords="offset points", 
             xytext=(14, -11), 
             ha='center') 
    
plt.ylim(-2,1)
plt.xlim(-1.0,1.2)
plt.ylabel('Z [m]')
plt.xlabel('Y [m]')
ax = plt.gca()
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
plt.savefig(f"Plots/0_übersicht_rps{rps}.png")
plt.show()

# Überprüfen Sie die Frequenzen auf Konstanz oder Variation, indem Sie die Frequenzen im Laufe der Zeit vergleichen
# Die STFT stellen Informationen zu Änderungen der Frequenz über die Zeit bereit

#%% Main Loop für alle Bretter
for brett in bretter:
    prot(f"Starte Analyse für Punkt Nummer {brett} \n\n")
    
    #%% Zeitreihe erstellen
    zeitreihe_y, zeitreihe_z, t = zeitreihe_erstellen(df, brett, 4)
    
    # Ausreisser prüfen
    zeitreihe_z = np.array(check_ausreisser(zeitreihe_z))
    #zeitreihe_y = check_ausreisser(zeitreihe_y)
    
    # Zeitreihe plotten
    plt.plot(t,zeitreihe_z*100,'.')
    plt.ylabel('Z [cm]')
    plt.xlabel('Zeit [s]')
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    plt.savefig(f"Plots/brett{brett}_rps{rps}_zeitreihe.png")
    plt.show()

    np.savetxt(f"Dateien/{brett}_zeitreihe.txt",zeitreihe_z)
    np.savetxt(f"Dateien/{brett}_time.txt",t)

    #%% Trendgeraden bestimmen und Reduzierung vornehmen
    zeitreihe = trendreduzierung(zeitreihe_z, t, rps, brett)
    plt.plot(t,zeitreihe*100,'.')
    
    plt.ylabel('Z [cm]')
    plt.xlabel('Zeit [s]')
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    plt.savefig(f"Plots/brett{brett}_rps{rps}_reduzierte_zeitreihe.png")
    plt.show()
    
    np.savetxt(f"Dateien/{brett}_reduzierte_zeitreihe.txt",zeitreihe)

    
    #%% STFT durchführen und Ergebnisse darstellen
    f, time, Sxx = perform_stft(zeitreihe, 50, rps, brett)
    
    prot("STFT Ergebnisse in Datei gespeichert. Siehe Dateien\n")
        
    np.savetxt(f"Dateien/{brett}_Sxx.txt",Sxx)
    np.savetxt(f"Dateien/{brett}_Frequenzen.txt",f)
    np.savetxt(f"Dateien/{brett}_STFT_Time.txt",time)

    #%% Fourier Reihe bilden
    startpunkt, endpunkt = 300, 1700 # 300,900
    anzahl_koeffizienten = 1101 # (ungerade)  # 501
    param_optimiert,param_covarianz = fourier_approximation(t,zeitreihe,anzahl_koeffizienten,startpunkt,endpunkt, rps, brett)
    
    prot(f"\nFourier-Approximation für Punkt Nummer {brett}\n")
    prot(f"Anzahl der Parameter: {anzahl_koeffizienten}\n")
    prot(f"Betrachtung der Kurve von Index {startpunkt} bis Index {endpunkt}\n\n")
    
    prot("Ergebnisse der Fourier Approximation in Datei gespeichert. Siehe Dateien\n")
    
    np.savetxt(f"Dateien/{brett}_param_cov.txt",param_optimiert)
    np.savetxt(f"Dateien/{brett}_param_opt.txt",param_covarianz)
prot("***END***")   

#%% Reload Data (Test)
#path = r"C:\Users\lukas\Desktop\HCU\Master\Semester 3\Dynamische Messtechnik\Uebungen\Uebung 3\Dateien\8050_Sxx.txt"
#data = np.genfromtxt(path, dtype=np.complex_)

