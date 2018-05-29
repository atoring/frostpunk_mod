@echo off

set pyi="C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\Scripts\pyinstaller.exe"
set bin=frostpunk_mod

call make_ver.bat

cd ..\frostpunk_mod
rd /S /Q __pycache__
rd /S /Q build
rd /S /Q dist
del /Q *.spec

rem %pyi% --clean --onefile --name %bin% --windowed --uac-admin main.py
%pyi% --clean --onefile --name %bin% --windowed --manifest build\%bin%\%bin%.exe.manifest main.py
copy /Y dist\*.exe ..\compile

rd /S /Q __pycache__
rd /S /Q build
rd /S /Q dist
del /Q *.spec
cd ..\compile

call reset_ver.bat
