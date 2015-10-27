# -*- coding: utf-8 -*-
# Lösungsvorschläge zum Übungsblatt 5

import krypto4
# ===========================================
# Aufgabe 5.4 - Implementierung RSA-Verfahren
# ===========================================


def encryptRSA(n, e, message):
    """Verschlüsselt die Zahl *message* mittels RSA-Verfahren mit dem
    öffentlichen Schlüssel (n, e)."""
    k = n.bit_length() - 1
    assert message < 2**k
    return (message ** e) % n
    
n = 22
e = 7
message = 5
print("Schlüssel: ", n, e)
print("Verschlüssele Nachricht", message)
print("Chiffretext:", encryptRSA(n, e, message))

def generateD(q1, q2, e):
    """Erzeugt *d* aus der Faktorisierung q1*q2 = n und e. Dazu wird zunächst
    φ(n) = (q1-1)(q2-1) berechnet und dann d als inverses von e in Z_{φ(n)}.
    """
    phi = (q1-1)*(q2-1)
    return krypto4.invertZN(e, phi)
    
def decryptRSA(n, d, e, chiffretext):
    """Enschlüsselt *chiffretext* mit dem RSA-Verfahren bei gegebenem
    Entschlüsselungsschlüssel (n, d, e).
    """
    return (chiffretext**d) % n
    
d = generateD(11, 2, 7)
print("d =", d)
chiffre = 15
print("Enschlüssele", chiffre)
print("Ergebnis:", decryptRSA(n, d, e, chiffre))