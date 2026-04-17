@echo off
set CONDAPATH=%USERPROFILE%\anaconda3
call %CONDAPATH%\Scripts\activate.bat %CONDAPATH%
cd /d "%USERPROFILE%\Desktop\Monics"
streamlit run mon.py
pause