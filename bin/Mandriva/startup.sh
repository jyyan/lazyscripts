#!/bin/bash
# -*- coding: UTF-8 -*-
# This is a startup file for Mandriva

echo "source ~/.bashrc" >> $ENV_EXPORT_SCRIPT

if [ -z "$DISTRO_VERSION" ];then
    DISTRO_VERSION=`zenity --list --title="Choice your linux distribution version" --radiolist --column "" --column "Linux Distribution Version" FALSE "Mandriva 2009.1"`
    case $DISTRO_VERSION in
        "Mandriva 2009.1")
        export DISTRO_VERSION="2009.1"
        ;;
    esac
    echo "export DISTRO_VERSION=${DISTRO_VERSION}" >> $ENV_EXPORT_SCRIPT
fi

if [ -z "$DESKTOP_SESSION" ];then
    WIN_MGR=`zenity --list --title="Choice your window manager" --radiolist --column "" --column "Linux Distribution Version" FALSE "Gnome" FALSE "KDE"`
else
    case ${DESKTOP_SESSION} in
	    '02GNOME')
	    export WIN_MGR='Gnome'
	    echo "export WIN_MGR=\"Gnome\"" >> $ENV_EXPORT_SCRIPT
	    ;;  
	    '01KDE4')
	    export WIN_MGR='KDE'
	    echo "export WIN_MGR=\"KDE\"" >> $ENV_EXPORT_SCRIPT
	    ;;    
	    *)  
	    echo "Lazysciprs can't identified your window manager"
	    export WIN_MGR=''
	    echo "export WIN_MGR=\"\"" >> $ENV_EXPORT_SCRIPT
	    ;;  
	esac
fi
if which zenity &> /dev/null ; then
    if ! zenity --question "Lazyscripts will install some required packages. Press OK to continue and install, or Press Cancel to exit." ; then
        exit
    fi
elif which kdialog &> /dev/null ; then
    if ! kdialog --warningcontinuecancel "Lazyscripts will install some required packages. Press OK to continue and install, or Press Cancel to exit." ; then
        exit
    fi 
else
    echo  "Lazyscripts will install some required packages."
fi

echo "source bin/${DISTRO_ID}/install_require_packages.sh" >> $ENV_EXPORT_SCRIPT
