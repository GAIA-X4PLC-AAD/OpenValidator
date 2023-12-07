#!/bin/bash


# file=$(find data/inputs -type f -name "0" -print -quit)

# cp "$file" data/inputs

# python3 main.py "$file"

# cp -r /app/reports data/outputs

# python main.py data/inputs/0 -o data/outputs/
echo $1
echo $2
python main.py /app/$1 -o /app/$2