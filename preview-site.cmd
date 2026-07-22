@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if not errorlevel 1 (
  py tools\serve_local.py 8000
  goto :finished
)

where python >nul 2>nul
if not errorlevel 1 (
  python tools\serve_local.py 8000
  goto :finished
)

echo Δεν βρέθηκε εγκατάσταση Python. Εγκαταστήστε Python 3 ή εκτελέστε το preview από το Codex.
pause
exit /b 1

:finished
set "previewExitCode=%errorlevel%"
if not "%previewExitCode%"=="0" pause
exit /b %previewExitCode%
