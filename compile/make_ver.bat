@echo off

set git="C:\Program Files\Git\bin\git.exe"
set bat="..\general\version.py"

set d=%date:/=%
set t=%time: =0%
set t=%t:~0,5%
set t=%t::=%
rem echo version_str = "%d%.%t%">%bat%

%git% show --format="version_str=\"%%cd @%%h\"" --date=format:%%Y%%m%%d.%%H%%M -s>%bat%
