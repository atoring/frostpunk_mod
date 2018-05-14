@echo off

set bat="..\general\version.py"

set d=%date:/=%
set t=%time: =0%
set t=%t:~0,5%
set t=%t::=%

echo version_str = "%d%.%t%">%bat%
