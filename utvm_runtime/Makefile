PKG_NAME ?= utvm_runtime
UTVM_NAME ?= $(PKG_NAME)
UTVM_RUNTIME_BUILD_DIR ?= $(BINDIR)/pkg-build/$(PKG_NAME)
UTVM_RUNTIME_SOURCE_DIR = $(CURDIR)
include $(RIOTBASE)/Makefile.base

UTOE_RT_CXXFLAGS = $(CXXFLAGS) -Wno-error # RIOT do not export CXXFLAGS, to align the settings in CMAKE

.PHONY: all prepare clean

all: prepare
	"$(MAKE)" -C $(UTVM_RUNTIME_BUILD_DIR)
	@cp $(UTVM_RUNTIME_BUILD_DIR)/libcommon.a $(BINDIR)/libcommon.a
	@cp $(UTVM_RUNTIME_BUILD_DIR)/libmemory.a $(BINDIR)/libmemory.a


	@cp $(UTVM_RUNTIME_BUILD_DIR)/libaot_executor_module.a $(BINDIR)/libaot_executor_module.a
	@cp $(UTVM_RUNTIME_BUILD_DIR)/libaot_executor.a $(BINDIR)/libaot_executor.a

	@cp $(UTVM_RUNTIME_BUILD_DIR)/libgraph_executor_module.a $(BINDIR)/libgraph_executor_module.a
	@cp $(UTVM_RUNTIME_BUILD_DIR)/libgraph_executor.a $(BINDIR)/libgraph_executor.a

	@cp $(UTVM_RUNTIME_BUILD_DIR)/libmicrotvm_rpc_common.a $(BINDIR)/libmicrotvm_rpc_common.a
	@cp $(UTVM_RUNTIME_BUILD_DIR)/libmicrotvm_rpc_server.a $(BINDIR)/libmicrotvm_rpc_server.a

prepare: $(UTVM_RUNTIME_BUILD_DIR)/Makefile

$(UTVM_RUNTIME_BUILD_DIR)/Makefile:
	mkdir -p $(UTVM_RUNTIME_BUILD_DIR)
	cmake -B$(UTVM_RUNTIME_BUILD_DIR) -H$(UTVM_RUNTIME_SOURCE_DIR) \
			-DCRT_CONFIG_PATH=$(UTVM_RUNTIME_SOURCE_DIR)/include/tvm/runtime/ \
			-DCMAKE_C_COMPILER_WORKS=TRUE \
			-DCMAKE_CXX_COMPILER_WORKS=TRUE \
			-DCMAKE_SYSTEM_NAME=RIOT \
			-DCMAKE_SYSTEM_PROCESSOR="$(MCPU)" \
			-DCMAKE_CXX_FLAGS="$(CFLAGS) -fno-exceptions -fno-rtti -Wno-error" \
			-DCMAKE_VERBOSE_MAKEFILE=0 \

clean::
	$(QQ)rm -Rf $(UTVM_RUNTIME_BUILD_DIR)
