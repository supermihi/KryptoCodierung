# -*- coding: utf-8 -*-
# Lösungsvorschläge zum Übungsblatt 4

# ==================================================
# Aufgabe 4.3 - Knacken affin linearer Blockchiffren
# ==================================================

import krypto1 # Funktionen aus der 1. Übung importieren (muss im selben Ordner liegen)
import numpy as np # numpy erlaubt das Rechnen mit Matrizen und Vektoren


def invertZN(a, N):
    """Berechnet das Inverse eines Elements a von Z_N, falls möglich, mit dem
    erweiterten euklidischen Algorithmus.
    """
    # erweiterter ggt-Alg. (von Wikipedia)
    t = 0
    newt = 1
    r = N
    newr = a
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        raise ValueError('{} nicht invertierbar mod {}'.format(a, N))
    return t if t >= 0 else t + N


def invertierbar(a, N):
    """Gibt an ob eine Zahl a invertierbar in Z_N ist."""
    return krypto1.ggT(a, N) == 1


def invertMatrixZN(M, N):
    """Invertiert eine Matrix M in ZN mit dem Gauss-Jordan-Algorithmus, indem
    die Matrix zu einer Einheitsmatrix umgeformt und die entsprechenden Schritte
    auf einer Einheitsmatrix wiederholt werden, die dann am Schluss die Inverse
    darstellt.
    """
    n = M.shape[0]  # shape = (nzeilen, nspalten), also shape[0] = nzeilen
    M = M.copy() # nicht an der Originalmatrix rumspielen
    I = np.identity(n, int) # Einheitsmatrix -> wird später das Ergebnis
    for row in range(n):
        if not invertierbar(M[row, row], N):
            # müssen Zeilen tauschen
            for j in range(row+1, n):
                if invertierbar(M[j, row], N):
                    tmp = M[row, :].copy()
                    M[row, :] = M[j, :]
                    M[j, :] = tmp
                    tmp = I[row, :].copy()
                    I[row, :] = I[j, :]
                    I[j, :] = tmp
                    break
            else:
                # hier kommen wir hin wenn die for-Schleife nicht durch ein
                # break beendet wurde, also keine geeignete Zeile zum Tauschen
                # existiert
                raise ValueError("Matrix nicht invertierbar")
        # Zeile mit dem Inversen des Pivot-Elements multiplizieren, um eine 1
        # auf der Diagonalen zu erreichen
        faktor = invertZN(M[row, row], N)
        M[row, :] = (M[row, :] * faktor) % N
        I[row, :] = (I[row, :] * faktor) % N
        
        # Nullen unterhalb des aktuellen Pivots erzeugen
        for j in range(row + 1, n):
            if invertierbar(M[j, row], N):
                faktor = invertZN(M[j, row], N)
                M[j, :] = (M[j, :] * faktor - M[row, :]) % N
                I[j, :] = (I[j, :] * faktor - I[row, :]) % N
            elif M[j, row] != 0:
                # In Z_N können Nullteiler auftreten, z.B. die 8 in Z_{12}.
                # Um dort eine 0 zu erzeugen, müssen wir mit dem kgV der beiden
                # Zahlen multiplizieren. Da ggt*kgv = mn gilt, können wir dazu
                # den bereits implementierten ggt-Algorithmus nehmen.
                faktor = N * M[j, row] // krypto1.ggT(N, M[j, row])
                M[j, :] = (M[j, :] * faktor) % N
                I[j, :] = (I[j, :] * faktor) % N
    # jetzt haben wir eine obere Dreiecksmatrix. Um daraus eine Diagonalmatrix
    # zu machen, müssen wir nun noch einmal von unten nach oben durchgehen
    # um die Einträge oberhalb der Diagonalen zu Nullen zu machen.
    for row in range(n-1, -1, -1):
        for j in range(row + 1, n):
            faktor = M[row, j]
            M[row, :] = (M[row, :] - faktor*M[j, :]) % N
            I[row, :] = (I[row, :] - faktor*I[j, :]) % N
    return I
        

def breakAffineLinear(n, klartexte, chiffretexte):
    """Knackt eine affin lineare Blockchiffre auf dem lateinischen Alphabet mit
    Blocklänge n unter Angabe von n+1 Klartexten und zugehörigen Chiffretexten,
    die jeweils als Textstring gegeben sein müssen.
    """
    P = np.zeros((n, n), int)
    C = np.zeros((n, n), int)
    # Klartexte vom zweiten (Index 1) an durchgehen, in Zahlen konvertieren,
    # in die i-te Spalte der Matrix schreiben, und anschließend den Nullten
    # Klartext abziehen -> ergibt Matrix P
    for i, p in enumerate(klartexte[1:]):
        P[:, i] = krypto1.wortZuZahlen(p)
        P[:, i] -= krypto1.wortZuZahlen(klartexte[0])
    # gleiches gilt für Matrix C mit den Chiffretexten
    for i, x in enumerate(chiffretexte[1:]):
        C[:, i] = krypto1.wortZuZahlen(x)
        C[:, i] -= krypto1.wortZuZahlen(chiffretexte[0])
    # P invertieren mit obigem Algorithmus, in Z26
    Pinv = invertMatrixZN(P, 26)
    # np.dot führt Matrix-Multiplikation durch
    A = np.dot(C, Pinv) % 26
    b = (C[:, 0] - np.dot(A, P[:, 0])) % 26
    return A, b
    
