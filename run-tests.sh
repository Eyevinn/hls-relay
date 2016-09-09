#!/bin/bash
function install_deps {
    pip install -r requirements-dev.txt
}

function run {
    python tests/mockserver.py &
    PYTHONPATH=. py.test -vv --cov-report term-missing --cov hlsrelay tests/
    ps ax | grep "python tests/mockserver.py" | grep -v grep | cut -d ' ' -f 1 | xargs kill
}

function main {
    install_deps
    run
    retval=$?
    return "$retval"
}

if [ -z "$1" ]; then
    main
else
    $@
fi

