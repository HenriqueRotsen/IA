#!/bin/bash

# Lista de argumentos que você quer passar para as instâncias
alg=("B" "I" "U" "A" "G" "H")

# Loop para percorrer os argumentos e rodar o programa
for arg in "${alg[@]}"
do
    python3 TP1.py $arg 8 6 7 2 5 4 3 0 1 PRINT > $arg.out &
done

# Espera todos os processos terminarem
wait