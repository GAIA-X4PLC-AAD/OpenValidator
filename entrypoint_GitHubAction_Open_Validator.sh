echo $1
echo $2
python main.py /app/$1 -o "/app/$2"
echo " EXIT CODE : $?"
echo "param 1 : ($1)"
echo "param 2 : ($2)"
exit 0
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