returns=$(python main.py /app/$1 -o "/app/$2" -e exit-if-error)
exit_code=$?
time=$(date)
echo "returns : $returns"
echo "EXIT CODE : $exit_code"
echo "Input File : ($1)"
echo "Output Dir : ($2)"
# echo $(python3 -c "import sys, json; print(json.loads('{\"output\":\"$2\", \"validation\":\"success\"}')[\"validation\"])")
if [ $exit_code -eq 0 ]; then
    echo "validation_status : success"
    echo "validation_status=success" >> $GITHUB_OUTPUT
    echo "validation_result={\"output\":\"$2\", \"validation\":\"success\"}" >> $GITHUB_OUTPUT
    exit 0
else
    echo "validation_status : failure"
    echo "validation_status=failure" >> $GITHUB_OUTPUT
    echo "validation_result={\"output\":\"$2\", \"validation\":\"failure\"}" >> $GITHUB_OUTPUT
    exit 1
fi