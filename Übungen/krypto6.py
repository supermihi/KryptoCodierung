# -*- coding: utf-8 -*-
# Lösungsvorschläge zum Übungsblatt 6

import numpy as np

def millerRabin(n):
    """Führt den Miller-Rabin-Test mit *n* durch, um abzuschätzen, ob n eine
    Primzahl ist oder nicht. Gibt True zurück, wenn der Test bestanden wird,
    sonst False.
    """
    s = 0
    t = n - 1
    while t % 2 == 0:
        s += 1
        t = t // 2
    a = np.random.randint(1, n)
    if a**t % n == 1:
        return True
    for r in range(s):
        if a**(2**r*t) % n == n-1:
            return True
    return False


def erzeugePrimzahl(size, eps):
    """Erzeugt einen Kandidaten für eine Primzahl, dessen Binärdarstellung die Länge *size* hat und der
    mit Fehlerwahrscheinlichkeit kleiner *eps* tatsächlich eine Primzahl ist.
    """
    # Anzahl Runden berechnen, die wir brauchen, um die gewünschte
    # Fehlerwahrscheinlichkeit p zu erreichen.  Es soll gelten p < 0.25^n < eps
    runden = int(np.ceil(np.log(eps) / np.log(0.25)))

    while True:
        # Primzahlkandidaten der Länge <size> erstellen
        n = np.random.randint(2**(size-1), 2**size)
        if n % 2 == 0 or n % 3 == 0 or n % 5 == 0:
            # ist der Primazahlkandidat durch 2, 3 oder 5 teilbar, wird ein neuer erzeugt
            continue
        print('Teste {}'.format(n))
        for runde in range(runden):
            # den Primzahlkandidaten runden-mal mit millerRabin testen
            if not millerRabin(n):
                # gibt ein Test False zurück, wird ein neuer Kandidat erzeugt
                break
        else:
            return n


erzeugePrimzahl(20, .01)