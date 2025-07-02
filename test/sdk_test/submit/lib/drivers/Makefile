OBJS = aes.o \
	   fpioa.o \
	   i2c.o \
	   timer.o \
	   plic.o \
	   dmac.o \
	   gpiohs.o \
	   uart.o \
	   fft.o \
	   kpu.o \
	   gpio.o \
	   pwm.o \
	   uarths.o \
	   wdt.o \
	   rtc.o \
	   i2s.o \
	   sysctl.o \
	   sha256.o \
	   dvp.o \
	   iomem.o \
	   spi.o \
	   apu.o \
	   utils.o \
	   clint.o
	   
drivers.o: $(OBJS)
	$(LD) -relocatable $^ -o $@

build: drivers.o

clean:
	-rm drivers.o
	-rm $(OBJS)