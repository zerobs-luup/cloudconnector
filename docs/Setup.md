
## Setup your LUUP-Account for API-Usage


- Goto to the [API-Section of your settings](https://luup-console.de/settings#api_key)
and click on "{ Generate }" to generate a new API-Key, if there is none per default:
no API-Key is generated

- copy that API-KEY 


## Install CloudConnector

- use either a small VPS or even a RasPi
- requirements: 1 CPU, 512 MB RAM, 20 GB HDD
- be sure the server can reach the LUUP_API (see Usage.md)
- the following softwarepackages are required (install-commands
are valid for debian/ubunto-derivates, YMMV):

~~~

git
python3-virtualenv
python3-pip
dh-autoreconf  (deb-specific, but basically autoconf/automake and its requirements)


apt install git python3-virtualenv python3-venv python3-pip dh-autoreconf



~~~

- download software and cd into `cloudconnector`

~~~

git clone https://github.com/zerobs-luup/cloudconnector.git

~~~

- run `install.sh` to install all required packages into a local virtualenv

- edit `config.yaml` to setup your cloudproviders and LUUP_API_KEY

- test your config with `./lcc ping`

~~~

lcc@lcc-prod:~/cloudconnector

$ ./lcc ping
[+] Luup PING: OK | 200 | ping_ok 
    API: https://api.luup-console.de/api/v1/ping

~~~

## Setup your cloud-accounts to allow CloudConnector to read 

currently the following cloudproviders are available
and can be configured to deliver ip-information for
automated luup-updates:

- Amazon AWS
- Google GPC
- Microsoft Azure
- DigitalOcean
- Hetzner

and additionally:

- you can use flatfiles as import_source


### Note:

If you comment out credentials in config.yaml file, that provider would automatically be ignore while running.


## Setup AWS


Install aws-cli tool from https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html

and then enter your default credentials if you want using:

````
$ aws configure

AWS Access Key ID [None]: FQDN2448AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: json

````

more information : https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html


#### Credentials file

If you want to add more users please visit : ```~/.aws/credentials``` file
the content would look like something like this:

````

[default]
aws_access_key_id = key
aws_secret_access_key = seceret

````

#### Configure lcc


finally, edit and set the following in `config.yaml`, client-names
beeing one or more projects you_d like to be integrated with luup

~~~

aws:
  client-names:
  - default
  - non-default
  - test

~~~




## Setup (DigitalOcean)

- Activate an API_Token on your [API-Settings-Page](https://cloud.digitalocean.com/account/api/)
on the interface
- make sure your token has Read-Only-rights
- copy that token, because it will be displayed only once
- edit and set the following in `config.yaml`

~~~

digital-ocean:
  token: YOURDIGIOTALOCEANTOKENHERE

~~~


## Setup (Azure)

You would need to set ``azure`` in config.yaml file for which you would need:
 1. client-id 
 2. client-secret
 3. subscription-id
 4. tenant-id
 and for creating these credentials you can follow these steps:
    1. visit https://portal.azure.com/#home which would lead you to portal for azure.
    2. then click <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDYyJYPqlR0gMnWHi3n6YE5LnXoNfKvSN85g&usqp=CAU" width="15" height="15" /> button which is on the top right menu.
    3. write following command ```az ad sp create-for-rbac``` which would give you appId(client-id), password(client-secret), tenant(tenant-id),<br/>Please save these credentials somewhere to use them afterwards.
    4. For ``` subscription-id ``` please type ``` az account show --query id -o tsv ``` command and save it.
    5. Fill in the credentials in config.yaml file.
   
All set!



## Setup (Google Cloud Systems)

Please follow these steps:
1. Setup ```` export GOOGLE_APPLICATION_CREDENTIALS="[key_file]" ````
   1. Open google console and go for this <a href="https://console.cloud.google.com/apis/credentials"> Link</a>
   2. There you can make api credentials and then save them as json
   3. Now open your .bashrc file and save global variable <b> GOOGLE_APPLICATION_CREDENTIALS </b> value as the location for this json file.
2. Now simple mention you project name in config.yaml file.   
