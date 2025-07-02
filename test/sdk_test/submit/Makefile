INC_DIR:= $(CURDIR)/lib/bsp/include \
		  $(CURDIR)/lib/drivers/include \
		  $(CURDIR)/lib/utils/include \
		  $(CURDIR)/third_party/xtl/include \
		  $(CURDIR)/lib/nncase/include \
		  $(CURDIR)/test/include

INCFLAGS := $(addprefix -I, $(INC_DIR))

C_CPP_FLAGS:= -mcmodel=medany \
			  -mabi=lp64f \
			  -march=rv64imafc \
			  -fno-common \
			  -ffunction-sections \
			  -fdata-sections \
			  -fstrict-volatile-bitfields \
			  -fno-zero-initialized-in-bss \
			  -ffast-math \
			  -fno-math-errno \
			  -fsingle-precision-constant \
			  -Os \
			  -ggdb \
			  -Wall \
			  -Werror=all \
			  -Wno-error=unused-function \
			  -Wno-error=unused-but-set-variable \
			  -Wno-error=unused-variable \
			  -Wno-error=deprecated-declarations \
			  -Wno-multichar \
			  -Wextra \
			  -Werror=frame-larger-than=32768 \
			  -Wno-unused-parameter \
			  -Wno-sign-compare \
			  -Wno-error=missing-braces \
			  -Wno-error=return-type \
			  -Wno-error=pointer-sign \
			  -Wno-missing-braces \
			  -Wno-strict-aliasing \
			  -Wno-implicit-fallthrough \
			  -Wno-missing-field-initializers \
			  -Wno-int-to-pointer-cast \
			  -Wno-error=comment \
			  -Wno-error=logical-not-parentheses \
			  -Wno-error=duplicate-decl-specifier \
			  -Wno-error=parentheses

LINKFLAGS:= -nostartfiles \
        -static \
        -Wl,--gc-sections \
        -Wl,-static \
        -Wl,--start-group \
        -Wl,--whole-archive \
        -Wl,--no-whole-archive \
        -Wl,--end-group \
        -Wl,-EL \
        -Wl,--no-relax \
        -T $(CURDIR)/lds/kendryte.ld \


DEF := TCB_SPAN_NO_EXCEPTIONS \
	  TCB_SPAN_NO_CONTRACT_CHECKING \
	  NNCASE_TARGET=k210 \
	  KENDRYTE_SDK_TYPE=1 \
	  KENDRYTE_SDK_TYPE_STANDALONE=1 \
	  KENDRYTE_SDK_TYPE_FREERTOS=2 \
	  KENDRYTE_SDK_RELEASE_DATE=0 \
	  CONFIG_LOG_LEVEL=LOG_VERBOSE \
	  CONFIG_LOG_ENABLE \
	  CONFIG_LOG_COLORS \
	  LOG_KERNEL \
	  __riscv64 \
	  LV_CONF_INCLUDE_SIMPLE

DEFFLAGS := $(addprefix -D, $(DEF))

CFLAGS:= -std=gnu11 \
		 -Wno-pointer-to-int-cast \
		 -Wno-old-style-declaration \
		 $(C_CPP_FLAGS) $(INCFLAGS) $(DEFFLAGS)


CXXFLAGS:= -std=gnu++17 $(C_CPP_FLAGS) $(INCFLAGS) $(DEFFLAGS)
	  
LINK_ARG_PREFIX:= -Wl,--whole-archive
LINK_ARG_SUFFIX:= -Wl,--no-whole-archive


ARCH:= riscv64-unknown
CC      :=  $(ARCH)-elf-gcc
CXX     :=  $(ARCH)-elf-g++
AR      :=  $(ARCH)-elf-ar
OBJCOPY :=  $(ARCH)-elf-objcopy
LD      :=  $(ARCH)-elf-ld
NM      :=  $(ARCH)-elf-nm
RANLIB  :=  $(ARCH)-elf-ranlib

export CC CXX AR OBJCOPY LD NM DEFFLAGS CXXFLAGS CFLAGS RANLIB

CRT0_OBJ := $(shell $(CC) -print-file-name=crt0.o )
CRTBEGIN_OBJ := $(shell $(CC) -print-file-name=crtbegin.o)
CRTEND_OBJ := $(shell $(CC) -print-file-name=crtend.o)
CRTI_OBJ := $(shell $(CC) -print-file-name=crti.o)
CRTN_OBJ := $(shell $(CC) -print-file-name=crtn.o)

all: build

build: FORCE
	$(MAKE) -C lib build
	$(MAKE) -C src build
	$(MAKE) -C test build
	mkdir -p target
	$(CC) $(CFLAGS) $(LINKFLAGS) "$(CRTI_OBJ)" "$(CRTBEGIN_OBJ)" src/src.o test/testdir.o "$(CRTEND_OBJ)" "$(CRTN_OBJ)" -o target/k210_kernel -Wl,--start-group -lgcc -lm -lc -Wl,--whole-archive lib/libkendryte.a -Wl,--no-whole-archive -Wl,--end-group lib/libnncase.a -lstdc++ -lm 
	$(OBJCOPY) --output-format=binary target/k210_kernel target/k210.bin

clean: 
	$(MAKE) -C lib clean
	$(MAKE) -C src clean
	$(MAKE) -C test clean
	-rm -r target

FORCE:
