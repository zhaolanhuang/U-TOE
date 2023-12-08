/*
 * Copyright (c) 2023 Zhaolan Huang
 * 
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v3.0. See the file LICENSE in the top level
 * directory for more details.
 */
#include "net/nanocoap_sock.h"

#define MAIN_QUEUE_SIZE     (8)
static msg_t _main_msg_queue[MAIN_QUEUE_SIZE];

void coap_server_init(void) {
    msg_init_queue(_main_msg_queue, MAIN_QUEUE_SIZE);

    sock_udp_ep_t local = {
        .port = COAP_PORT,
        .family = AF_INET6,
    };

    nanocoap_server_start(&local);
}