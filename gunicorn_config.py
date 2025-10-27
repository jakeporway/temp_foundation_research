"""Gunicorn configuration for production deployment"""

# Worker configuration
workers = 2
worker_class = 'sync'
timeout = 180  # 3 minutes for long-running chat queries
keepalive = 5

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Server mechanics
bind = '0.0.0.0:10000'  # Render uses port 10000 by default
