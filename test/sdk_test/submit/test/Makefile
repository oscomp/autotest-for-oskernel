build: testdir.o

testdir.o: test.o test1.o test2.o test3.o
	$(LD) -relocatable $^ -o $@

clean: 
	-rm *.o