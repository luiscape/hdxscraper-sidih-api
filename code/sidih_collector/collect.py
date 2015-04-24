#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import json
import requests
import scraperwiki
from utilities.prompt_format import item
from utilities.store_records import StoreRecords

def BuildQueryString(id):
  '''Building query strings based on a SIDIH indicator id.'''

  #
  # Building query string and making query.
  # 
  print '%s Collecting indicator id: %s' % (item('prompt_bullet'), str(id))
  u = 'http://sidih.salahumanitaria.co/sissh/api/dato_sector.php?user=siconpaz&password=s1conpaz&ID_DATO=' + str(id) + '&ACTUALIZACION=1950-1-1';
  r = requests.get(u)

  #
  # Checking status of the request.
  #
  if r.status_code == requests.codes.ok:
    data = r.json()[str(id)]
    return data

  else:
    print '%s The SIDIH server returned an error status code.' % item('prompt_error')
    return False


def Main(verbose=False):
  '''Wrapper.'''

  #
  # List of indicators to download.
  #
  indicators = [642, 653, 654, 593, 587, 3, 190, 504, 495, 343, 322, 337, 545, 384, 664, 645, 541, 540, 684, 588]
  # indicators = [322]
  for indicator in indicators:
    data = BuildQueryString(indicator)
    print '%s Processing data for `%s`' % (item('prompt_bullet'), data['metadato']['NOM_DATO'].encode('utf-8'))

    #
    # Error handler for the processing.
    #
    errors = []
    try:
      table_name = 'sidih_' + str(indicator)
      StoreRecords(data=data['valores'], table=table_name, schema='sidih_schema')
      StoreRecords(data=data['valores'], table="all_data", schema='sidih_schema')

    except Exception as e:
      errors.append(indicator)
      print '%s Indicator %s failed to process.' % (item('prompt_bullet'), str(indicator))
      if verbose:
        print e

  #
  # Pretty printing summary.
  #
  n_success = len(indicators) - len(errors)
  print '%s Successfully collected %s indicators from SIDIH.' % (item('prompt_success'), str(n_success))
  if len(errors) > 0:
    print '%s %s indicators failed to collect: %s.' % (item('prompt_warn'), str(len(errors)), errors)
  return True


if __name__ == '__main__':

  try:
      Main()
      print "SW Status: Everything seems to be just fine."
      scraperwiki.status('ok')

  except Exception as e:
      print e
      scraperwiki.status('error', 'Error collecting data.')
      os.system("mail -s 'SIDIH API: Failed collecting data.' luiscape@gmail.com")
