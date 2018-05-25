@echo off

set git="C:\Program Files\Git\bin\git.exe"
set py="..\frostpunk_mod\version.py"

%git% show --format="version_str=\"%%cd @%%h\"" --date=format:%%Y%%m%%d.%%H%%M -s>%py%
