import os
import sys
import threading
import socket
import time
from pathlib import Path


def find_free_port():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    addr, port = s.getsockname()
    s.close()
    return port


def start_server(port):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    import django
    django.setup()
    from django.core.wsgi import get_wsgi_application
    from django.contrib.staticfiles.handlers import StaticFilesHandler
    from waitress import serve

    app = get_wsgi_application()
    # Wrap with StaticFilesHandler so static files are served in DEBUG mode
    app = StaticFilesHandler(app)
    serve(app, host='127.0.0.1', port=port)


def wait_for_server(url, timeout=10.0):
    import urllib.request
    start = time.time()
    while True:
        try:
            with urllib.request.urlopen(url, timeout=1):
                return True
        except Exception:
            if time.time() - start > timeout:
                return False
            time.sleep(0.2)


def main():
    port = find_free_port()
    t = threading.Thread(target=start_server, args=(port,), daemon=True)
    t.start()

    url = f'http://127.0.0.1:{port}/'
    if not wait_for_server(url, timeout=15.0):
        print('Server did not start in time.', file=sys.stderr)
        sys.exit(1)

    try:
        import webview
    except Exception as exc:
        print('pywebview is required to run the desktop app.\nInstall with: python -m pip install pywebview', file=sys.stderr)
        raise

    window = webview.create_window('Django Desktop App', url)
    webview.start()

    # ensure process exits (server thread is daemon)
    os._exit(0)


if __name__ == '__main__':
    main()
