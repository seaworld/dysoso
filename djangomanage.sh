#!/bin/bash
PROJDIR=/home/code/dysoso
PIDFILE=$PROJDIR/django.pid
cd $PROJDIR
func_kill_py(){
    if [ -f $PIDFILE ]; then
        kill `cat $PIDFILE`
        rm -f $PIDFILE
    fi
}
if [ "$1" = "stop" ]; then
    printf “Stop django…\n”;
    func_kill_py
elif [ "$1" = "start" ] || [ "$1" = "restart" ]; then
    printf “Start django…\n”;
    func_kill_py;
    exec python manage.py runfcgi method=threaded host=0.0.0.0 port=8000 pidfile=$PIDFILE
fi
