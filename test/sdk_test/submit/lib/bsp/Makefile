OBJS = locks.o \
	entry.o \
	sleep.o \
	syscalls.o \
	printf.o \
	interrupt.o \
	entry_user.o \
	crt.o

crt.o: crt.S
	$(CC) $(CFLAGS) -x assembler-with-cpp -c crt.S -o crt.o 

bsp.o: $(OBJS)
	$(LD) -relocatable $^ -o $@

build: bsp.o

clean:
	-rm *.o
