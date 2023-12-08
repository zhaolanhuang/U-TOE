#model control interface
# INCLUDES += -I$(CURDIR)/include
PARAMS_PERSISTENT_ON_FLASH ?= 0

ifeq ($(PARAMS_PERSISTENT_ON_FLASH), 1)

CFLAGS += -DCONFIG_PARAMS_PERSISTENT_ON_FLASH
USEMODULE += mtd
USEMODULE += mtd_flashpage
USEMODULE += mtd_write_page

endif

include $(RIOTBASE)/Makefile.base