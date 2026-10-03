#Requires -RunAsAdministrator
<#
make-static-ip.ps1: give this Windows VM its static IPv4 address on VLAN 1020.

  lastname-win:  .\make-static-ip.ps1                        get this VM's address from the course registry
  any VM:        .\make-static-ip.ps1 -Check                 check only, change nothing
  any VM:        .\make-static-ip.ps1 -IPAddress 10.5.103.x  use a specific address from the course block
  undo:          .\make-static-ip.ps1 -Dhcp                  go back to DHCP

Run from an elevated PowerShell (console, RDP, or SSH):
  powershell -ExecutionPolicy Bypass -File .\make-static-ip.ps1

When it changes the address, it shows the new one to write down, waits one
minute (Ctrl+C cancels; nothing has changed yet), then applies it and reboots.
Running it again on a VM that already has its address changes nothing.

Why: VLAN 1020 runs a live DHCP pool with 1-hour leases. The earlier version
of this script turned the VM's DHCP address into a static one, but the address
stayed in the pool, so within about an hour DHCP could lease it to another VM.
Two VMs on one address means RDP and logins land on either machine at random
("my password works sometimes"). So static addresses now come only from the
course block (10.5.103.x), which sits above the addresses DHCP is handing out,
and the instructor's registry records which VM has each one.
#>
param([string]$IPAddress, [switch]$Check, [switch]$Dhcp, [switch]$Auto)
$ErrorActionPreference = 'Stop'

$CourseFirst = '10.5.103.1'      # course block for static addresses: all of 10.5.103.x
$CourseLast  = '10.5.103.254'
$Reserved    = @('10.5.103.250') # inside the block but never handed out (the registry VM)
$Registry    = '10.5.103.250:8080'  # instructor VM that records which VM has which address

$route = Get-NetRoute -AddressFamily IPv4 -DestinationPrefix '0.0.0.0/0' -PolicyStore ActiveStore -ErrorAction SilentlyContinue |
    Sort-Object { $_.RouteMetric + (Get-NetIPInterface -InterfaceIndex $_.InterfaceIndex -AddressFamily IPv4).InterfaceMetric } |
    Select-Object -First 1
if (-not $route) { throw 'No IPv4 default route; cannot read network settings. Ask your instructor.' }
$idx = $route.InterfaceIndex; $gw = $route.NextHop
$adapter = Get-NetAdapter -InterfaceIndex $idx
$mac = $adapter.MacAddress.ToLower().Replace('-', ':')
$cur = Get-NetIPAddress -InterfaceIndex $idx -AddressFamily IPv4 |
    Where-Object { $_.IPAddress -notlike '169.254.*' } | Select-Object -First 1
$curIp = $cur.IPAddress; $prefix = $cur.PrefixLength
$isDhcp = (Get-NetIPInterface -InterfaceIndex $idx -AddressFamily IPv4).Dhcp -eq 'Enabled'
$hostName = $env:COMPUTERNAME

function ToInt([string]$a) { $b = ([ipaddress]$a).GetAddressBytes(); [uint64]$b[0] * 16777216 + $b[1] * 65536 + $b[2] * 256 + $b[3] }
function ToIp([uint64]$n) { (($n -shr 24) -band 255), (($n -shr 16) -band 255), (($n -shr 8) -band 255), ($n -band 255) -join '.' }
# Stops unless $a is on this VM's own network (true for the course block on
# VLAN 1020; a VM on another network would end up unreachable).
function Test-OnSubnet([string]$a) {
    $hb = [uint64]1 -shl (32 - $prefix)
    if ([math]::Floor((ToInt $a) / $hb) -ne [math]::Floor((ToInt $gw) / $hb)) {
        Write-Host "$a is not on this VM's network ($curIp/$prefix). Is this VM on the course network (VLAN 1020)? Nothing was changed." -ForegroundColor Red; exit 1
    }
    if ($a -eq $gw) { Write-Host "$a is the gateway. Nothing was changed." -ForegroundColor Red; exit 1 }
}
function Test-InBlock([string]$a) {
    if ($Reserved -contains $a) { return $false }
    $n = ToInt $a; return ($n -ge (ToInt $CourseFirst) -and $n -le (ToInt $CourseLast))
}

