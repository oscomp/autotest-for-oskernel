build: src.o

src.o: main.o
	$(LD) -relocatable $^ -o $@

clean: 
	-rm *.o