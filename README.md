initializing database .venv format modifier 

python -m venv .venv

type this into the terminal with .venv format(should have the schema.swl file within the directory)

Get-Content schema.sql | & "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p