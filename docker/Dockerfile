# FROM ubuntu:18.04 AS build_stage
# LABEL maintainer="w-mj <wmj@alphamj.cn>"

# RUN sed -i s@/archive.ubuntu.com/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list && apt update
# RUN apt install -y --no-install-recommends git ca-certificates && update-ca-certificates
# RUN git clone --recursive https://github.com/kendryte/kendryte-gnu-toolchain
# RUN apt install -y --no-install-recommends \
#     autoconf automake autotools-dev curl libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev
# RUN cd kendryte-gnu-toolchain && ./configure --prefix=/opt/kendryte-toolchain --with-cmodel=medany --with-arch=rv64imafc --with-abi=lp64f && make -j8

# FROM ubuntu:20.04
FROM docker.educg.net/cg/code-server:4.10.0-ubuntu-1
# COPY --from=build_stage /opt/kendryte-toolchain/ /opt/kendryte-toolchain/
ENV PATH "$PATH:/opt/kendryte-toolchain/bin:/root/.cargo/bin"

USER root
RUN sed -i s@/archive.ubuntu.com/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list && apt update
RUN apt install -y --no-install-recommends git ca-certificates && update-ca-certificates
RUN apt install -y --no-install-recommends python3 python3-pip make curl sshpass openssh-client
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Aisa/Shanghai
RUN apt update && apt install -y --no-install-recommends gcc libc-dev
RUN apt-get install -y git build-essential gdb-multiarch gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu libpixman-1-0 git

RUN pip install pytz Cython jwt jinja2 requests

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y
RUN echo 'source $HOME/.cargo/env' >> $HOME/.bashrc
RUN mkdir -p $HOME/.cargo/ && echo "[source.crates-io]\nregistry = \"https://github.com/rust-lang/crates.io-index\"\nreplace-with = 'ustc'\n[source.ustc]\nregistry = \"git://mirrors.ustc.edu.cn/crates.io-index\"" >> $HOME/.cargo/config
RUN export PATH="$PATH:/root/.cargo/bin"

#RUN rustup install nightly-2020-06-27
#RUN rustup install nightly-2021-05-24
#RUN rustup install nightly-2022-04-11
RUN rustup install nightly-2023-03-27
RUN rustup default nightly-2023-03-27
RUN rustup component add llvm-tools-preview
RUN rustup target add riscv64imac-unknown-none-elf
RUN rustup target add riscv64gc-unknown-none-elf

#RUN rustup target add riscv64imac-unknown-none-elf --toolchain nightly-2021-05-24
#RUN rustup target add riscv64gc-unknown-none-elf --toolchain nightly-2021-05-24
#RUN rustup target add riscv64imac-unknown-none-elf --toolchain nightly-2020-06-27
#RUN rustup target add riscv64gc-unknown-none-elf --toolchain nightly-2020-06-27
#RUN rustup component add llvm-tools-preview --toolchain nightly-2021-05-24
#RUN rustup component add llvm-tools-preview --toolchain nightly-2020-06-27
#
#RUN rustup target add riscv64imac-unknown-none-elf --toolchain nightly-2022-04-11
#RUN rustup target add riscv64gc-unknown-none-elf --toolchain nightly-2022-04-11
#RUN rustup component add llvm-tools-preview --toolchain nightly-2022-04-11

RUN rustup target add riscv64imac-unknown-none-elf --toolchain nightly-2023-03-27
RUN rustup target add riscv64gc-unknown-none-elf --toolchain nightly-2023-03-27
RUN rustup component add llvm-tools-preview --toolchain nightly-2023-03-27

RUN cargo install cargo-binutils --version 0.3.6


COPY oscomp-dependencies-2023 /oscomp-dependencies-2023
#
ENV http_proxy "http://host.docker.internal:10809"
ENV https_proxy "http://host.docker.internal:10809"
#

RUN cd /oscomp-dependencies-2023 && cargo build
#
ENV http_proxy ""
ENV https_proxy ""


# https://github.com/riscv/riscv-gnu-toolchain
# COPY riscv /opt/riscv
# https://github.com/kendryte/kendryte-gnu-toolchain/releases/tag/v8.2.0-20190213
COPY kendryte-toolchain /opt/kendryte-toolchain

COPY qemu-prebuilt-7.0.0.tar.gz /qemu/qemu.tar.gz
RUN cd /qemu && tar xavf /qemu/qemu.tar.gz
ENV PATH /qemu/bin/:$PATH
ENV LD_LIBRARY_PATH /opt/kendryte-toolchain/bin/:$LD_LIBRARY_PATH

COPY riscv64--musl--bleeding-edge-2020.08-1.tar.bz2 /opt/
RUN cd /opt && tar jxvf /opt/riscv64--musl--bleeding-edge-2020.08-1.tar.bz2
ENV PATH $PATH:/opt/riscv64--musl--bleeding-edge-2020.08-1/bin

RUN rm /qemu/qemu.tar.gz && rm /opt/riscv64--musl--bleeding-edge-2020.08-1.tar.bz2

RUN apt-get install --no-install-recommends -y libguestfs-tools qemu-utils linux-image-generic

RUN apt-get install --no-install-recommends -y libncurses5-dev python

RUN apt-get install --no-install-recommends -y autotools-dev automake
ENV LIBGUESTFS_BACKEND=direct

RUN apt-get install -y musl-tools
RUN rm -rf /var/lib/apt/lists/*

ENTRYPOINT ""

# ENV LD_LIBRARY_PATH /opt/kendryte-toolchain/bin/

# RUN mkdir -p /kernel/
# RUN groupadd -r cguser && useradd --no-log-init -m -r -g cguser cguser

# USER cguser
