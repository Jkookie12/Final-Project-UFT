# Building the Desktop Executable

This guide walks through creating a standalone Windows executable for the
Django-based blog application using the `desktop.py` launcher script and
[PyInstaller].

## Prerequisites

1. A working Python 3.11 virtual environment in the project root (see
   `requirements.txt`).
2. All dependencies installed:
   ```powershell
   .env\Scripts\python -m pip install -r requirements.txt
   ```
3. `pyinstaller` installed in the same environment:
   ```powershell
   .env\Scripts\python -m pip install pyinstaller
   ```

## The Launcher

`desktop.py` starts a local Waitress WSGI server bound to `127.0.0.1` on a
free port and then opens that URL inside a native window using `pywebview`.

The script is written to be importable by PyInstaller and to exit cleanly
when the window closes.

## Adjusting Settings for Frozen Executable

`myproject/settings.py` contains logic to set `BASE_DIR` based on whether the
app is running as a frozen executable.  PyInstaller extracts files to a
temporary folder referred to by `sys._MEIPASS`, so the code looks like:

```python
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
```

This ensures that template and static file lookups continue to function after
packaging.

## Packaging Command

Run the following from the project root while the virtual environment is
activated (or use the full path to `.env\Scripts\python.exe`):

```powershell
.env\Scripts\python -m PyInstaller \
    --onefile \
    --add-data "blogpost/templates;blogpost/templates" \
    --add-data "members/templates;members/templates" \
    --add-data "static;static" \
    desktop.py
```

Explanation of flags:

- `--onefile` generates a single `.exe` instead of a folder.
- `--add-data` copies specified directories into the bundle.  Use
  `SOURCE;DEST` syntax on Windows; the `DEST` path is relative to `sys._MEIPASS`.

Any additional directories (e.g. if you add more apps with templates) should be
listed similarly.

## Output

PyInstaller will create `build/` and `dist/` directories.  The resulting
`dist\desktop.exe` is the standalone desktop application.  Run it with:

```powershell
.\dist\desktop.exe
```

When executed, the app will display the blog's web UI in a native window.  It
can be freely copied to other Windows machines; no Python installation is
required on the target system.

## Troubleshooting

- **`TemplateDoesNotExist` errors after packaging** – ensure `BASE_DIR` logic is
  present in settings and that you included all template directories via
  `--add-data`.
- **Missing static files** – add `static;static` to `--add-data` (already
  included above) and verify `STATICFILES_DIRS` points to `static`.
- **`pywebview` or `waitress` not found** – double-check they are in
  `requirements.txt` and installed in the environment.

[PyInstaller]: https://www.pyinstaller.org/
