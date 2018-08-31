#!/usr/bin/env python
# junos device info
junos_host = '192.168.10.1'
host_netconf_port = '22'
host_user = 'lab'
host_pwd = 'lab.123'

# display script usage if args are omitted
import sys
script_name = sys.argv[0]
if len(sys.argv) == 1:
  print "Script usage:", script_name, "addr-set-name addr-prefix1 addr-prefix2 addr-prefix3 ..."
  exit()

# define variables for address-set and addresses
set_name = sys.argv[1]
set_cmd = ''
addr_cmd = ''

# iterate through address arguments and build set commands
for addr_prefix in sys.argv[+2:]:
  #print addr_prefix
  addr_cmd = addr_cmd + 'set security address-book global address ' + 'NET_' + addr_prefix + ' ' + addr_prefix + "\n"
  set_cmd = set_cmd + 'set security address-book global address-set ' + set_name + ' address NET_' + addr_prefix + '\n'
all_set_cmds = addr_cmd + set_cmd
print  "\nSET commands to be added:\n", all_set_cmds

# connect to junos device
print "Connecting to Junos device -", junos_host, ":", host_netconf_port
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
junos_device = Device(host=junos_host, port=host_netconf_port, user=host_user, password=host_pwd)
junos_device.open()

# load config module and execute set commands
cfg = Config(junos_device)
cfg.load(all_set_cmds, format="set")

# output 'show |compare'
print "Changes to commit:\n", cfg.diff()

# commit with comment
commit_comment = script_name + ' added address-set: ' + set_name
if cfg.diff():
  cfg.commit(comment=commit_comment)

# cleanup
junos_device.close
