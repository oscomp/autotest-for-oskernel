OBJS = bsp/bsp.o drivers/drivers.o nncase/nncase.o

libkendryte.a: bsp/bsp.o drivers/drivers.o
	$(AR) qc libkendryte.a bsp/bsp.o drivers/drivers.o
	$(RANLIB) libkendryte.a

libnncase.a: nncase/nncase.o
	$(AR) qc libnncase.a nncase/nncase.o
	$(RANLIB) libnncase.a

$(OBJS):
	make -C $(notdir $(basename $@)) build

build: libkendryte.a libnncase.a


clean:
	make -C nncase clean
	make -C drivers clean
	make -C bsp clean
	-rm *.a