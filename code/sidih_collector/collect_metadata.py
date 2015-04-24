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

def Main(csv_path):
  #
  # List of indicators to download.
  #
  indicators = [642, 653, 654, 593, 587, 3, 190, 504, 495, 343, 322, 337, 545, 384, 664, 645, 541, 540, 684, 588]
  for indicator in indicators:
    data = BuildQueryString(indicator)

  #
  # Storing CSV.
  #
  with open(csv_path, 'wb') as test_file:
  csv_writer = csv.writer(test_file)
  for y in range(length):
      csv_writer.writerow([ x[y] for x in data['metadatos'] ])


if __name__ == '__main__':
  Main(csv_path)
