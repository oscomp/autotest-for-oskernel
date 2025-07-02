old_dir = old-kernel

build:
	rm -f kernel.zip
	mkdir -p ${old_dir}

	cd kernel && zip -0 -r ../kernel.zip *
	cp kernel.zip ${old_dir}/kernel-`date +%Y-%m-%d-%H-%M-%S`.zip
