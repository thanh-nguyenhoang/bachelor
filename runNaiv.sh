#! /bin/sh
python3 ./python/associationNaiv.py
javac -cp ./java/libarx-3.9.0.jar ./java/arx/Main.java
java -Dfile.encoding=Cp1252 -cp "./java/libarx-3.9.0.jar:./java/" arx.Main ./results/step1/associationNaiv.csv 2
python3 ./python/summarize.py