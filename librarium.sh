rm -rf Documents_Recuperes/*
rm -rf /mnt/c/Users/louis/Downloads/Doc_admin/*

python3 main.py

if [ "$(ls -A Documents_Recuperes)" ]; then
	cp Documents_Recuperes/* /mnt/c/Users/louis/Bureau/Doc_admin
fi

cp -r Documents_Administratifs /mnt/c/Users/louis/Documents/

