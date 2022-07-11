#!/bin/sh
supression="0.05 0.1"
k="5 10 15 20"

rm results/step3/*
rm logNaiv
touch logNaiv

echo "associationNaiv time" >> logNaiv
time -p -o logNaiv -a python3 ./python/associationNaiv.py
javac -cp ./java/libarx-3.9.0.jar ./java/arx/Main.java

for i in $supression
do
for j in $k
do
echo "limit k=$j supression=$i" >> logNaiv
time -p -o logNaiv -a java -Dfile.encoding=Cp1252 -cp "./java/libarx-3.9.0.jar:./java/" arx.Main ./results/step1/associationNaiv.csv $j $i >> logNaiv
python3 ./python/summarize.py $j.$i
done
done