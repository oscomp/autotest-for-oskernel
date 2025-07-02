KERNEL_NAME := cg/os_k210_autotest
VERSION := v0.0.1

DOCKER := kendryte-tool-chain:4.1

build:
	-rm kernel.zip
	cd kernel && zip ../kernel.zip -r *
#	-del kernel.zip
#	Bandizip.exe bc -aoa -o:. .\kernel\

docker_build: build
	docker image build --force-rm -t $(KERNEL_NAME):$(VERSION) .

img: docker_build
	docker save $(DOCKER) | pigz -c > $(subst /,-, $(KERNEL_NAME))_$(VERSION).tar.gz

test: build
	python test.py $(DOCKER)

run_docker:
	docker run --rm -e SERVER_IP=1 -e SERVER_PSW=2 -e SERVER_DEV=3 -v D:\codes\os-contest-2022\xv6-k210\:/coursegrader/submit -v D:\codes\os-contest-2022\testdata\:/coursegrader/testdata -v D:\codes\os-contest-2022\os_k210_autotest\kernel.zip:/cg/kernel.zip os-contest:v6.3 python3 /cg/kernel.zip

test_unmatch:
	ssh -p 200 root@tobyhome.oicp.net rm -f /cg/$(DEV)/*.txt
	scp -P 200 ssh_run_unmatched.py root@tobyhome.oicp.net:/cg/$(DEV)/
	ssh -p 200 root@tobyhome.oicp.net python /cg/$(DEV)/ssh_run_unmatched.py $(DEV)
	ssh -p 200 root@tobyhome.oicp.net cat /cg/$(DEV)/os_serial_out.txt

local_test:
	scp ssh_run_2023.py wmj@192.168.0.102:~/2023

FORCE: ;
