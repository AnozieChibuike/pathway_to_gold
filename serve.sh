#!/bin/bash
source .venv/bin/activate
gunicorn --reload --log-level debug -b 127.0.0.1:8000 main:app