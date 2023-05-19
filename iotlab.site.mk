# board-site mapping
IOTLAB_SITE_arduino-zero   = saclay
IOTLAB_SITE_b-l072z-lrwan1 = saclay
IOTLAB_SITE_b-l475e-iot01a = saclay
IOTLAB_SITE_dwm1001        = lille
IOTLAB_SITE_firefly        = lille
IOTLAB_SITE_iotlab-a8-m3   = grenoble
IOTLAB_SITE_iotlab-m3      = grenoble
# IOTLAB_SITE_microbit       = microbit:ble # not support anymore
IOTLAB_SITE_nrf52dk        = saclay
IOTLAB_SITE_nrf52840dk     = saclay
IOTLAB_SITE_nucleo-wl55jc  = grenoble
IOTLAB_SITE_samr21-xpro    = saclay
IOTLAB_SITE_samr30-xpro    = saclay
IOTLAB_SITE_samr34-xpro    = grenoble
IOTLAB_SITE_zigduino       = strasbourg
IOTLAB_SITE_openmote-b       = strasbourg
IOTLAB_SITE ?= $(IOTLAB_SITE_$(BOARD))