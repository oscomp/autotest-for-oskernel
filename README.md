# How to run oscomp locally
This document is to guide you to run your oscomp work locally

## 1 clone the autotest repository
git clone https://github.com/oscomp/autotest-for-oskernel.git

## 2 pull the docker image
sudo docker pull docker.educg.net/cg/os-contest:20250627

This docker image provides enviroment for OS build tool chain and qemu-systems


## 3 prepare the supporting testdata
The supporting testdata is used for make judge on your work

### create the directory
mkdir ~/Program/testdata (This can be arbitray diretory)

### cp the judge scripts to testdata
cd autotest-for-oskernel

cp -fr kernel/judge/* ~/Program/testdata

### download the sd-card images

cd ~/Program/testdata

Download  https://github.com/oscomp/testsuits-for-oskernel/releases/download/pre-20250615/sdcard-la.img.xz

Download  https://github.com/oscomp/testsuits-for-oskernel/releases/download/pre-20250615/sdcard-rv.img.xz

unxz sdcard-la.img.xz

gzip sdcard-la.img

unxz sdcard-rv.img.xz

gzip sdcard-rv.img

## 4 preparing supporting python kernel for judge
cd autotest-for-oskernel

cd kernel

zip ../kernel.zip -r *

## 5 clone your work
cd ~/Program/HIT (can be any directory)
git clone https://gitlab.eduxiji.net/T202510213995926/oskernel2025-rocketos.git

## 6 Run the evaluation process
sudo docker run --rm -v ~/Program/EDUCG/HIT/oskernel2025-rocketos/:/coursegrader/submit  -v ~/Program/testdata:/coursegrader/testdata -v ~/autotest-for-oskernel:/cg -v ~/Program/testdata:/mnt/cghook/ docker.educg.net/cg/os-contest:20250627 python3 /cg/kernel.zip

after building your OS, and the evluate your OS output, above command will output the result on the console.




