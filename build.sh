pyinstaller --noconfirm --onefile --console --add-data "/home/xff/PycharmProjects/pythonProject/hostile.png:." --add-data "/home/xff/PycharmProjects/pythonProject/mcapi.py:."  "/home/xff/PycharmProjects/pythonProject/main.py"

rm -rf package/bin
mkdir package/bin
mv dist/main package/bin/mobs


cd package
tar -czvf mobs.tar.gz ./*
cd ..

mv package/*.tar.gz .

