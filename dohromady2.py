#!/usr/bin/python3
import os
import sys
import time
from subprocess import PIPE, run
#funkce pro ssh pripojeni
def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout

#vypise napovedu pokud neni zadan host nebo je pouzit parametr -h
if len(sys.argv[1]) < 1 or sys.argv[1] in ("-h", "--help"):
    print("pouziti:")
    print("./dohromady2.py <host>")

#zkontroluje zda je host v pohode
try:
    if sys.argv[1].split(".")[1] in ("ko", "ng"):
        print("host ok")
except:
    print("neplatny hostname")
    sys.exit()

#ulozi lxlist
host=sys.argv[1]
tmp=out("ssh {} '/www/lxc/bin/lxlist -v'".format(host))
final=str(tmp)

#zkontroluje zda jsou vsechny virtualy zapnute, kdyz ne, tak se zepta zda chceme zapnout
for stp in final.split('\n'):
    if "STOP" in stp:
        name=stp.split()[1]
        id=stp.split()[0]
        ans=input("{} je vypnuty, zapnout(y/n)?".format(name))
        if ans in ("y", "Y", "yes"):
            out("ssh {} '/www/lxc/bin/lxctl start {}'".format(host, id))

time.sleep(5) #pocka par sekund po zapnuti

#samotne nahozeni sluzeb na virtualech
for szn in final.split('\n'):
    id=szn.split()[0]
    name=szn.split()[1]
    if "email-scan-in" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} 'etc/init.d/szn-email-scanner restart;/etc/init.d/szn-email-twisted-aeros-proxy restart;/etc/init.d/szn-email-delayed-balancer restart;/etc/init.d/szn-email-nanoprometheus-server restart;/etc/init.d/szn-email-scanner-neurotic-classifier restart;sleep 2;/etc/init.d/szn-email-scanner start;/etc/init.d/szn-email-twisted-aeros-proxy start;/etc/init.d/szn-email-delayed-balancer start;/etc/init.d/szn-email-nanoprometheus-server start;/etc/init.d/szn-email-scanner-neurotic-classifier start''".format(host, id))

    if "email-proxy" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-email-proxy start;/etc/init.d/szn-email-gnscachedaemon start''".format(host, id))

    if "napoveda" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-napoveda-web-proxy restart;/etc/init.d/szn-napoveda-web-lb restart;/etc/init.d/szn-napoveda-web restart;sleep 2;/etc/init.d/szn-napoveda-web-proxy start;/etc/init.d/szn-napoveda-web-lb start;/etc/init.d/szn-napoveda-web start''".format(host, id))

    if "dmarcd" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-email-dmarcd start''".format(host, id))

    if "fbl" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-email-fbld start;/etc/init.d/szn-email-gnscachedaemon start''".format(host, id))

    if "domain" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-email-domain-server start;/etc/init.d/szn-email-gnscachedaemon start''".format(host, id))

    if "aero" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/aerospike start;/etc/init.d/amc start''".format(host, id))

    if "rus-login" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-rus-login start;sleep 2s;/etc/init.d/szn-rus-login-proxy restart''".format(host, id))

    if "rus-sbox" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-rus-sbox start;sleep 2;/etc/init.d/szn-rus-sbox-proxy restart''".format(host, id))

    if "rus-icon" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-rus-icon-server start;sleep 2;/etc/init.d/szn-rus-icon-server-proxy restart''".format(host, id))

    if "email-bounce" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-email-bouncer start''".format(host, id))

    if "email-mda" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-email-mda start;/etc/init.d/szn-email-gnscachedaemon start''".format(host, id))

    if "email-qm" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-email-queue-manager start;/etc/init.d/szn-email-gnscachedaemon start''".format(host, id))

    if szn in ("email-pop", "email-notify-pub"):
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-email-pop3 start;/etc/init.d/szn-email-gnscachedaemon start''".format(host, id))

    if "email-imap" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-email-imap start;/etc/init.d/szn-email-gnscachedaemon start''".format(host, id))

    if "email-nametag" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-email-delayed-balancer restart;/etc/init.d/szn-email-nametag-proxy restart;/etc/init.d/szn-email-scanner-nametag-classifier restart;sleep 2;/etc/init.d/szn-email-delayed-balancer start;/etc/init.d/szn-email-nametag-proxy start;/etc/init.d/szn-email-scanner-nametag-classifier start''".format(host, id))

    if szn in ("email-smtpi", "email-smtpd", "email-mx", "email-relay"):
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-email-smtpd start;/etc/init.d/szn-email-gnscachedaemon start''".format(host, id))

    if "email-av" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-esets restart''".format(host, id))

    if "email-ebox-ssd" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-email-ebox start;/etc/init.d/szn-email-gnscachedaemon start''".format(host, id))

    if "email-rescue-ssd" in szn:
        print("delam {}".format(name))
        out("ssh {} '/www/lxc/bin/lxctl exec {} '/etc/init.d/szn-email-rescue start;/etc/init.d/szn-email-gnscachedaemon start''".format(host, id))
