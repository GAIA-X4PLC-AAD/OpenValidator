#!/bin/bash

# i : input file
# o : output dir
# t : type of execution // docker or github
# e : exit if error // true or false

input_file="data/inputs/sampleODR"
output_dir="data/outputs"
type_of_execution="docker"
exit_if_error="false"

while getopts i:o:e:t: flag
do
    case "${flag}" in
        i) input_file=${OPTARG};;
        o) output_dir=${OPTARG};;
        t) type_of_execution=${OPTARG};;
        e) exit_if_error=${OPTARG};;
    esac
done

echo "Param 1 : ($1)"
echo "Param 2 : ($2)"
echo "Param 3 : ($3)"
echo "Param 4 : ($4)"
echo "Param 5 : ($5)"
echo "Param 6 : ($6)"
echo "Param 7 : ($7)"
echo "Param 8 : ($8)"

echo "Input File : ($input_file)"
echo "Output Dir : ($output_dir)"
echo "Type of Execution : ($type_of_execution)"
echo "Exit if Error : ($exit_if_error)"

if [ $exit_if_error == true ]; then
    returns=$(python main.py /app/$input_file -o "/app/$output_dir" -e exit-if-error)
else
    returns=$(python main.py /app/$input_file -o "/app/$output_dir")
fi
exit_code=$?
time=$(date)
echo "Returns : $returns"
echo "EXIT CODE : $exit_code"
echo "Input File : ($input_file)"
echo "Output Dir : ($output_dir)"
# echo $(python3 -c "import sys, json; print(json.loads('{\"output\":\"$2\", \"validation\":\"success\"}')[\"validation\"])")
if [ $exit_code -eq 0 ]; then
    echo "validation_status : success"
    if [ $type_of_execution == "github" ]; then
        echo "validation_status=success" >> $GITHUB_OUTPUT
        echo "validation_result={\"output\":\"$output_dir\", \"validation\":\"success\"}" >> $GITHUB_OUTPUT
    else
        echo "validation_status=success"
        echo "validation_result={\"output\":\"$output_dir\", \"validation\":\"success\"}"
    fi
    exit 0
else
    echo "validation_status : failure"
    if [ $type_of_execution == "github" ]; then
        echo "validation_status=failure" >> $GITHUB_OUTPUT
        echo "validation_result={\"output\":\"$output_dir\", \"validation\":\"failure\"}" >> $GITHUB_OUTPUT
    else
        echo "validation_status=failure"
        echo "validation_result={\"output\":\"$output_dir\", \"validation\":\"failure\"}"
    fi
    exit 1
fi