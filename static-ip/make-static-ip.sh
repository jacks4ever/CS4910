#!/usr/bin/env bash
# make-static-ip.sh: give this Ubuntu 24.04 VM its static IPv4 address on VLAN 1020.
#
#   lastname-srv, lastname-tgt:  sudo bash make-static-ip.sh              get this VM's address from the course registry
#   any VM:                      sudo bash make-static-ip.sh --check      check only, change nothing
#   any VM:                      sudo bash make-static-ip.sh 10.5.103.x   use a specific address from the course block
#   undo:                        sudo bash make-static-ip.sh --dhcp       go back to DHCP
#
# Works from the VM console or over SSH. When it changes the address, it shows
# the new one to write down and reboots the VM one minute later. Running it
# again on a VM that already has its address changes nothing.
#
# Why: VLAN 1020 runs a live DHCP pool with 1-hour leases. The earlier version
# of this script turned the VM's DHCP address into a static one, but the
# address stayed in the pool, so within about an hour DHCP could lease it to
# another VM. Two VMs on one address means SSH and logins land on either
# machine at random ("my password works sometimes"). So static addresses now
# come only from the course block (10.5.103.x), which sits above the addresses
# DHCP is handing out, and the instructor's registry records which VM has each.
set -euo pipefail

COURSE_FIRST="10.5.103.1"     # course block for static addresses: all of 10.5.103.x
COURSE_LAST="10.5.103.254"
RESERVED="10.5.103.250"       # inside the block but never handed out (the registry VM)
REGISTRY="10.5.103.250:8080"   # instructor VM that records which VM has which address

[[ $EUID -eq 0 ]] || { echo "Run with sudo:  sudo bash $0 $*" >&2; exit 1; }
MODE=auto; WANT=""
case "${1:-}" in
  ""|--auto) ;;
  --check) MODE=check ;;
  --dhcp)  MODE=dhcp ;;
  -h|--help) sed -n '2,11p' "$0"; exit 0 ;;
  *)       MODE=static; WANT=$1 ;;
esac

ip2int() { local a b c d; IFS=. read -r a b c d <<<"$1"; echo $(( (a << 24) | (b << 16) | (c << 8) | d )); }
isip() { [[ "$1" =~ ^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$ ]] &&
         (( BASH_REMATCH[1] < 256 && BASH_REMATCH[2] < 256 && BASH_REMATCH[3] < 256 && BASH_REMATCH[4] < 256 )); }
inblock() {
  [[ -n "$COURSE_FIRST" && -n "$COURSE_LAST" ]] || return 1
  local n r; n=$(ip2int "$1")
  for r in $RESERVED; do [[ "$1" == "$r" ]] && return 1; done
  (( n >= $(ip2int "$COURSE_FIRST") && n <= $(ip2int "$COURSE_LAST") ))
}

