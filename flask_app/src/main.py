from __future__ import absolute_import, print_function

import logging
import multiprocessing
import os
import signal
import subprocess
import sys


logging.root.setLevel(logging.INFO)

CPU_COUNT = multiprocessing.cpu_count()

MODEL_SERVER_TIMEOUT = os.environ.get("MODEL_SERVER_TIMEOUT", 60)
MODEL_SERVER_WORKERS = int(os.environ.get("MODEL_SERVER_WORKERS", CPU_COUNT))


def sigterm_handler(nginx_pid, gunicorn_pid):
    try:
        os.kill(nginx_pid, signal.SIGQUIT)
    except OSError:
        pass
    try:
        os.kill(gunicorn_pid, signal.SIGTERM)
    except OSError:
        pass

    sys.exit(0)


def serve():
    logging.info("Starting the inference server with {} workers.".format(MODEL_SERVER_WORKERS))

    # link the log streams to stdout/err so they will be logged to the container logs
    subprocess.check_call(["ln", "-sf", "/dev/stdout", "/var/log/nginx/access.log"])
    subprocess.check_call(["ln", "-sf", "/dev/stderr", "/var/log/nginx/error.log"])

    nginx = subprocess.Popen(["nginx", "-c", "/opt/program/nginx.conf"])
    gunicorn = subprocess.Popen(["gunicorn",
                                 "--timeout", str(MODEL_SERVER_TIMEOUT),
                                 "-k", "sync",
                                 "-b", "unix:/tmp/gunicorn.sock",
                                 "-w", str(MODEL_SERVER_WORKERS),
                                 "wsgi:app"])

    signal.signal(signal.SIGTERM, lambda a, b: sigterm_handler(nginx.pid, gunicorn.pid))

    # If either subprocess exits, so do we.
    pids = set([nginx.pid, gunicorn.pid])
    while True:
        pid, _ = os.wait()
        if pid in pids:
            break

    sigterm_handler(nginx.pid, gunicorn.pid)
    logging.info("Inference server exiting")


if __name__ == "__main__":
    if sys.argv[1] == "serve":
        logging.info("Starting the inference server.")
        serve()
