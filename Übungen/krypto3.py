# -*- coding: utf-8 -*-
# Lösungsvorschläge zum Übungsblatt 3

# =================================
# Aufgabe 3.1 - Vernam One-Time Pad
# =================================

def cryptVernam(message, key):
    """Ver- und Entschlüsselungsfunktion für das Vernam One-Time-Pad. Sowohl
    die Nachricht (message) als auch der Schlüssel (key) müssen {0,1}-Wörter
    gleicher Länge sein.
    """
    if len(message) != len(key):
        # die "raise"-Konstruktion kann benutzt werden, um einen Fehler im 
        # Programmablaufauszulösen. Hier dadurch aufgetreten, dass der Benutzer
        # die Funktion inkorrekt (mit nicht gleich langen Parametern) aufgerufen
        # hat.
        raise ValueError("Vernam OneTime-Pad benötigt Schlüssellänge = Klartextlänge")
    ans = []
    for messageBit, keyBit in zip(message, key):
        ans.append((messageBit + keyBit) % 2)
    return ans
    # Kurzform: return [m^k for m, k in zip(message, key)]
    
print('VERNAM ONE-TIME PAD BEISPIEL')
vernamKey = [0,1,1,1,0,1,1,0]
vernamMsg = [0,0,0,0,1,1,1,1]
print('Klartextnachricht: ', vernamMsg)
vernamVersch = cryptVernam(vernamMsg, vernamKey)
print('Verschlüsselt:', vernamVersch)
vernamEntsch = cryptVernam(vernamVersch, vernamKey)
print('Entschlüsselt:', vernamEntsch)


# die Variante oben erlaubt nur {0,1}-Wörter als Nachrichtentext und Schlüssel.
# Um richtigen Text zu verschlüsseln, müsste dieser zuerst in ein solches Wort
# konvertiert werden. Alternativ können wir die Vernam-Funktion so umschreiben,
# dass sie direkt auf Byte-Ebene (1 Byte = 8 Bit) arbeitet. Dazu brauchen wir
# als Schlüssel zufällige Bytes, und der Klartext muss mit encode() in ein
# Bytes-Objekt umgewandelt werden.


def cryptVernamBytes(message, key):
    """Ver- und Entschlüsselung mit Vernam One-Time Pad auf Byte-Ebene. Sowohl
    *message* als auch *key* müssen vom Typ bytes sein und gleiche Länge haben.
    """
    assert len(key) == len(message)
    return bytes([x^y for x, y in zip(message, key)])
    # die Einträge eines bytes-Objekts sind einfache Integer-Zahlen mit Werten
    # zwischen 0 und 255. Die Operation x^y ist das sogenannte "bitweise XOR",
    # Sie entspricht der GF(2)-Addition der einzelnen Bits in der binären
    # Zahldarstellung. Es werden also immer 8 Bits (1 Byte) auf einmal
    # verschlüsselt.

import os
nachricht = 'SUPER GEHEIME UNNÖTIGE NACHRICHT!!'
print('Nachricht:', nachricht)
nachrichtBytes = nachricht.encode()
print('Nachricht, als Bytes:', nachrichtBytes) # man sieht: Ö wurde zu zwei bytes!
vernamKeyBytes = os.urandom(len(nachrichtBytes))  # urandom erzeugt zufällige Bytes
print('Schlüssel:', vernamKeyBytes)
vernamBytesVersch = cryptVernamBytes(nachrichtBytes, vernamKeyBytes)
print('Chiffretext:', vernamBytesVersch)
vernamBytesEntsch = cryptVernamBytes(vernamBytesVersch, vernamKeyBytes)
print('Entschlüsselt:', vernamBytesEntsch.decode()) # decode() bringt uns das Ö wieder