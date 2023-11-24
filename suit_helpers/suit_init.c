/* Adopted from examples/suit_update/main.c of RIOT's repo */

#include <stdio.h>

#include "fmt.h"
#include "thread.h"
#include "irq.h"
#include "net/nanocoap_sock.h"

#include "shell.h"

#include "suit/transport/coap.h"
#ifdef MODULE_SUIT_STORAGE_FLASHWRITE
#include "riotboot/slot.h"
#endif

#include "suit/storage.h"
#include "suit/storage/ram.h"
#ifdef BOARD_NATIVE
#include "suit/storage/vfs.h"
#include "xfa.h"
#include "vfs_default.h"
#endif

#define COAP_INBUF_SIZE (256U)

/* Extend stacksize of nanocoap server thread */
static char _nanocoap_server_stack[THREAD_STACKSIZE_DEFAULT + THREAD_EXTRA_STACKSIZE_PRINTF];
#define NANOCOAP_SERVER_QUEUE_SIZE     (8)
static msg_t _nanocoap_server_msg_queue[NANOCOAP_SERVER_QUEUE_SIZE];

#define MAIN_QUEUE_SIZE     (8)
static msg_t _main_msg_queue[MAIN_QUEUE_SIZE];

/* add handled storages */
#if IS_USED(MODULE_SUIT_STORAGE_VFS)
XFA_USE(char*, suit_storage_files_reg);
#ifdef BOARD_NATIVE
XFA(suit_storage_files_reg, 0) char* _slot0 = VFS_DEFAULT_DATA "/SLOT0.txt";
XFA(suit_storage_files_reg, 1) char* _slot1 = VFS_DEFAULT_DATA "/SLOT1.txt";
#endif
#endif

#ifdef MODULE_SUIT_STORAGE_FLASHWRITE
static int cmd_print_riotboot_hdr(int argc, char **argv)
{
    (void)argc;
    (void)argv;

    int current_slot = riotboot_slot_current();
    if (current_slot != -1) {
        /* Sometimes, udhcp output messes up the following printfs.  That
         * confuses the test script. As a workaround, just disable interrupts
         * for a while.
         */
        unsigned state = irq_disable();
        riotboot_slot_print_hdr(current_slot);
        irq_restore(state);
    }
    else {
        printf("[FAILED] You're not running riotboot\n");
    }
    return 0;
}

static int cmd_print_current_slot(int argc, char **argv)
{
    (void)argc;
    (void)argv;
    /* Sometimes, udhcp output messes up the following printfs.  That
     * confuses the test script. As a workaround, just disable interrupts
     * for a while.
     */
    unsigned state = irq_disable();
    printf("Running from slot %d\n", riotboot_slot_current());
    irq_restore(state);
    return 0;
}
#endif

static void *_nanocoap_server_thread(void *arg)
{
    (void)arg;

    /* nanocoap_server uses gnrc sock which uses gnrc which needs a msg queue */
    msg_init_queue(_nanocoap_server_msg_queue, NANOCOAP_SERVER_QUEUE_SIZE);

    /* initialize nanocoap server instance */
    uint8_t buf[COAP_INBUF_SIZE];
    sock_udp_ep_t local = { .port=COAP_PORT, .family=AF_INET6 };
    nanocoap_server(&local, buf, sizeof(buf));

    return NULL;
}


int suit_init(void)
{
    puts("SUIT update init");

#ifdef MODULE_SUIT_STORAGE_FLASHWRITE
    cmd_print_current_slot(0, NULL);
    cmd_print_riotboot_hdr(0, NULL);
#endif
    /* initialize suit storage */
    suit_storage_init_all();

    /* start nanocoap server thread */
    thread_create(_nanocoap_server_stack, sizeof(_nanocoap_server_stack),
                  THREAD_PRIORITY_MAIN - 1,
                  THREAD_CREATE_STACKTEST,
                  _nanocoap_server_thread, NULL, "nanocoap server");

    /* the shell contains commands that receive packets via GNRC and thus
       needs a msg queue */
    msg_init_queue(_main_msg_queue, MAIN_QUEUE_SIZE);

    return 0;
}