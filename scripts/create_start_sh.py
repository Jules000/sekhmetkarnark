#!/usr/bin/env python
"""Create start.sh with proper Unix line endings."""
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
start_sh_path = os.path.join(project_dir, "start.sh")

content = (
    "#!/bin/bash\n"
    "set -e\n"
    "\n"
    'PORT="${PORT:-8000}"\n'
    'echo "Starting gunicorn on port $PORT..."\n'
    "\n"
    "python manage.py migrate --noinput --settings=config.settings.production\n"
    "\n"
    "python manage.py collectstatic --noinput --settings=config.settings.production || true\n"
    "\n"
    "exec gunicorn config.wsgi:application \\\n"
    "    --bind 0.0.0.0:$PORT \\\n"
    "    --workers 2 \\\n"
    "    --worker-class gthread \\\n"
    "    --threads 2 \\\n"
    "    --timeout 120 \\\n"
    "    --max-requests 1000 \\\n"
    "    --max-requests-jitter 50 \\\n"
    "    --access-logfile - \\\n"
    "    --error-logfile -\n"
)

with open(start_sh_path, "w", newline="\n") as f:
    f.write(content)

print(f"Created {start_sh_path} with LF line endings")
