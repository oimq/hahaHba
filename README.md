## hahaHba

##### Handler for hbase with happybase module

for installing and using, requirements are below : 

* tqdm : https://github.com/tqdm/tqdm

* happybase : https://github.com/python-happybase/happybase

* thrift : https://github.com/Thriftpy/thriftpy2

* Hash : https://github.com/oimq/Hash

###### 'Very thanks to happybase.'

***

### Installation

The pre-install resource is hasH : https://github.com/oimq/Hash

```code
pip3 install hahaHba-master/
```

***

### Projects

Before we started, if you don't know about HBase,

please study from here : https://hbase.apache.org/, https://hbase.apache.org/apache_hbase_reference_guide.pdf

happybase API would be very helpful : https://happybase.readthedocs.io/en/latest/api.html

hahaHba consisted by three parts.

##### hahaHba 

* exists : Check table is exists.

* create_table, delete_table : Create and Delete the table.

* put : Input the data to table.

* pop : Delete the data from table.

* scan : Search the data from table.

* rows : Search the data by row-keys from table.

##### hahaSavor

* reset : Delete the exists tables and create the new table.

* generate : Using hasH module.

* store : Store the data.

##### hahatools.json

* metadata for hahaHba and hahaSavor (look demo/save_to_hbase.py)

```python3
{
    'SAVOR':{
        'SPECIAL':{
            'human':[ # fix the value to 1
                'fix', '1',
            ],
            "code" :[ # set the value to row-key
                "row_key"
            ],
        },
        'TRASH':['trash'] # do not regards fields.
    },
    'TABLE':{
        'REF'   :'type',     # field for table id
        'PREFIX':'table_',   # prefix for table name
        'ROW':{
            'KEY':{          # we create the row-key from below fields
                'MATERIAL':[('name', 4), ('phone', 6)],
                'FUNC':'hasHXOR' # now, only hasHXOR function is avaliable
            },
        },
        'IDS':[ # we make the table with prefix like : ['test_one', 'test_two']
            'friends', 'business'
        ],
        'COLUMN':{
            'FAMILIES' : {    # HBase column families. 'family':'field'
                'n':'name',
                'i':'info',
            },
            'QUALIFIERS' : {  # HBase column qualifier. 'qualifier':'field'
                'i:a':'age',
                'i:p':'phone',
                'i:c':'code',
                'i:h':'human'
            },
            'RAW_FAM' : ['n'] # There are column families which are don't have qualifiers.
        }
    }
}
```

***

### Examples
* Sample data
```python3
[
    {
        'type':['friends'],
        'name':['daniel'],
        'phone':['01012345678'],
        'age':['26'],
        'trash':['heheheheheeeaa']
    },
    {
        'type':['business'],
        'name':['franklin'],
        'phone':['01098765432'],
        'age':['31'],
        'trash':['rororororrrror']
    },
]
```

* Script
```python3
from hahaHba import hahaSavor
from jSona import jSona
import os

if __name__=="__main__" :
    TOOL_PATH = 'hahatools.json'
    DATA_PATH = 'sample_data.json'

    jSona().saveJson(TOOL_PATH, TOOL)
    jSona().saveJson(DATA_PATH, DATA)
    
    hs = hahaSavor(TOOL_PATH)
    hs.reset() # set comment if you don't want reset.
    hs.store(DATA_PATH)
```
* Outputs
```python
SAVE SUCCESS TO [ hahatools.json ]
SAVE SUCCESS TO [ sample_data.json ]
HBase Connection Success [localhost:9090]
Delete table table_friends success.
Create table table_friends success.
Delete table table_business success.
Create table table_business success.
100%|██████████████████████████████████████████| 2/2 [00:00<00:00, 44.12it/s]
```

* Check tables by hbase shell
```
hbase(main):001:0> scan 'table_friends'
ROW                      COLUMN+CELL                                                        
 D@64MMOOKD              column=i:a, timestamp=1593165902246, value=26                      
 D@64MMOOKD              column=i:c, timestamp=1593165902246, value=D@64MMOOKD              
 D@64MMOOKD              column=i:h, timestamp=1593165902246, value=1                       
 D@64MMOOKD              column=i:p, timestamp=1593165902246, value=01012345678             
 D@64MMOOKD              column=n:daniel, timestamp=1593165902246, value=1                  
1 row(s)
Took 0.0288 seconds                                                                         
hbase(main):002:0> scan 'table_business'
ROW                      COLUMN+CELL                                                        
 7O4AOMMKKP              column=i:a, timestamp=1593165902255, value=31                      
 7O4AOMMKKP              column=i:c, timestamp=1593165902255, value=7O4AOMMKKP              
 7O4AOMMKKP              column=i:h, timestamp=1593165902255, value=1                       
 7O4AOMMKKP              column=i:p, timestamp=1593165902255, value=01098765432             
 7O4AOMMKKP              column=n:franklin, timestamp=1593165902255, value=1                
1 row(s)
Took 0.0228 seconds
```
***


### Notices

###### Unauthorized distribution and commercial use are strictly prohibited without the permission of the original author and the related module.
