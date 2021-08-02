
## Usage


get help with ` ./lcc -h `

~~~

lcc@lcc-prod:~/cloudconnector

$ ./lcc -h

USAGE:

  lcc -h     -> this help
  
  lcc ping   -> test api_connection
  
  lcc run    -> collect IPs and update LUUP_API


~~~


run the update manually 

~~~

lcc@lcc-prod:~/cloudconnector

$ ./lcc run

**************************************************
************* Scanning AWS    ********************
**************************************************

**************************************************
************* Scanning Azure  ********************
**************************************************

**************************************************
************* Scanning Digital Ocean  ************
**************************************************

*******************************************************************************************************
Data has been written to file : output/result.16278845678.json. Please open the file to see result.
*******************************************************************************************************

[+] Luup Updated: OK | 201 | changed


~~~

## Datastore

after each run, a resultset is stored in `outpout/result.TIMESTAMP.json`
as well as data that has been transferred to the LUUP-API




