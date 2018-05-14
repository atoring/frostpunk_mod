@echo off

set pyi="C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\Scripts\pyinstaller.exe"

call make_ver.bat

for %%f in (..\dat\*.py) do %pyi% --onefile %%f
copy dist\*.exe ..\dat
rd /S /Q ..\dat\__pycache__
rd /S /Q build
rd /S /Q dist
del /Q *.spec

for %%f in (..\binfont\*.py) do %pyi% --onefile %%f
copy dist\*.exe ..\binfont
rd /S /Q ..\binfont\__pycache__
rd /S /Q build
rd /S /Q dist
del /Q *.spec

for %%f in (..\lang\*.py) do %pyi% --onefile %%f
copy dist\*.exe ..\lang
rd /S /Q ..\lang\__pycache__
rd /S /Q build
rd /S /Q dist
del /Q *.spec

for %%f in (..\general\*.py) do %pyi% --onefile --windowed %%f
copy dist\*.exe ..\general
rd /S /Q ..\general\__pycache__
rd /S /Q build
rd /S /Q dist
del /Q *.spec

del /Q ..\general\version.exe
