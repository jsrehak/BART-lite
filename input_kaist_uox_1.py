from os import listdir
from os.path import isfile, join

mat_dir = './mat/kaist/' # Location of material files
mats = [mat_dir + f for
        f in listdir(mat_dir) if isfile(join(mat_dir, f))]

layout_mox1 = """
  20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
  20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
  20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
  20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
  aa 20 20 bb bb aa aa 20 20 20 20 20 20 20 20 20 20
  aa 20 20 bb bb aa aa 20 20 20 20 20 20 20 20 20 20
  20 20 20 20 20 20 20 20 20 aa aa 20 20 20 20 20 20
  20 20 20 20 20 20 20 20 20 aa aa 20 20 20 20 20 20
  20 20 20 20 20 20 20 bb bb 20 20 20 20 20 20 20 20
  20 20 20 20 20 20 20 bb bb 20 20 20 20 20 20 20 20
  aa 20 20 20 20 aa aa 20 20 20 20 aa aa 20 20 20 20
  aa 20 20 20 20 aa aa 20 20 20 20 aa aa 20 20 20 20
  20 20 20 bb bb 20 20 20 20 20 20 bb bb 20 20 20 20
  20 20 20 bb bb 20 20 20 20 20 20 bb bb 20 20 20 20
  20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
  20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
  gt 20 20 20 20 aa aa 20 20 20 20 aa aa 20 20 20 20
"""
layout_dict={'20': 'uo2_20',
             'gt': 'guide_tube',
             'aa': 'control_rod',  # Control rod
             #'aa': 'control_rod', # Guide tube
             'bb': 'uo2_20'}       # Fuel
             #'bb': 'ba'}          # Gd BA rod

problem = {
    "sn_order": 6,              # REQ: SN angular quadrature order
    "do_nda": False,            # REQ: to determine whether or not to use NDA
    "do_ua": False,            # REQ: to determine use UA for NDA or not
    "mesh_cells": 34,           # REQ: number of cells per side
    "groups": 7,                # REQ: number of energy groups
    "domain_upper": 10,         # REQ: domain size
    "materials": mats,          # REQ: list of xml material files
    "layout": layout_mox1,      # REQ: material layout to use
    "layout_dict": layout_dict, # REQ: material layout dictionary
    "tr_scatt": True            # OP:  Take transp. of scatt. matrices
}
