TOOL = {
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

DATA = [
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

from hahaHba import hahaSavor
from jSona import jSona
import os

if __name__=="__main__" :
    TOOL_PATH = 'hahatools.json'
    DATA_PATH = 'sample_data.json'

    jSona().saveJson(TOOL_PATH, TOOL)
    jSona().saveJson(DATA_PATH, DATA)
    
    hs = hahaSavor(TOOL_PATH)
    # hs.reset() # set comment if you don't want reset.
    hs.store(DATA_PATH)