# testen von breakAffineLinear am Beispiel aus der Übungsaufgabe
klar = ["AA", "HA", "ND"]
versch = ["AA", "FO", "OT"]
A, b = breakAffineLinear(2, klar, versch)
print(A, b)


# ==================================
# Aufgabe 4.4 - Verschlüsselungsmodi
# ==================================    

def cryptVernamNumpy(message, key):
    """Ver- und Entschlüsselungsfunktion für das Vernam One-Time-Pad. Sowohl
    die Nachricht (message) als auch der Schlüssel (key) müssen Numpy-Arrays
    gleicher Länge sein.
    """
    return (message + key) % 2


def ECB(klartexte, verschFn, schlüssel):
    ciphertexte = []
    for text in klartexte:
        ciphertexte.append(verschFn(text, schlüssel))
    return ciphertexte


def CBC(klartexte, c0, verschFn, schlüssel):
    ciphertexte = []
    cAktuell = c0
    for text in klartexte:
        cAktuell = verschFn((text + cAktuell) % 2, schlüssel)
        ciphertexte.append(cAktuell)
    return ciphertexte
    
def CFB(klartexte, c0, verschFn, schlüssel):
    ciphertexte = []
    cAktuell = c0
    for text in klartexte:
        cAktuell = (text + verschFn(cAktuell, schlüssel)) % 2
        ciphertexte.append(cAktuell)
    return ciphertexte
    
def OFB(klartexte, c0, verschFn, schlüssel):
    ciphertexte = []
    sAktuell = c0  # s_0 = c_0
    for text in klartexte:
        sAktuell = verschFn(sAktuell, schlüssel)
        ciphertexte.append((text + sAktuell) % 2)
    return ciphertexte
        
schlüssel = np.array([1, 0, 1, 1])
c0 = np.array([0, 0, 1, 1])
p = [np.array([0, 1, 0, 0]), np.array([0, 1, 0, 0]),
     np.array([1, 1, 1, 0]), np.array([1, 0, 1, 1])]

print('Verschlüsselungsmodi - Verschlüsseln')
print('ECB:')
print(ECB(p, cryptVernamNumpy, schlüssel))
print('CBC:')
print(CBC(p, c0, cryptVernamNumpy, schlüssel))
print('CFB:')
print(CFB(p, c0, cryptVernamNumpy, schlüssel))
print('OFB:')
print(OFB(p, c0, cryptVernamNumpy, schlüssel))

deECB = ECB  # bei ECB sind Ver- und Enschlüsseln symmetrisch, nur dass beim
             # Entschlüsseln ggf. die Entschlüsselungsfunktion und der
             # Entschlüsselungsschlüssel verwendet werden müssen

def deCBC(ciphertexte, c0, entschFn, schlüssel):
    klartexte = []
    cAktuell = c0
    for ciph in ciphertexte:
        klartexte.append((entschFn(ciph, schlüssel) - cAktuell) % 2)
        cAktuell = ciph
    return klartexte

def deCFB(ciphertexte, c0, verschFn, schlüssel):
    """Zum Entschlüsseln eines CFB-verschlüsselten Texts braucht man nur die
    Verschlüsselungsfunktion; dies macht also nur bei symmetrischen Verfahren
    Sinn.
    """
    klartexte = []
    cAktuell = c0
    for ciph in ciphertexte:
        klartexte.append((ciph - verschFn(cAktuell, schlüssel)) % 2)
        cAktuell = ciph
    return klartexte
    
deOFB = OFB  # bei OFB sind Ver- und Enschlüsseln symmetrisch
    
c = [np.array([1, 1, 0, 1]), np.array([1, 1, 0, 1]),
     np.array([0, 0, 1, 0]), np.array([1, 0, 0, 1])]
print('Verschlüsselungsmodi - Entschlüsseln')
print('ECB:')
print(deECB(c, cryptVernamNumpy, schlüssel))
print('CBC:')
print(deCBC(c, c0, cryptVernamNumpy, schlüssel))
print('CFB:')
print(deCFB(c, c0, cryptVernamNumpy, schlüssel))
print('OFB:')
print(deOFB(c, c0, cryptVernamNumpy, schlüssel))