META = {
    'SAVOR':{
        'SPECIAL':{
        },
        'TRASH':[]
    },
    'TABLE':{
        'REF'   :'',
        'PREFIX':'',
        'ROW':{
            'KEY':{
                'MATERIAL':[],
                'FUNC':'hashXOR'
            },
        },
        'IDS':[
        ],
        'COLUMN':{
            'FAMILIES' : {
            },
            'QUALIFIERS' : {
            },
            'RAW_FAM' : []
        }
    }
}

if __name__=="__main__" :
    from jSona import jSona
    import os
    SAVE_PATH = os.path.join('./', 'haha_meta.json')
    jSona().saveJson(SAVE_PATH, META)