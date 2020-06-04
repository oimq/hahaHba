from hahaHba import hahaHba
from jSona import jSona
from Hash import hasHXOR

from tqdm import tqdm
import pprint
pp = pprint.pprint
import traceback

class hahaSavor :
    def __init__(self, meta='hbase_meta.json', haddr='localhost', hport=9090) :
        self.jso  = core()
        self.hh   = core(haddr, hport)
        self.hxor = hashXOR()
        self.meta = self.jso.loadJson(meta) if type(meta)==type("") else meta
        
    def reset(self) :
        for table_id in self.meta['TABLE']['IDS'] :
            if self.hh.exists(self.meta['TABLE']['PREFIX']+table_id) :
                self.hh.delete_table(self.meta['TABLE']['PREFIX']+table_id)
            self.hh.create_table(
                self.meta['TABLE']['PREFIX']+table_id, 
                {cf:{} for cf in self.meta['TABLE']['COLUMN']['FAMILIES'].keys()}
            )

    def error(self, e, msg="", ex=True) :
        traceback.print_exc()
        print("ERROR {} : {}".format(msg, e))
        if ex : exit()

    def generate(self, sources, func) :
        if func == 'hashXOR' : return "".join([self.hxor.digest(source[0], source[1]) for source in sources])

    def special(self, special_dict, refer_fields, supplies={'row_key':'default'}) :
        if set(special_dict.keys())-set(refer_fields.keys()) : raise Exception("Special fields {} can't be referenced.".format(special_dict.keys()))
        sdata = dict()
        for sfield in special_dict :
            if   special_dict[sfield][0] == 'fix' :
                sdata[refer_fields[sfield]] = special_dict[sfield][1]
            elif special_dict[sfield][0] == 'row_key' :
                sdata[refer_fields[sfield]] = supplies['row_key']
        return sdata

    def configuration(self) :
        qualifiers_families = [cq.split(':')[0] for cq in self.meta['TABLE']['COLUMN']['QUALIFIERS'].keys()]
        main_fields = tuple(self.meta['TABLE']['COLUMN']['FAMILIES'][cf] for cf in self.meta['TABLE']['COLUMN']['RAW_FAM'])
        subo_fields = tuple(self.meta['TABLE']['COLUMN']['QUALIFIERS'].values())
        table_refer = self.meta['TABLE']['REF']
        spec_fields = tuple(self.meta['SAVOR']['SPECIAL'].keys())
        trsh_fields = tuple(self.meta['SAVOR']['TRASH'])
        all_fields  = set(main_fields)|set(subo_fields)|set([table_refer])|set(spec_fields)|set(trsh_fields)

        familes    = dict(filter(lambda m : m[1] in main_fields, self.meta['TABLE']['COLUMN']['FAMILIES'  ].items()))
        qualifiers = dict(filter(lambda m : m[1] not in spec_fields and m[1] in subo_fields, self.meta['TABLE']['COLUMN']['QUALIFIERS'].items()))
        specials   = {v:k for k,v in self.meta['TABLE']['COLUMN']['QUALIFIERS'].items() if v in self.meta['SAVOR']['SPECIAL']}

        return qualifiers, main_fields, subo_fields, table_refer, spec_fields, trsh_fields, all_fields, familes, qualifiers, specials

    def store(self, data, options="", cry=True) :
        if type(data)==type("") : data = self.jso.loadJson(data)
        if len(set(['-r', '--reset'])  &set(options.split())) : self.reset()                            # Reset table?
        # if len(set(['-d', '--demo'])   &set(options.split())) : self.meta['TABLE']['PREFIX']+="demo_"   # Demo version?
        # is_vir = len(set(['-v', '--virtual'])&set(options.split()))!=0  # Apply Virtual keypoint?
        try :
            # Get data aligned by fields which are FAMILIES and QUALIFIERS
            qualifiers, main_fields, subo_fields, table_refer, spec_fields, trsh_fields, all_fields, familes, qualifiers, specials = self.configuration()

            if cry : pbar = tqdm(total=len(data))
            for item in data : 
                if set(item.keys()) - all_fields : raise Exception("No match fields \n * savor({}) : \n * data({})\n => {}".format(
                        all_fields, set(data[0].keys()), set(data[0].keys())-all_fields))

                # Create row-key
                row_key = self.generate([(item[f],n) for f,n in self.meta['TABLE']['ROW']['KEY']['MATERIAL']], 
                                        self.meta['TABLE']['ROW']['KEY']['FUNC'])

                # Create basic hata : basic hbase data - RAW_FAM
                hata = dict()
                for cf,field in familes.items() :
                    for value in item[field] : 
                        hata["{}:{}".format(cf, value)] = '1'            
                
                # Append details(qualifiers) to hata
                for cq,field in qualifiers.items() :
                    for value in item[field] : 
                        hata[cq] = str(value)
                
                # Append specials to hata
                hata.update(self.special(self.meta['SAVOR']['SPECIAL'], specials, {'row_key':row_key}))

                # Save to HBASE database
                for table_id in item[table_refer] :
                    self.hh.put(
                        name = self.meta['TABLE']['PREFIX']+table_id,
                        rkey = row_key,
                        data = hata
                    )

                pbar.update(1)
            if cry : pbar.close()
            
        except Exception as e :
            if cry : pbar.close()
            self.error(e, "STORE")
        
import os

if __name__=="__main__" :
    META_PATH = os.path.join('/home/park/myElasticsearch/modules/hahaHba/hahaHba/', 'hbase_meta.json')
    DATA_PATH = os.path.join('/home/park/datasets/zara/datasets/supplied_zara_20200525.json')
    hs = hahaSavor(META_PATH)
    hs.store(DATA_PATH, '')
    # hs.reset()
                
