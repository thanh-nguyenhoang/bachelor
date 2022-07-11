#!/bin/sh
supression="0.05 0.1"
k="5 10 15 20"

rm results/step3/*
rm logMSA
touch logMSA

echo "associationMSA time" >> logMSA
time -p -o logMSA -a python3 ./python/associationMSA.py
javac -cp ./java/libarx-3.9.0.jar ./java/arx/Main.java

for i in $supression
do
for j in $k
do
echo "limit k=$j supression=$i" >> logMSA
time -p -o logMSA -a java -Dfile.encoding=Cp1252 -cp "./java/libarx-3.9.0.jar:./java/" arx.Main ./results/step1/associationMSA.csv $j $i >> logMSA
python3 ./python/summarize.py $j.$i
done
done