@echo off
echo Mengonfigurasi nama dan email Git...
git config --global user.name "Seksi Pajak Automation"
git config --global user.email "dev@automasi-pajak.local"

echo Menginisialisasi repositori...
git init
git add .

echo Menulis struktur awal (Initial Commit)...
git commit -m "🚀 Initial release: Pajak Editor & Merge Tools (CustomTkinter GUI)"

echo Menyambungkan dengan remote Github...
git branch -M main
git remote add origin https://github.com/edpspimdih2l-prog/Automasi-Data-Pajak-PSIAP.git

echo Meng-upload mahakarya ke GitHub...
git push -u origin main

echo Selesai!
