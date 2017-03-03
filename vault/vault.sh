
start() {
    /usr/bin/vault server -config=/etc/vault.d &
    return $?
}

stop(){
    kill $(ps -C vault|awk 'END {print $1')
    return $?
}

status(){
    if [ -z $(ps -C vault|awk 'END {print $1}'|grep -v PID) ]; then
        echo "Vault is not running"
        return 3
    else
        /usr/bin/vault status -address=http://$(cat /etc/vault.d/config.json | awk '/address/ {x=$3} END {print x}'|sed 's/"//g')
        return $?
    fi
}

case "$1" in
    start)
        start
        RETVAL=$?
        ;;
    stop)
        stop
        RETVAL=$?
        ;;
    status)
        status
        RETVAL=$?
        ;;
    *)
        echo $"Usage: vault {start|stop|status}"
        RETVAL=2
        ;;
esac