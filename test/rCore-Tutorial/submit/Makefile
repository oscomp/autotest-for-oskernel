k210:
	@make -C os run

clean:
	@make -C user clean
	@make -C os clean
	rm target/k210.bin

fmt:
	@cd os && cargo fmt
	@cd os/src/algorithm && cargo fmt
	@cd user && cargo fmt
