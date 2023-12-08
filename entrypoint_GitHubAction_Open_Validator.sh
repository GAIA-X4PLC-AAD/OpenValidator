result=$(python main.py /app/$1 -o "/app/$2")
exit_code=$?
echo "result : $result"
echo "EXIT CODE : $exit_code"
echo "param 1 : ($1)"
echo "param 2 : ($2)"
if [ $exit_code -eq 1 ]; then
    echo "success"
    exit 0
else
    echo "failure"
    exit 1
fi
# exit code
# if [ $? -eq 0 ]; then
#     echo "success"
#     echo "::set-output name=exit_code::0"
#     # time=$(date)
#     # echo "time=$time, output=/data, sucess" >> $GITHUB_OUTPUT
#     # exit 0
# else
#     echo "failure"
#     echo "::set-output name=exit_code::1"
#     # time=$(date)
#     # echo "time=$time, output=/data, failure" >> $GITHUB_OUTPUT
#     # exit 1
# fi