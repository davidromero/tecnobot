#!/bin/bash

WHITE_COLOR='\E[1;37m'
GREEN_COLOR='\E[0;32m'
ORANGE_COLOR='\E[0;33m'
RED_COLOR='\E[0;31m'

declare -a dep=("alta%20verapaz" "baja%20verapaz" "solola" "chimaltenango" "chiquimula" "el%20progreso" "escuintla" "guatemala" "huehuetenango" "izabal" "jalapa" "jutiapa" "peten" "quetzaltenango" "quiche" "retalhuleu" "sacatepequez" "san%20marcos" "santa%20rosa" "solola" "suchitepequez" "totonicapan" "zacapa") 
deployed_end_p='https://c8i8vtg8dl.execute-api.us-east-1.amazonaws.com/api/'
geo='/geo/'
campaign='/middleware/campaign'
ERR=1

echo -e $WHITE_COLOR 'Testing endpoint Geo Service for ' $deployed_end_p 
for i in "${dep[@]}"
do
    if [[ ERR -eq 1 ]]; then
        res=$(curl -sL -w "%{http_code}\\n" "$deployed_end_p""$geo""$i" -o out.json)
        if [[ res -eq 200 ]]; then
            diff <(jq -S '.payload' out.json) <(jq -S . "$i".json 2>/dev/null) &>/dev/null
            ret=$?
            if [[ ret -eq 0 ]]; then
                echo -e $GREEN_COLOR "Passed test for " "$i"
            else
                echo -e $RED_COLOR "Geo Test (Bad http body) for" "$i"
            fi
        else
            echo -e $RED_COLOR "Geo Test (Bad HTTP response Code) for " "$i"
        fi
    else
        echo -e $RED_COLOR "Test Failed"
#        exit
    fi
done
