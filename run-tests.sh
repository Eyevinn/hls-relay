#!/bin/bash
function install_deps {
    pip install -r requirements-dev.txt
}

function run {
    PYTHONPATH=. py.test -vv --cov-report term-missing --cov hlsrelay tests/
}

function main {
    install_deps
    python tests/mockserver.py &
    run
    retval=$?
    ps ax | grep "python tests/mockserver.py" | grep -v grep | cut -d ' ' -f 1 | xargs kill
    return "$retval"
}

if [ -z "$1" ]; then
    main
else
    $@
fi

