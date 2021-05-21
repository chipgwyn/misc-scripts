# the "dly" function
dly ()
{
    datepath=$(date "+%Y/%m/%d")
    if [ -d ~/daily_log/$datepath ]; then
        cd ~/daily_log/$datepath;
    else
        mkdir -p ~/daily_log/$datepath;
        cd ~/daily_log/$datepath;
    fi
}
