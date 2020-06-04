import happybase
import traceback
import pprint
pp = pprint.pprint
from thriftpy2.thrift import TApplicationException

class hahaHba :
    def __init__(self, host='localhost', port=9090) :
        self.host = host
        self.port = port
        self.available = False
        self.connect()
    
    def connect(self) :
        try :
            self.conn = happybase.Connection(host=self.host, port=self.port)
            self.conn.open()
            self.available = True
        except Exception as e :
            self.error(e, "CONNECT")
        else :
            print("HBase Connection Success [{}:{}]".format(self.host, self.port))

    def exists(self, name) :
        if not self.available : self.error('Server not exist.', 'SERVER'); return False
        try :
            tables = self.conn.tables()
            return name.encode() in tables
        except Exception as e :
            self.connect()
            self.error(e, 'GET TABLES')
            return False

    # fam : column familles
    def create_table(self, name, fams) :
        try :
            if self.exists(name) : raise Exception("Table {} already exists.".format(name))
            self.conn.create_table(name, fams)
        except Exception as e :
            self.error(e, 'CREATE TABLE')
        else :
            print("Create table {} success.".format(name))

    def delete_table(self, name) :
        try :
            if not self.exists(name) : raise Exception("Table {} not exists.".format(name))
            self.conn.delete_table(name, disable=True)
        except Exception as e :
            self.error(e, "DELETE TABLE")       
        else :
            print("Delete table {} success.".format(name))

    def checkData(self, data) :
        if type(data) == type(dict()) :
            for ckey in list(data.keys()) :
                if ":" not in ckey : return False
            return True
        return False

    # rkey : Row key
    # data : Data, that should be dictionary type like {'fams:col':'contents'}
    def put(self, name, rkey, data, debug=False) :
        try :
            if not self.exists(name)    : raise Exception("Table {} not exists.".format(name)) 
            if not self.checkData(data) : raise Exception("Wrong data format")
            table = self.conn.table(name)
            if table.rows([rkey])   :   
                                        if debug : print("{} already exists in table {}".format(rkey, name))
            else                    :   table.put(rkey, data)
        except Exception as e :
            self.error(e, "PUT")       
        else :
            if debug : print("\nPut data {} into table {} success.".format(rkey, name))
            pass

    def pop(self, name, rkey) :
        try :
            if not self.exists(name)    : raise Exception("Table {} not exists.".format(name)) 
            table = self.conn.table(name)
            table.delete(rkey)
        except Exception as e :
            self.error(e, "POP")       
        else :
            print("Pop data {} from table {} success.".format(rkey, name))

    # row_start=None, row_stop=None, row_prefix=None, columns=None, filter=None, timestamp=None, include_timestamp=False, 
    # batch_size=1000, scan_batching=None, limit=None, sorted_columns=False, reverse=False
    def scan(self, name, row_prefix=None, columns=None, filters=None) :
        try :
            if not self.exists(name)    : raise Exception("Table {} not exists.".format(name))
            table = self.conn.table(name)
            return {k:v for k,v in table.scan(row_prefix=row_prefix, columns=columns, filter=filters)}
            
        except Exception as e :
            self.error(e, "SCAN")       
            return {}

    def rows(self, name, rows) :
        try :
            if not self.exists(name)    : raise Exception("Table {} not exists.".format(name))
            table = self.conn.table(name)
            return {k:v for k,v in table.rows(rows=rows)}
            
        except Exception as e :
            self.connect()
            self.error(e, "ROWS")       
            return None

    def error(self, e, msg="", ex=False, cry=False) :
        if type(e) == type(TApplicationException()) :
            print("\nERROR {} : {}\n".format(msg, "TApplicationException"))
        else :
            print("\nERROR {} : {}\n".format(msg, e))
        if cry : traceback.print_exc(); print("\n")
        if ex  : exit()
        
        
if __name__=="__main__" :
    hh = hahaHba("localhost", 9090)
    # pp(hh.scan("clo_tabl_shirt", row_prefix=None, filters="PrefixFilter('GwIPCxAfNi4X') AND PrefixFilter('GwI')"))
    pp(hh.scan("clo_tabl_shirt", row_prefix=None, filters="QualifierFilter(=,'substring:black')"))