# ARP through Windows itself (SendARP). Works even when the other machine's
# firewall blocks ping. Types added here are visible to the runspaces below.
Add-Type -Namespace CourseNet -Name Arp -MemberDefinition @'
[DllImport("iphlpapi.dll", ExactSpelling = true)]
public static extern int SendARP(uint DestIP, uint SrcIP, byte[] pMacAddr, ref uint PhyAddrLen);
'@
$arpScript = {
    param([string]$a)
    $m = New-Object byte[] 6; $len = [uint32]6
    $ip = [BitConverter]::ToUInt32(([ipaddress]$a).GetAddressBytes(), 0)
    if ([CourseNet.Arp]::SendARP($ip, 0, $m, [ref]$len) -eq 0) { ($m[0..5] | ForEach-Object { $_.ToString('x2') }) -join ':' }
}

# MAC of another machine using address $a, or $null. Windows cannot ARP its
# own address, so for that it reads the conflicts it logged in the last 24
# hours (System log, Tcpip event 4199).
function Find-Holder([string]$a) {
    if ($a -eq $curIp) {
        $ev = Get-WinEvent -FilterHashtable @{ LogName = 'System'; Id = 4199; StartTime = (Get-Date).AddHours(-24) } -ErrorAction SilentlyContinue |
            Where-Object { $_.ProviderName -match 'Tcpip' -and $_.Message -match "\b$([regex]::Escape($a))\b" } |
            Select-Object -First 1
        if ($ev) { if ($ev.Message -match '([0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}') { return $Matches[0].ToLower().Replace('-', ':') } else { return 'unknown' } }
        return $null
    }
    $m = & $arpScript $a
    if ($m -and $m -ne $mac) { return $m }
    return $null
}

# Asks the instructor's registry. Returns @{ Code; Body }; Code 0 = unreachable.
function Invoke-Registry([string]$path) {
    try {
        $r = Invoke-WebRequest -UseBasicParsing -TimeoutSec 5 -Uri "http://$Registry/$path"
        $body = $r.Content
        if ($body -is [byte[]]) { $body = [Text.Encoding]::UTF8.GetString($body) }  # no Content-Type: PS 5.1 returns bytes
        return @{ Code = [int]$r.StatusCode; Body = "$body".Trim() }
    } catch {
        $resp = $_.Exception.Response
        if (-not $resp) { return @{ Code = 0; Body = '' } }
        $body = "$($_.ErrorDetails.Message)"
        if (-not $body) {
            try { $body = (New-Object IO.StreamReader($resp.GetResponseStream())).ReadToEnd() } catch { }
        }
        return @{ Code = [int]$resp.StatusCode; Body = $body.Trim() }
    }
}
$q = "mac=$mac&host=$hostName"

function Clear-Static {
    foreach ($store in 'ActiveStore', 'PersistentStore') {
        Get-NetRoute -InterfaceIndex $idx -DestinationPrefix '0.0.0.0/0' -PolicyStore $store -ErrorAction SilentlyContinue | Remove-NetRoute -Confirm:$false
        Get-NetIPAddress -InterfaceIndex $idx -AddressFamily IPv4 -PolicyStore $store -ErrorAction SilentlyContinue |
            Where-Object { $_.IPAddress -notlike '169.254.*' } | Remove-NetIPAddress -Confirm:$false
    }
}

function Set-DhcpNow {
    Clear-Static
    Set-NetIPInterface -InterfaceIndex $idx -AddressFamily IPv4 -Dhcp Enabled
    Set-DnsClientServerAddress -InterfaceIndex $idx -ResetServerAddresses
}