ROUTE=$(ip -4 route show default | awk 'NR==1')
[[ -n "$ROUTE" ]] || { echo "No default route; cannot read network settings. Ask your instructor." >&2; exit 1; }
IFACE=$(awk '{for (i = 1; i <= NF; i++) if ($i == "dev") print $(i + 1)}' <<<"$ROUTE")
GW=$(awk '{for (i = 1; i <= NF; i++) if ($i == "via") print $(i + 1)}' <<<"$ROUTE")
CIDR=$(ip -4 -o addr show dev "$IFACE" scope global | awk 'NR==1 {print $4}')
[[ -n "$GW" && -n "$CIDR" ]] || { echo "Could not read network settings. Ask your instructor." >&2; exit 1; }
MAC=$(cat "/sys/class/net/$IFACE/address")
CUR=${CIDR%/*}; PREFIX=${CIDR#*/}
if grep -qsE '^\s*dhcp4:\s*(true|yes)' /etc/netplan/*.yaml /etc/netplan/*.yml; then ADDRMODE=dhcp; else ADDRMODE=static; fi

# ARP probe (RFC 5227): sender IP 0.0.0.0, so it works for this VM's own
# address. Prints the other machine's MAC and returns 0 if anyone else answers.
probe() {
  python3 - "$IFACE" "$1" "$MAC" "${2:-2}" <<'PY'
import socket, struct, sys, time
iface, ip, mymac, wait = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
mac, tip = bytes.fromhex(mymac.replace(':', '')), socket.inet_aton(ip)
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0806))
s.bind((iface, 0)); s.settimeout(0.1)
pkt = (b'\xff' * 6 + mac + b'\x08\x06' + struct.pack('!HHBBH', 1, 0x0800, 6, 4, 1)
       + mac + b'\x00' * 4 + b'\x00' * 6 + tip).ljust(60, b'\x00')
end, nxt = time.time() + wait, 0
while time.time() < end:
    if time.time() >= nxt:
        s.send(pkt); nxt = time.time() + wait / 3
    try:
        f = s.recv(64)
    except socket.timeout:
        continue
    if len(f) >= 42 and f[22:28] != mac and f[28:32] == tip:
        print(':'.join('%02x' % b for b in f[22:28])); sys.exit(0)
sys.exit(1)
PY
}

# DHCP DISCOVER with this VM's MAC. No REQUEST is sent, so no lease is taken.
# Prints the address the DHCP server would hand this VM right now.
dhcp_offer() {
  python3 - "$IFACE" "$MAC" <<'PY'
import random, socket, struct, sys, time
iface, mac = sys.argv[1], bytes.fromhex(sys.argv[2].replace(':', ''))
xid = random.getrandbits(32)
p = (struct.pack('!BBBBIHH', 1, 1, 6, 0, xid, 0, 0x8000) + b'\0' * 16 + mac + b'\0' * 202
     + b'\x63\x82\x53\x63' + bytes([53, 1, 1, 55, 2, 1, 3, 255]))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, iface.encode() + b'\0')
s.bind(('', 68)); s.settimeout(1); s.sendto(p, ('255.255.255.255', 67))
end = time.time() + 5
while time.time() < end:
    try:
        d, _ = s.recvfrom(2048)
    except socket.timeout:
        continue
    if len(d) >= 240 and struct.unpack('!I', d[4:8])[0] == xid:
        print(socket.inet_ntoa(d[16:20])); sys.exit(0)
sys.exit(1)
PY
}

# Installs a netplan file (old ones are kept in /root), shows the address to
# write down, and reboots one minute later; the new address takes effect at
# boot. The reboot is scheduled with shutdown, so it still happens if the SSH
# session drops or the countdown is interrupted.
install_netplan() {
  local yaml=$1 newip=$2 b A i
  if [[ -f /etc/netplan/50-cloud-init.yaml && "$(cat /etc/netplan/50-cloud-init.yaml)" == "$yaml" ]] &&
     [[ -z "$newip" || "$newip" == "$CUR" ]]; then
    echo "This VM is already set up this way. Nothing to change."
    echo "Your address: $CUR"
    exit 0
  fi
  echo; echo "$yaml"; echo
  read -rp "Install this and reboot the VM in one minute? [y/N] " A
  [[ "$A" =~ ^[Yy]$ ]] || { echo "Nothing was changed."; exit 0; }
  b=/root/netplan-backup-$(date +%Y%m%d-%H%M%S); mkdir -p "$b"
  shopt -s nullglob; for f in /etc/netplan/*.yaml /etc/netplan/*.yml; do mv "$f" "$b/"; done
  echo "$yaml" > /etc/netplan/50-cloud-init.yaml; chmod 600 /etc/netplan/50-cloud-init.yaml
  mkdir -p /etc/cloud/cloud.cfg.d
  echo 'network: {config: disabled}' > /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
  if ! netplan generate; then
    cp "$b"/* /etc/netplan/ && rm -f /etc/netplan/50-cloud-init.yaml
    echo "The new settings did not validate, so the old ones were put back. Nothing was changed." >&2; exit 1
  fi
  shutdown -r +1 "make-static-ip: rebooting to apply the new IP address ${newip:-(DHCP)}" >/dev/null 2>&1

  echo
  echo "=================================================================="
  if [[ -n "$newip" ]]; then
    echo "  WRITE THIS DOWN.  $(hostname) will be at:   $newip"
    echo
    echo "  Connect next time with:  ssh student@$newip"
  else
    echo "  WRITE THIS DOWN after the reboot: this VM will use DHCP."
    echo "  Log in at the console and run 'ip -br a' to see its address."
  fi
  [[ $MODE_WAS == dhcp ]] && [[ -n "$newip" ]] &&
    echo "  (DHCP address; it can change if the VM is off for a long time.)"
  echo
  echo "  For your instructor:  $(hostname)  $MAC  ${newip:-DHCP}"
  echo "=================================================================="
  echo "Old settings are saved in $b."
  echo "To cancel the reboot: sudo shutdown -c  (the new address then applies at the next reboot)"
  echo
  for (( i = 60; i > 0; i-- )); do
    printf '\rRebooting in %2d seconds... ' "$i"; sleep 1
  done
  echo; echo "Rebooting now."
}

to_dhcp() {
  local next
  next=$(dhcp_offer || true)
  echo "DHCP will give this VM: ${next:-(no answer to the probe; DHCP will assign one when applied)}"
  # dhcp-identifier: mac lets OIT reserve an address for this VM by its MAC.
  install_netplan "network:
  version: 2
  ethernets:
    $IFACE:
      dhcp4: true
      dhcp-identifier: mac" "$next"
}

echo "This VM: $(hostname)  MAC $MAC  $CIDR  ($ADDRMODE)"

# Asks the instructor's registry. Prints the reply body; returns 0 on success,
# 1 if the registry refused (reply printed), 2 if it could not be reached.
reg() {
  local out code
  out=$(curl -sS --max-time 5 -w '\n%{http_code}' "http://$REGISTRY/$1" 2>/dev/null) || return 2
  code=${out##*$'\n'}; echo "${out%$'\n'*}"
  [[ $code == 200 ]] && return 0
  [[ $code == 000 ]] && return 2
  return 1
}
q="mac=$MAC&host=$(hostname)"

# --auto: the registry hands this VM an address (the same one on every run) and
# remembers it, so a classmate's powered-off VM never loses its address. The
# ARP probe still runs, and anything found answering is reported as taken. If
# the registry is unreachable, fall back to picking at random among addresses
# nobody answers for, which cannot see powered-off VMs.
MODE_WAS=$MODE
if [[ $MODE == auto ]]; then
  WANT=""
  if [[ $ADDRMODE == static ]] && inblock "$CUR" && ! probe "$CUR" >/dev/null; then
    if R=$(reg "claim?$q&want=$CUR"); then WANT=$CUR; echo "Keeping $CUR (already this VM's)."
    elif [[ $? == 2 ]]; then WANT=$CUR; echo "Keeping $CUR. The registry is unreachable; tell your instructor your address."
    fi
  fi
  if [[ -z "$WANT" ]]; then
    for try in 1 2 3 4 5; do
      R=$(reg "claim?$q") && rc=0 || rc=$?
      if [[ $rc == 2 ]]; then break; fi
      [[ $rc == 0 ]] || { echo "Registry: $R. Tell your instructor." >&2; exit 2; }
      if OTHER=$(probe "$R"); then
        echo "$R was assigned, but $OTHER is answering on it. Reporting it and asking again."
        reg "taken?ip=$R&mac=$OTHER" >/dev/null || true
        continue
      fi
      WANT=$R; echo "Registry assigned $WANT to this VM."; break
    done
    [[ -n "$WANT" || $rc == 2 ]] || { echo "No free address after 5 tries. Tell your instructor." >&2; exit 2; }
  fi
  if [[ -z "$WANT" ]]; then
    echo "WARNING: could not reach the address registry at $REGISTRY. Picking from addresses" >&2
    echo "nobody answers for; tell your instructor which one you get." >&2
    FREE=$(mktemp)
    for (( n = $(ip2int "$COURSE_FIRST"); n <= $(ip2int "$COURSE_LAST"); n++ )); do
      c="$(( (n >> 24) & 255 )).$(( (n >> 16) & 255 )).$(( (n >> 8) & 255 )).$(( n & 255 ))"
      inblock "$c" && echo "$c"
    done > "$FREE.all"
    # Probe 40 at a time so a 253-address block does not start 253 processes.
    export -f probe; export IFACE MAC
    xargs -P 40 -n 1 bash -c 'probe "$1" 2 >/dev/null || echo "$1"' _ < "$FREE.all" > "$FREE"
    rm -f "$FREE.all"
    WANT=$(shuf -n 1 "$FREE" || true); rm -f "$FREE"
    [[ -n "$WANT" ]] || { echo "Every address in the course block is in use. Tell your instructor." >&2; exit 2; }
    echo "Picked $WANT."
  fi
  MODE=static
fi

case $MODE in
  check)
    if OTHER=$(probe "$CUR"); then
      echo "CONFLICT: $CUR is also being used by the machine with MAC $OTHER." >&2
      echo "Run 'sudo bash $0' to move this VM to its own address, and send your instructor that MAC." >&2
      exit 2
    fi
    echo "No other machine is answering for $CUR right now."
    if [[ $ADDRMODE == static ]] && inblock "$CUR"; then echo "OK: static address inside the course block."; exit 0; fi
    if [[ $ADDRMODE == dhcp ]]; then echo "NOT STATIC YET: this VM is still on DHCP. Run 'sudo bash $0' to give it its address." >&2
    else echo "PROBLEM: this static address is inside the DHCP pool. DHCP can give $CUR to another VM at any time. Run 'sudo bash $0' to fix it." >&2; fi
    exit 3 ;;

  dhcp) to_dhcp ;;

  static)
    isip "$WANT" || { echo "'$WANT' is not an IPv4 address." >&2; exit 1; }
    if [[ -z "$COURSE_FIRST" || -z "$COURSE_LAST" ]]; then
      echo "Static addresses are turned off until your instructor has a block of addresses" >&2
      echo "excluded from DHCP. Run 'sudo bash $0' instead; it sets this VM to DHCP." >&2; exit 1
    fi
    inblock "$WANT" || { echo "$WANT is outside the course block $COURSE_FIRST-$COURSE_LAST or reserved. Run with --auto to pick a free one." >&2; exit 1; }
    mask=$(( (0xFFFFFFFF << (32 - PREFIX)) & 0xFFFFFFFF ))
    (( ($(ip2int "$WANT") & mask) == ($(ip2int "$GW") & mask) )) || { echo "$WANT is not on this VM's subnet." >&2; exit 1; }
    [[ "$WANT" != "$GW" ]] || { echo "$WANT is the gateway." >&2; exit 1; }
    if [[ $MODE_WAS != auto ]]; then
      if R=$(reg "claim?$q&want=$WANT"); then :
      elif [[ $? == 1 ]]; then echo "Registry: $R. Nothing was changed; run with --auto instead." >&2; exit 2
      else echo "WARNING: could not reach the address registry; tell your instructor you took $WANT." >&2
      fi
    fi
    if [[ "$WANT" != "$CUR" ]] && OTHER=$(probe "$WANT"); then
      echo "CONFLICT: $WANT is already used by MAC $OTHER. Nothing was changed; run with --auto to pick a free one." >&2; exit 2
    fi
    DNS=$(resolvectl dns "$IFACE" 2>/dev/null | sed 's/^[^:]*: *//' | xargs | sed 's/ /, /g' || true)
    [[ -n "$DNS" ]] || DNS="128.198.1.50, 128.198.1.71"
    install_netplan "network:
  version: 2
  ethernets:
    $IFACE:
      dhcp4: false
      addresses: [$WANT/$PREFIX]
      routes:
        - to: default
          via: $GW
      nameservers:
        addresses: [$DNS]" "$WANT" ;;
esac
