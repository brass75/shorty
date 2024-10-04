#!/bin/bash

cd /app/src
export PYTHONPATH=/app:$PYTHONPATH
gunicorn app:app --config ../gunicorn-config.py