# Shows the address to write down, waits a minute (Ctrl+C cancels and nothing
# changes), schedules the reboot, then applies. Scheduling first means the
# reboot still happens if the address change drops this RDP or SSH session.
function Invoke-Change([string]$newIp) {   # $newIp empty = DHCP
    $dns = @((Get-DnsClientServerAddress -InterfaceIndex $idx -AddressFamily IPv4).ServerAddresses)
    if (-not $dns) { $dns = @('128.198.1.50', '128.198.1.71') }
    if ($newIp) {
        Test-OnSubnet $newIp
        if (-not $isDhcp -and $newIp -eq $curIp) { Write-Host "This VM is already set up this way. Nothing to change.`nYour address: $curIp"; exit 0 }
        Write-Host "`nWill set: static $newIp/$prefix  gateway $gw  dns $($dns -join ', ')"
    } else {
        if ($isDhcp) { Write-Host "This VM already uses DHCP. Nothing to change.`nYour address: $curIp"; exit 0 }
        Write-Host "`nWill set: DHCP (automatic address)"
    }
    if ((Read-Host 'Apply this and reboot the VM in one minute? [y/N]') -notmatch '^[Yy]$') { Write-Host 'Nothing was changed.'; exit 0 }

    Write-Host ''
    Write-Host '=================================================================='
    if ($newIp) {
        Write-Host "  WRITE THIS DOWN.  $hostName will be at:   $newIp" -ForegroundColor Yellow
        Write-Host ''
        Write-Host "  Connect next time with:  mstsc /v:$newIp"
    } else {
        Write-Host '  This VM will use DHCP. After the reboot, run ipconfig at the' -ForegroundColor Yellow
        Write-Host '  console to see its address.' -ForegroundColor Yellow
    }
    Write-Host ''
    Write-Host "  For your instructor:  $hostName  $mac  $(if ($newIp) { $newIp } else { 'DHCP' })"
    Write-Host '=================================================================='
    Write-Host 'Press Ctrl+C during the countdown to cancel. Nothing has changed yet.'
    for ($i = 60; $i -gt 0; $i--) { Write-Host -NoNewline ("`rApplying and rebooting in {0,2} seconds... " -f $i); Start-Sleep -Seconds 1 }
    Write-Host ''

    shutdown.exe /r /t 20 /c "make-static-ip: rebooting to apply the new IP address $(if ($newIp) { $newIp } else { '(DHCP)' })" | Out-Null
    if (-not $newIp) { Set-DhcpNow; Write-Host 'DHCP is on. Rebooting in 20 seconds.' -ForegroundColor Green; return }

    Set-NetIPInterface -InterfaceIndex $idx -AddressFamily IPv4 -Dhcp Disabled
    Clear-Static
    New-NetIPAddress -InterfaceIndex $idx -IPAddress $newIp -PrefixLength $prefix -DefaultGateway $gw | Out-Null
    Set-DnsClientServerAddress -InterfaceIndex $idx -ServerAddresses $dns
    # Windows runs duplicate address detection when the address is added.
    $deadline = (Get-Date).AddSeconds(10)
    do { Start-Sleep -Milliseconds 500; $state = (Get-NetIPAddress -InterfaceIndex $idx -IPAddress $newIp -ErrorAction SilentlyContinue).AddressState }
    while ($state -eq 'Tentative' -and (Get-Date) -lt $deadline)
    if ("$state" -eq 'Duplicate') {
        Write-Host "Windows found another machine on $newIp. Switched to DHCP instead; tell your instructor." -ForegroundColor Red
        Invoke-Registry "taken?ip=$newIp&mac=00:00:00:00:00:00" | Out-Null
        Set-DhcpNow
    } else {
        Write-Host "Static $newIp is set. Rebooting in 20 seconds." -ForegroundColor Green
    }
}

Write-Host "This VM: $hostName  MAC $mac  $curIp/$prefix  ($(if ($isDhcp) { 'dhcp' } else { 'static' }))"

if ($Dhcp) { Invoke-Change ''; exit 0 }

if ($Check) {
    $holder = Find-Holder $curIp
    if ($holder) {
        Write-Host "CONFLICT: $curIp was also claimed by the machine with MAC $holder." -ForegroundColor Red
        Write-Host 'Run .\make-static-ip.ps1 to move this VM to its own address, and send your instructor that MAC.'
        exit 2
    }
    Write-Host "No address conflict logged for $curIp in the last 24 hours."
    if (-not $isDhcp -and (Test-InBlock $curIp)) { Write-Host 'OK: static address inside the course block.' -ForegroundColor Green; exit 0 }
    if ($isDhcp) { Write-Host 'NOT STATIC YET: this VM is still on DHCP. Run .\make-static-ip.ps1 to give it its address.' -ForegroundColor Yellow }
    else { Write-Host "PROBLEM: this static address is inside the DHCP pool. DHCP can give $curIp to another VM at any time. Run .\make-static-ip.ps1 to fix it." -ForegroundColor Red }
    exit 3
}

# No options: same as -Auto.
if (-not $IPAddress) { $Auto = [switch]$true }

