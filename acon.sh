#!/bin/sh
#
# Load arabic console support
#
# chkconfig: 2345 99 06
# description: This package loads the arabic support for the Linux console \
#   allowing right-to-left display of Arabic/Farsi/Hebrew text

#[ -f /usr/bin/acon ] || exit 0

# Source function library.
. /etc/rc.d/init.d/functions

# source i18n values, so acon knows which support (Arabic, Hebrew,...) to use
. /etc/sysconfig/i18n

[ -z "$LANG" -a -n "$LC_ALL" ] && LANG=$LC_ALL
[ -z "$LANG" -a -n "$LC_CTYPE" ] && LANG=$LC_CTYPE
[ -z "$LANG" -a -n "$LANGUAGE" ] && LANG=$LANGUAGE

case "$LANG" in
	ar*) LANG_NAME=`gprintf "Arabic"`;;
	fa*) LANG_NAME=`gprintf "Farsi"`;;
	he*) LANG_NAME=`gprintf "Hebrew"`;;
	ps*) LANG_NAME=`gprintf "Pashto"`;;
	ur*) LANG_NAME=`gprintf "Urdu"`;;
	yi*) LANG_NAME=`gprintf "Yiddish"`;;
	*) LANG_NAME=`gprintf "Arabic"`;;
esac

[ -z "$HENDI_NUM" ] && HENDI_NUM="-hn"

case "$1" in
	start)
		gprintf "Loading %s console support: " "$LANG_NAME"
		/usr/bin/acon $HENDI_NUM -s 1 2 3 4 5 6 &
		ps auwx | grep /usr/bin/acon | grep -v grep >& /dev/null \
			&& success || failure
		touch /var/lock/subsys/acon
		;;
	stop)
		gprintf "Stopping %s console support: " "$LANG_NAME"
		killall acon && success || failure
		rm -f /var/lock/subsys/acon
		;;
	restart|reload)
		$0 stop
		$0 start
		;;
	status)
		status acon
		;;
	*)
		gprintf "Usage: %s\n" "`basename $0` {start|stop|restart|reload|status}" 
		exit 1
esac

exit 0
