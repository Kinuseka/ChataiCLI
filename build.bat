@echo off
python -m venv .venv
set FileName=ChataiV1.exe

call .venv\Scripts\activate
where pip
where python

pip install -r requirements.txt
python -OO -m PyInstaller --noconfirm build.spec
pause