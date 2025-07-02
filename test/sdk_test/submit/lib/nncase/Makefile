SRC = nncase.cpp \
	  runtime/cpu/cpu_ops.cpp \
	  runtime/interpreter.cpp \
	  runtime/k210/interpreter.cpp \
	  runtime/k210/k210_ops.cpp \
	  runtime/kernel_registry.cpp \
	  runtime/neutral/neutral_ops.cpp

OBJ = $(addsuffix .o, $(basename $(SRC)))

nncase.o: $(OBJ)
	$(LD) -relocatable $^ -o $@

build: nncase.o

clean:
	-rm nncase.o
	-rm $(OBJ)