#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import scraperwiki
from utilities import prompt_format as I

def StoreRecords(data, schema, table, verbose = True):
  '''Store records in a ScraperWiki database.'''

  schemas = {
    'sidih_schema': ["ID_VALDA", "FIN_VALDA", "INI_VALDA", "ID_DATO", "ID_UNIDAD", "ID_MUN", "VAL_VALDA", "ID_DEPTO"]
  }

  try:
    schema = schemas[schema]

  except Exception as e:

    if verbose:
      print e
      return False

    else: 
      print "%s select one of the following tables: 'funnel', 'metrics', or '_log'." % I.item('prompt_error')
      return False


  ## See if record already exists.
  def recordExists(record):

    ## TODO: navigate the schema properly.
    
    sql_statement = 'SELECT COUNT (' + schema[0] + ') FROM ' + table + ' WHERE ' + schema[0] + '=' + '"' + record[schema[0]] + '"' + ' AND ' + schema[1] + '=' + '"' + record[schema[0]] + '"'
    
    try:
      query = scraperwiki.sqlite.execute(sql_statement)
      return query["data"][0][0] > 0

    except Exception as e:
      print e
      return

  
      
  def recordDelete(record):
    sql_statement = 'DELETE FROM ' + table + ' WHERE ' + schema[0] + '=' + '"' + record[schema[0]] + '"' + ' AND ' + schema[1] + '=' + '"' + record[schema[1]] + '"'

    try:
      query = scraperwiki.sqlite.execute(sql_statement)

    except Exception as e:
      print e


  exist = 0
  not_exist = 0
  for record in data:

    if recordExists(record) is True:
      recordDelete(record)
      exist =+ 1

    else: 
      not_exist =+ 1

    scraperwiki.sqlite.save(schema, record, table_name=table)


  # Printing summary of operation.
  if not_exist > 0:
    if verbose:
      print "%s Storing %s record(s) in database, %s." % (I.item('prompt_bullet'), not_exist, table)

  if exist > 0:
    print "%s %s records already exists in database, %s. Updated." % (I.item('prompt_bullet'), exist, table)

  return True


if __name__ == '__main__':
  StoreRecords()