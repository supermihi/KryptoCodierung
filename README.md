# Vorlesungsunterlagen zur Einführung in die Kryptographie, Informations- und Codierungstheorie

Dieses Repository enthält die TeX-Quellen zu einem Skript, Übungsblättern und begleitenden Folienvorträgen für eine vierstündige Vorlesung zum o.g. Thema.

Im Folgenden einige Hinweise zum Übersetzen der Quellen:
## Compiler
Das Skript (`Skript/main.tex`) sowie die Übungen (im Ordner `Übungen`) müssen mit `lualatex` übersetzt werden, da einige spezifische Features dieses Compilers verwendet werden. Die Vorträge hingegen laufen auch mit dem herkömmlichen `pdflatex`-Compiler.

## Pakete
Neben aktuellen Standardpaketen aus dem CTAN-Archiv verwenden wir das `mh_basic`-Paket sowie die Übungsblattklasse `mh_exsheet`; beide sind [hier](https://github.com/supermihi/latex)  erhältlich.
## Bibliographie
Die Bibliographie wird mit `biblatex`und `biber` erstellt.