#!/bin/env python

import sys
import argparse
import subprocess

# icinga returncode vars
EXIT_OK         = 0
EXIT_WARNING    = 1
EXIT_CRITICAL   = 2
EXIT_UNKNOWN    = 3

def thresholds(stats, metric, warning, critical):
    message = ' - %s is %s|%s=%s;%s;%s' %(metric, int(stats[metric]), metric, int(stats[metric]), warning, critical)
    if int(stats[metric]) > critical:
        critical_exit(message)
    if int(stats[metric]) > warning:
        warning_exit(message)
    ok_exit(message)

def fetch_stats(dcliArgs):
    rdsinfoOutput = subprocess.Popen(rdsinfoArgs, stdout=subprocess.PIPE, shell=True).communicate()[0]
    if len(rdsinfoOutput):
        return rdsinfoOutput

def parse_stats(commandOutput, stats):
    for line in commandOutput.splitlines():
        try:
            name, value = line.split()
        except:
            continue
        if stats.has_key(name):
            length = value.find('/')
            if length < 0:
                length = value.find(' ')
            if length < 0:
                length = value.find('%')
            if length < 0:
                length = None
            stats[name] = value[0:length]
    return stats

### stats define

stats = {
    'conn_reset': 0,
    'recv_drop_bad_checksum': 0,
    'recv_drop_old_seq': 0,
    'recv_drop_no_sock': 0,
    'recv_drop_dead_sock': 0,
    'recv_deliver_raced': 0,
    'recv_delivered': 0,
    'recv_queued': 0,
    'recv_immediate_retry': 0,
    'recv_delayed_retry': 0,
    'recv_ack_required': 0,
    'recv_rdma_bytes': 0,
    'recv_ping': 0,
    'send_queue_empty': 0,
    'send_queue_full': 0,
    'send_lock_contention': 0,
    'send_lock_queue_raced': 0,
    'send_immediate_retry': 0,
    'send_delayed_retry': 0,
    'send_drop_acked': 0,
    'send_ack_required': 0,
    'send_queued': 0,
    'send_rdma': 0,
    'send_rdma_bytes': 0,
    'send_pong': 0,
    'page_remainder_hit': 0,
    'page_remainder_miss': 0,
    'copy_to_user': 0,
    'copy_from_user': 0,
    'cong_update_queued': 0,
    'cong_update_received': 0,
    'cong_send_error': 0,
    'cong_send_blocked': 0,
    'qos_threshold_exceeded': 0,
    'ib_connect_raced': 0,
    'ib_listen_closed_stale': 0,
    'ib_evt_handler_call': 0,
    'ib_tasklet_call': 0,
    'ib_tx_cq_event': 0,
    'ib_tx_ring_full': 0,
    'ib_tx_throttle': 0,
    'ib_tx_sg_mapping_failure': 0,
    'ib_tx_stalled': 0,
    'ib_tx_credit_updates': 0,
    'ib_rx_cq_event': 0,
    'ib_rx_ring_empty': 0,
    'ib_rx_refill_from_cq': 0,
    'ib_rx_refill_from_thread': 0,
    'ib_rx_alloc_limit': 0,
    'ib_rx_total_frags': 0,
    'ib_rx_total_incs': 0,
    'ib_rx_credit_updates': 0,
    'ib_ack_sent': 0,
    'ib_ack_send_failure': 0,
    'ib_ack_send_delayed': 0,
    'ib_ack_send_piggybacked': 0,
    'ib_ack_received': 0,
    'ib_rdma_mr_alloc': 0,
    'ib_rdma_mr_free': 0,
    'ib_rdma_mr_used': 0,
    'ib_rdma_mr_pool_flush': 0,
    'ib_rdma_mr_pool_wait': 0,
    'ib_rdma_mr_pool_depleted': 0,
    'ib_srq_lows': 0,
    'ib_srq_refills': 0,
    'ib_srq_empty_refills': 0
}

# icinga returncode functions
def critical_exit(message):
    print 'CRITICAL' + message
    sys.exit(EXIT_CRITICAL)

def warning_exit(message):
    print 'WARNING' + message
    sys.exit(EXIT_WARNING)

def ok_exit(message):
    print 'OK' + message
    sys.exit(EXIT_OK)

def unknown_exit():
    sys.exit(EXIT_UNKNOWN)

if __name__ == '__main__':
    # request parameters for script
    parser = argparse.ArgumentParser('Icinga check for rds-info')
    parser.add_argument('--rdsinfo', default='/usr/bin/rds-info', help='path to rds-info. /usr/bin/rdsinfo')
    parser.add_argument('--metric', required=True, help='metric you want to check e.g: send_queue_full or  ib_tx_ring_full')
    parser.add_argument('--warning', required=True, type=int, help='warning threshold')
    parser.add_argument('--critical', required=True, type=int, help='critical threshold')
    args = parser.parse_args()
    # main program
    rdsinfoArgs = str(args.rdsinfo) + " -Icn"
    rdsinfoStats = fetch_stats(rdsinfoArgs)
    stats = parse_stats(rdsinfoStats, stats)
    thresholds(stats, args.metric, args.warning, args.critical)
