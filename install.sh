#!/bin/bash
#
#
vdir="venv"


echo "
LUUP_CloudConnector - INSTALLER

"
echo "[i] Initializing "

# shoudl do this during provisioning
#~ sudo apt install git python3-venv 

if [ -d "$vdir" ]; then
echo "  >  old venv found, creating new"
    rm -Rf $vdir
fi
echo "  >  installing new virtual-env in $vdir"

echo ">  installing virtualenv in $vdir"
python3 -m venv $vdir


. $vdir/bin/activate

echo ">  installing requirements"




pip3 install --upgrade pyjq
pip3 install --upgrade PyYAML
pip3 install --upgrade requests
pip3 install --upgrade python-dateutil

# providerspecific
pip3 install --upgrade boto3
pip3 install --upgrade google-api-python-client
pip3 install --upgrade python-digitalocean

#pip3 install --upgrade ipaddress  colorama click
#pip3 install --upgrade cpe
#pip3 install --upgrade cvss
#pip3 install --upgrade pygments
#pip3 install --upgrade shodan
#pip3 install --upgrade datetime


mkdir run
mkdir logs

if [ ! -f "config.yaml" ]; then

  echo "> no config_file found, copying config.yaml"
  
  cp config.yaml.example config.yaml
  

else

  echo "> config_file found, will not overwrite it"
  

fi



echo "> edit config.yaml and then run as a test:

> ./lcc ping 

" 