if ($Auto) {
    # The registry hands this VM an address (the same one on every run) and
    # remembers it. The ARP check still runs, and anything found answering is
    # reported as taken. If the registry is unreachable, pick at random among
    # addresses nobody answers for, which cannot see powered-off VMs.
    Test-OnSubnet $CourseFirst   # refuse at once if this VM is not on the course network
    $want = $null; $unreachable = $false
    if (-not $isDhcp -and (Test-InBlock $curIp) -and -not (Find-Holder $curIp)) {
        $r = Invoke-Registry "claim?$q&want=$curIp"
        if ($r.Code -eq 200) { $want = $curIp; Write-Host "Keeping $curIp (already this VM's)." }
        elseif ($r.Code -eq 0) { $want = $curIp; Write-Host "Keeping $curIp. The registry is unreachable; tell your instructor your address." }
    }
    if (-not $want) {
        for ($try = 1; $try -le 5; $try++) {
            $r = Invoke-Registry "claim?$q"
            if ($r.Code -eq 0) { $unreachable = $true; break }
            if ($r.Code -ne 200) { Write-Host "Registry: $($r.Body). Tell your instructor." -ForegroundColor Red; exit 2 }
            $other = Find-Holder $r.Body
            if ($other) {
                Write-Host "$($r.Body) was assigned, but $other is answering on it. Reporting it and asking again."
                Invoke-Registry "taken?ip=$($r.Body)&mac=$other" | Out-Null
                continue
            }
            $want = $r.Body; Write-Host "Registry assigned $want to this VM."; break
        }
        if (-not $want -and -not $unreachable) { Write-Host 'No free address after 5 tries. Tell your instructor.' -ForegroundColor Red; exit 2 }
    }
    if (-not $want) {
        Write-Host "WARNING: could not reach the address registry at $Registry. Picking from addresses" -ForegroundColor Yellow
        Write-Host 'nobody answers for; tell your instructor which one you get.' -ForegroundColor Yellow
        $cands = for ($n = ToInt $CourseFirst; $n -le (ToInt $CourseLast); $n++) { $c = ToIp $n; if (Test-InBlock $c) { $c } }
        # Probe 40 at a time; an unanswered ARP takes a few seconds each.
        $pool = [runspacefactory]::CreateRunspacePool(1, 40); $pool.Open()
        $jobs = foreach ($c in $cands) {
            $ps = [powershell]::Create(); $ps.RunspacePool = $pool
            [void]$ps.AddScript($arpScript).AddArgument($c)
            @{ PS = $ps; H = $ps.BeginInvoke(); Ip = $c }
        }
        $free = foreach ($j in $jobs) { $res = $j.PS.EndInvoke($j.H); $j.PS.Dispose(); if (-not $res) { $j.Ip } }
        $pool.Close()
        $free = @($free)
        if (-not $free) { Write-Host 'Every address in the course block is in use. Tell your instructor.' -ForegroundColor Red; exit 2 }
        $want = $free | Get-Random
        Write-Host "$($free.Count) free; picked $want."
    }
    Invoke-Change $want; exit 0
}

# Static on a specific address.
$ip = $IPAddress.Trim()
if (-not ($ip -as [ipaddress]) -or $ip -notmatch '^(\d{1,3}\.){3}\d{1,3}$') { Write-Host "'$ip' is not an IPv4 address." -ForegroundColor Red; exit 1 }
if (-not (Test-InBlock $ip)) { Write-Host "$ip is outside the course block $CourseFirst-$CourseLast or reserved. Run with -Auto to pick a free one." -ForegroundColor Red; exit 1 }
Test-OnSubnet $ip
$r = Invoke-Registry "claim?$q&want=$ip"
if ($r.Code -eq 0) { Write-Host "WARNING: could not reach the address registry; tell your instructor you took $ip." -ForegroundColor Yellow }
elseif ($r.Code -ne 200) { Write-Host "Registry: $($r.Body). Nothing was changed; run with -Auto instead." -ForegroundColor Red; exit 2 }
if ($ip -ne $curIp) {
    $holder = Find-Holder $ip
    if ($holder) { Write-Host "CONFLICT: $ip is already used by MAC $holder. Nothing was changed; run with -Auto instead." -ForegroundColor Red; exit 2 }
}
Invoke-Change $ip
