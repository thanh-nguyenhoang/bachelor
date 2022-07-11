#! /bin/sh
supression="0.1"
k="2"
python3 ./python/associationMSA.py
javac -cp ./java/libarx-3.9.0.jar ./java/arx/Main.java
java -Dfile.encoding=Cp1252 -cp "./java/libarx-3.9.0.jar:./java/" arx.Main ./results/step1/associationMSA.csv $k $supression
python3 ./python/summarize.py $k.$supression