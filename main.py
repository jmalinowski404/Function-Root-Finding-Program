import numpy as np
import matplotlib.pyplot as plt
import os

def wyczysc_ekran():
    os.system('cls' if os.name == 'nt' else 'clear')

def f_poly(x): return x**3 + 2*x**2 + 4*x + 6
def df_poly(x): return 3*x**2 + 4*x + 4

def f_trig(x): return np.sin(x)
def df_trig(x): return np.cos(x)

def f_exp(x): return np.exp(2*x) - 6
def df_exp(x): return 2 * np.exp(2*x)

def f_comp(x): return np.exp(x) - np.cos(x)
def df_comp(x): return np.exp(x) + np.sin(x)

dostepne_funkcje = {
    1: ("Wielomian: f(x) = x^3 + 2x^2 + 4x + 6", f_poly, df_poly),
    2: ("Trygonometryczna: f(x) = sin(x)", f_trig, df_trig),
    3: ("Wykładnicza: f(x) = e^2x - 6", f_exp, df_exp),
    4: ("Złozona: f(x) = e^x - cos(x)", f_comp, df_comp)
}

def handleBisekcja(func, a, b, typ_warunku, warunek_stopu, licznik_iteracji=1):
    if licznik_iteracji == 1 and (func(a) * func(b) > 0):
        print("[Metoda Bisekcji] Proszę podać poprawny przedział.")
        exit()

    srodek = (a + b) / 2

    if (typ_warunku == "epsilon"):
        if (abs(func(srodek)) < warunek_stopu):
            wyczysc_ekran()
            print(f"[Metoda Bisekcji] Znaleziono pierwiastek: {srodek}")
            print(f"[Metoda Bisekcji] Liczba iteracji: {licznik_iteracji}")
            return srodek

    if (typ_warunku == "iteracje"):
        if (licznik_iteracji >= warunek_stopu):
            print(f"[Metoda Bisekcji] Osiągnieto maksymalna ilość iteracji, znaleziono pierwiastek: {srodek}.")
            print(f"[Metoda Bisekcji] Liczba iteracji: {licznik_iteracji}")
            return srodek

    if (func(srodek) * func(b) < 0):
        return handleBisekcja(func, srodek, b, typ_warunku, warunek_stopu, licznik_iteracji+1)
    
    if (func(srodek) * func(a) < 0):
        return handleBisekcja(func, a, srodek, typ_warunku, warunek_stopu, licznik_iteracji+1)
    
def handleStyczne(func, deriv, start, typ_warunku, warunek_stopu, licznik_iteracji=1):
    if (typ_warunku == "epsilon"):
        if (abs(func(start)) < warunek_stopu):
            print(f"[Metoda Stycznych] Znaleziono pierwiastek: {start}")
            print(f"[Metoda Stycznych] Liczba iteracji: {licznik_iteracji}")
            return start
        
    if (typ_warunku == "iteracje"):
        if (licznik_iteracji >= warunek_stopu):
            print(f"[Metoda Stycznych] Znaleziono pierwiastek: {start}")
            print(f"[Metoda Stycznych] Liczba iteracji: {licznik_iteracji}")
            return start

    wartosc_funkcji = func(start)
    wartosc_pochodnej = deriv(start)

    if (wartosc_pochodnej == 0):
        print("[Metoda Stycznych] Styczna jest pozioma, znajdujemy się w ekstremum funkcji.")
        exit()
    
    x = start - (wartosc_funkcji / wartosc_pochodnej)
    return handleStyczne(func, deriv, x, typ_warunku, warunek_stopu, licznik_iteracji+1)

def handleFunction(func, deriv):
    wyczysc_ekran()

    print("1. Określ przedział poszukiwanych miejsc zerowych.")
    dolna_granica = float(input("Określ dolną granicę: "))
    gorna_granica = float(input("Określ górną granicę: "))

    wyczysc_ekran()

    print("2. Wybierz kryterium stopu algorytmu.")
    print("     a) Spełnienie warunku nałożonego na dokładność")
    print("     b) Osiągnięcie zadanej liczby iteracji")
    kryterium_stopu = input("Wybór: ")

    if (kryterium_stopu == "a"):
        wyczysc_ekran()
        print("3. Ustaw epsilon.")
        warunek_stopu = float(input("𝜀: "))
        typ_warunku = "epsilon"

    if (kryterium_stopu == "b"):
        wyczysc_ekran()
        print("3. Ustaw liczbę iteracji.")
        warunek_stopu = int(input("iter: "))
        typ_warunku = "iteracje"

    handleBisekcja(func, dolna_granica, gorna_granica, typ_warunku, warunek_stopu)
    handleStyczne(func, deriv, dolna_granica, typ_warunku, warunek_stopu)

    fig, ax = plt.subplots()

    x = np.linspace(dolna_granica - 1, gorna_granica + 1, 100)
    y = func(x)

    plt.plot(x, y, label="f(x)", color="blue")

    plt.axhline(0, color="black", linewidth="1")

    wynik_bisekcji = handleBisekcja(func, dolna_granica, gorna_granica, typ_warunku, warunek_stopu)
    wynik_stycznych = handleStyczne(func, deriv, dolna_granica, typ_warunku, warunek_stopu)

    if wynik_bisekcji is not None:
        plt.scatter(wynik_bisekcji, func(wynik_bisekcji), color="navy", s=150, zorder=5, label="Metoda bisekcja")
        format_bisekcji = f"{wynik_bisekcji:.8f}"
        plt.annotate(
            format_bisekcji, 
            xy=(wynik_bisekcji, func(wynik_bisekcji)),
            xytext=(-40, 40),
            textcoords="offset points",
            ha="right",
            rotation=45,
            bbox=dict(boxstyle="round,pad=0.3", fc="gray", ec="navy", alpha=0.8),
            arrowprops=dict(arrowstyle="->")
        )
    
    if wynik_stycznych is not None:
        plt.scatter(wynik_stycznych, func(wynik_stycznych), color="darkorange", marker="x", s=200, zorder=5, label="Metoda stycznych")
        format_stycznych = f"{wynik_stycznych:.8f}"
        plt.annotate(
            format_stycznych, 
            xy=(wynik_stycznych, func(wynik_stycznych)), 
            xytext=(40, -40), 
            textcoords="offset points",
            ha="left",
            rotation=45,
            bbox=dict(boxstyle="round,pad=0.3", fc="gray", ec="darkorange"
            "", alpha=0.8),
            arrowprops=dict(arrowstyle="->")
        )

    plt.title("Miejsca zerowe zadanej funkcji na zadanym przedziale.")
    plt.legend()
    plt.grid()

    plt.show()

def wyborFunkcji():
    print("--------[ NUMERKI ]--------")
    print("")
    print("Wybierz jedną z dostępnych funkcji: ")
    for klucz, wartosc in dostepne_funkcje.items():
        print(f"{klucz}. {wartosc[0]}")

    print("")
    wybor = input("Wybór: ")

    if (wybor == "1"):
        nazwa, funkcja, pochodna = dostepne_funkcje[1]
        handleFunction(funkcja, pochodna)
    
    if (wybor == "2"):
        nazwa, funkcja, pochodna = dostepne_funkcje[2]
        handleFunction(funkcja, pochodna)

    if (wybor == "3"):
        nazwa, funkcja, pochodna = dostepne_funkcje[3]
        handleFunction(funkcja, pochodna)

    if (wybor == "4"):
        nazwa, funkcja, pochodna = dostepne_funkcje[4]
        handleFunction(funkcja, pochodna)

if __name__ == "__main__":
    wyborFunkcji()