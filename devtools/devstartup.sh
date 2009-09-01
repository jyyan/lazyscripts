#!/bin/bash


function select_repo () {
    DISTRO_NAME="$DISTRO_ID"
    AVAILABLE_REPO=($(cat conf/repository.conf  | grep "${DISTRO_NAME}" | cut -d " " -f 1 | grep "^[git].*[git]$"))
    if [ ${#AVAILABLE_REPO[@]} -eq 1 ];then
        USE_REPO=(${AVAILABLE_REPO})
        REPO_URL=(${AVAILABLE_REPO})
    else
        if [ -z $WIN_MGR ] ; then
            if which zenity &> /dev/null ; then
                SHOW_REPO=$(for uri in ${AVAILABLE_REPO[*]} ; do echo -n "FALSE $uri " ; done)
                USE_REPO=$(zenity --list --title="Choice Scripts Repository You Want to Use" --radiolist --column "" --column "Repository URL" ${SHOW_REPO})
            elif which kdialog &> /dev/null ; then
                SHOW_REPO=$(for uri in ${AVAILABLE_REPO[*]} ; do echo -n "${uri} ${uri} off " ; done)
                USE_REPO=$(kdialog --title="Choice Scripts Repository You Want to Use" --radiolist "Choice a Repository URL" ${SHOW_REPO})
            else
#                echo "Some error happend."
                PS3_BAK=$PS3
                PS3="Choice Scripts Repository You Want to Use : "
                select USE_REPO in ${AVAILABLE_REPO[*]}
                do
                    if [ ! -z $USE_REPO ] ; then
                        break
                    else
                        echo "Please select again."
                    fi
                done
                PS3=$PS3_BAK
            fi
        else
            case $WIN_MGR in
            "Gnome")
                SHOW_REPO=$(for uri in ${AVAILABLE_REPO[*]} ; do echo -n "FALSE $uri " ; done)
                USE_REPO=$(zenity --list --title="Choice Scripts Repository You Want to Use" --radiolist --column "" --column "Repository URL" ${SHOW_REPO})
                    ;;
            "KDE")
                SHOW_REPO=$(for uri in ${AVAILABLE_REPO[*]} ; do echo -n "${uri} ${uri} off " ; done)
                USE_REPO=$(kdialog --title="Choice Scripts Repository You Want to Use" --radiolist "Choice a Repository URL" ${SHOW_REPO})
                    ;;
            *)
                SHOW_REPO=$(for uri in ${AVAILABLE_REPO[*]} ; do echo -n "FALSE $uri " ; done)
                USE_REPO=$(zenity --list --title="Choice Scripts Repository You Want to Use" --radiolist --column "" --column "Repository URL" ${SHOW_REPO})
                    ;;
            esac
        fi
                    
        REPO_URL=(${USE_REPO/|/ })
    fi
    export REPO_URL
    export REPO_NUM=${#REPO_URL[@]}
    for ((num=0;num<${REPO_NUM};num=$num+1)); do 
        REPO_DIR[$num]="./scriptspool/`./lzs repo sign ${REPO_URL[${num}]}`"
        if [ -d ${REPO_DIR[$num]} ];then
            pushd ${REPO_DIR[$num]}
            git pull
            popd
        #     rm -rf ${REPO_DIR[$num]}
        else
            git clone ${REPO_URL[$num]} ${REPO_DIR[$num]}
        fi
        ./lzs list build ${REPO_URL[$num]}
    done
}

select_repo


