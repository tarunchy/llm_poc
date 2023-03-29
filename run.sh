#!/bin/bash
export FLASK_APP=app.py
export FLASK_ENV=development
gunicorn --bind dlyog02:8000 app:app --pid app_id --timeout 0

