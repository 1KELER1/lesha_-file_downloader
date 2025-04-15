@echo off
echo Назначение роли EDITOR пользователю...
python manage.py shell -c "exec(open('set_editor_script.py').read())"
echo.
echo Готово!
pause 