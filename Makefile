RIOTBASE= ./RIOT

BOARD ?= stm32f746g-disco
APPLICATION = U-TOE

# WERROR ?= 0

EXTERNAL_PKG_DIRS += models
USEPKG += default 
USEMODULE += xtimer random stdin

UTOE_RANDOM_SEED ?= 42
UTOE_TRIAL_NUM ?= 10
UTOE_GRANULARITY ?= 0

CFLAGS += -DUTOE_RANDOM_SEED=$(UTOE_RANDOM_SEED) -DUTOE_TRIAL_NUM=$(UTOE_TRIAL_NUM)
CFLAGS += -DUTOE_GRANULARITY=$(UTOE_GRANULARITY)


include $(RIOTBASE)/Makefile.include

CFLAGS += -Wno-strict-prototypes

IOTLAB_ARCHI_openmote-b = openmoteb

include iotlab.site.mk
include $(RIOTBASE)/dist/testbed-support/makefile.iotlab.archi.inc.mk
include $(RIOTBASE)/dist/testbed-support/Makefile.iotlab
override BINARY := $(ELFFILE)
