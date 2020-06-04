## hahaHba

##### Handler for hbase with happybase module

for installing and using, requirements are below : 

* tqdm : https://github.com/tqdm/tqdm

* happybase : https://github.com/python-happybase/happybase

* thrift : https://github.com/Thriftpy/thriftpy2

* Hash : https://github.com/oimq/Hash

######'Very thanks to happybase.'

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

##### hahaMeta

* metadata for hahaHba and hahaSavor

***

### Examples

* Script
```python3
Sorry, we add this later...
```
* Outputs
```python
Sorry, we add this later...
```

***


### Notices

###### Unauthorized distribution and commercial use are strictly prohibited without the permission of the original author and the related module.