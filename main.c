/*
 * Copyright (C) 2023 Zhaolan Huang <zhaolan.huang@fu-berlin.de>
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v3. See the file LICENSE in the top level
 * directory for more details.
 */

/**
 * @ingroup     apps
 * @{
 *
 * @file
 * @brief       U-TOE Application
 *
 * @author      Zhaolan Huang <zhaolan.huang@fu-berlin.de>
 *
 * @}
 */

#include <stdio.h>
#include <string.h>
#include "xtimer.h"
#include "random.h"
#include <tvm/runtime/crt/microtvm_rpc_server.h>
#include <tvm/runtime/crt/logging.h>
#include "stdio_base.h"

#ifndef UTOE_RANDOM_SEED
#define UTOE_RANDOM_SEED 42
#endif

#ifndef UTOE_TRIAL_NUM
#define UTOE_TRIAL_NUM 10
#endif

/* UTOE_GRANULARITY 0 - Per Model, 1 - Per Operator*/
#ifndef UTOE_GRANULARITY
#define UTOE_GRANULARITY 0
#endif

#define UTOE_RPC_BUFFER_SIZE 128

#ifndef UTOE_INPUT_SIZE
#define UTOE_INPUT_SIZE 4
#endif

#ifndef UTOE_OUTPUT_SIZE
#define UTOE_OUTPUT_SIZE 4
#endif

// Called by TVM to write serial data to the UART.
ssize_t write_serial(void* unused_context, const uint8_t* data, size_t size) {
    (void) unused_context;
    stdio_write(data, size);
    return size;
}

#if (UTOE_GRANULARITY==0)
#include <tvmgen_default.h>

void per_model_eval(void)
{       
    #include "model_io_vars.h"
    (void) printf("U-TOE Per-Model Evaluation \n");
    (void) printf("Press any key to start >\n");
    (void) getchar();

    random_init(UTOE_RANDOM_SEED);
    uint32_t start, end;

    for(int i = 0; i < UTOE_TRIAL_NUM;i++) {
        
        random_bytes(&input, sizeof(input));
        start =  xtimer_now_usec();
        int ret_val = tvmgen_default_run(&default_inputs, &default_outputs);
        end =  xtimer_now_usec();
        printf("trial: %d, usec: %ld, ret: %d \n", i, (long int)(end - start), ret_val);
    }
    (void) printf("Evaluation finished >\n");
}
#endif

#if (UTOE_GRANULARITY==1)
microtvm_rpc_server_t server;
void per_ops_eval(void)
{
    uint8_t buffer[UTOE_RPC_BUFFER_SIZE];
    random_init(UTOE_RANDOM_SEED);
    server = MicroTVMRpcServerInit(write_serial, NULL);
    TVMLogf("U-TOE Per-Operator Evaluation");
    TVMLogf("microTVM RIOT runtime - running");
    
    for(;;) {
        size_t bytes_read = stdio_read(buffer, UTOE_RPC_BUFFER_SIZE);
        uint8_t* arr_ptr = buffer;
        while (bytes_read > 0) {
            // Pass the received bytes to the RPC server.
            tvm_crt_error_t err = MicroTVMRpcServerLoop(server, &arr_ptr, &bytes_read);
            if (err != kTvmErrorNoError && err != kTvmErrorFramingShortPacket) {
                TVMPlatformAbort(err);
            }

        }
    }
}
#endif

#ifdef USE_SUIT
extern int suit_init(void);
#endif

int main(void)
{
    xtimer_init();

#ifdef USE_SUIT
    suit_init();
#endif

#if (UTOE_GRANULARITY==1)
    per_ops_eval();
#elif (UTOE_GRANULARITY==0)
    per_model_eval();
#endif

    return 0;
}
