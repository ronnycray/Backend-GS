#!/bin/sh

/usr/local/bin/gunicorn -k uvicorn.workers.UvicornWorker services.main:app --bind "0.0.0.0:8000"