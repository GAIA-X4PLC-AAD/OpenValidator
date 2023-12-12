#!/bin/bash

echo "Param 1 : ($1)"
echo "Param 2 : ($2)"
echo "Param 3 : ($3)"
echo "Param 4 : ($4)"

returns=$(python main.py /app/$3 -o "/app/$4" -e exit-if-error)
exit_code=$?
time=$(date)
echo "returns : $returns"
echo "EXIT CODE : $exit_code"
echo "Input File : ($3)"
echo "Output Dir : ($4)"
# echo $(python3 -c "import sys, json; print(json.loads('{\"output\":\"$2\", \"validation\":\"success\"}')[\"validation\"])")
if [ $exit_code -eq 0 ]; then
    echo "validation_status : success"
    echo "validation_status=success" >> $GITHUB_OUTPUT
    echo "validation_result={\"output\":\"$4\", \"validation\":\"success\"}" >> $GITHUB_OUTPUT
    exit 0
else
    echo "validation_status : failure"
    echo "validation_status=failure" >> $GITHUB_OUTPUT
    echo "validation_result={\"output\":\"$4\", \"validation\":\"failure\"}" >> $GITHUB_OUTPUT
    exit 1
fi