#!/bin/bash
#
# This script must be run as root.
# To run with sudo: cat ./gprs-conf.sh | sudo bash

red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
blue=`tput setaf 4`
white=`tput setaf 7`
reset=`tput sgr0`

printf "${white}checking if ${blue}ppp ${white}is installed${reset}..."
INSTALLED=$(which pppd)
if [ -z "${INSTALLED}" ]; then
	printf "${yellow}[NOT INSTALLED]\n${white}installing ${blue}ppp..."
	(apt-get install ppp -y) > /dev/null 2> /dev/null
	if [ $? -gt 0 ]; then
		echo "${red}[ERROR]"
		exit 1
	fi
	printf "${green}[DONE]\n"
else
	printf "${green}[OK]\n"
fi

printf "${white}writing peer configuration..."
(cat << EOF | tee /etc/ppp/peers/gprs
user ""
connect "/usr/sbin/chat -v -f /etc/chatscripts/gprs"
/dev/ttyS0
115200
nocrtscts
debug
nodetach
ipcp-accept-local
ipcp-accept-remote
noipdefault
usepeerdns
defaultroute
persist
noauth
EOF
) > /dev/null 2> /dev/null
if [ $? -gt 0 ]; then
		echo "${red}[ERROR]${reset}"
		exit 1
	fi
printf "${green}[OK]\n${reset}"

printf "${white}creating ${blue}gprs ${white}systemd service..."
(cat << EOF | tee /etc/systemd/system/gprs.service
[Unit]
Description=GPRS internet connection

[Service]
ExecStart=/usr/sbin/pppd call gprs

[Install]
WantedBy=multi-user.target
EOF
) > /dev/null 2> /dev/null
if [ $? -gt 0 ]; then
		echo "${red}[ERROR]${reset}"
		exit 1
	fi
printf "${green}[OK]\n${reset}"
chmod 640 /etc/systemd/system/gprs.service
systemctl daemon-reload

printf "${white}creating ip-up script..."
(cat << EOF | tee /etc/ppp/ip-up.d/addroute
#!/bin/bash

/sbin/route add -net 0.0.0.0 ppp0
EOF
) > /dev/null 2> /dev/null
if [ $? -gt 0 ]; then
		echo "${red}[ERROR]${reset}"
		exit 1
	fi
printf "${green}[OK]\n${reset}"
chmod 755 /etc/ppp/ip-up.d/addroute