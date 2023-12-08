returns=$(python main.py /app/$1 -o "/app/$2")
exit_code=$?
time=$(date)
echo "returns : $returns"
echo "EXIT CODE : $exit_code"
echo "param 1 : ($1)"
echo "param 2 : ($2)"
if [ $exit_code -eq 0 ]; then
    echo "success"
    echo "validation_result={"time":"$time", "output":"$2", "validation":"success"}" >> $GITHUB_OUTPUT
    exit 0
else
    echo "failure"
    echo "validation_result={"time":"$time", "output":"$2", "validation":"failure"}" >> $GITHUB_OUTPUT
    exit 1
fi