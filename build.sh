mkdir build
cd ./src/vizdoom/gdtoa && cmake . && make
cd -
rm -rf ./bin
cd build && cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_PYTHON3=ON -DBUILD_JAVA=OFF ..
rm -f ../error.log && rm -f ../build.log && make -j12 #2> ../error.log > ../build.log
#ln -s ../vizdoom ../bin/python3/vizdoom
#ln -s ../freedoom2.wad ../bin/python3/freedoom2.wad
# echo "export PYTHONPATH=`pwd`/bin/python3/pip_package:$PYTHONPATH" >> /root/.bashrc
# export PYTHONPATH=`pwd`/../bin/python3/pip_package:$PYTHONPATH
#source /root/.bashrc
ln ../bin/vizdoom ../bin/python3/pip_package/vizdoom
