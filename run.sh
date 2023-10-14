#!/bin/bash

# Lista de argumentos que você quer passar para as instâncias
alg=("B" "I" "U" "A" "G" "H")

# Loop para percorrer os argumentos e rodar o programa
for arg in "${alg[@]}"
do
    python3 TP1.py $arg 8 4 7 6 2 3 5 1 0 PRINT > $arg.out &
done

# Espera todos os processos terminarem
wait
