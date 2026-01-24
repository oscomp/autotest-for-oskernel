# Running oscomp test cases locally

This document helps you run your `oscomp` work locally. Please execute the following commands.

## 1. Clone the autotest repository

```bash
git clone https://github.com/oscomp/autotest-for-oskernel.git
```

## 2. Pull the docker image

```bash
sudo docker pull zhouzhouyi/os-contest:20260104
```

This docker image provides environment for OS build toolchain and qemu-systems.

## 3. Prepare auxiliary test data

The auxiliary test data is used for judging your work. You can choose any directory you like, which we call `$data` in the following script.

```bash
# Create the directory.
mkdir $data

# Copy the judge scripts there.
cd autotest-for-oskernel
cp -rf kernel/judge/* $data

# Download the SD card images.
cd $data
wget https://github.com/oscomp/testsuits-for-oskernel/releases/download/pre-20250615/sdcard-la.img.xz
wget https://github.com/oscomp/testsuits-for-oskernel/releases/download/pre-20250615/sdcard-rv.img.xz

# It is possible to omit the `gzip` in order to save time,
# provided you modify the testing scripts locally.
unxz sdcard-la.img.xz
gzip sdcard-la.img
unxz sdcard-rv.img.xz
gzip sdcard-rv.img
```

## 4. Prepare auxiliary python kernel for judge

Note this "kernel" is not the operating system kernel.

```bash
cd autotest-for-oskernel/kernel
zip ../kernel.zip -r *
```

## 5. Evaluate your work

We assume you already have your work locally. We refer to its folder as `$os` in the following script.

Navigate to the parent folder of this repository, and run:

```bash
sudo docker run --rm \
-v $os:/coursegrader/submit \
-v $data:/coursegrader/testdata \
-v autotest-for-oskernel:/cg \
-v $data:/mnt/cghook/ \
docker.educg.net/cg/os-contest:20250714 python3 /cg/kernel.zip
```

The docker will build your OS, evaluate it, and output the result on the console.

To stop it, use `docker stop`, rather than force-exiting the python script. The latter method will leave the files in a locked state, and unlocking might require a reboot.
