#!/usr/bin/env python3
#coding=utf-8

"""
Copyright (C) 2022 Plato Mavropoulos
"""

import os
import subprocess

from common.path_ops import project_root, safe_path
from common.system import get_os_ver
from common.system import printer

# Get 7-Zip path
def get_szip_path():
    exec_name = '7z.exe' if get_os_ver()[1] else '7zzs'
    
    return safe_path(project_root(), ['external',exec_name])

# Check 7-Zip bad exit codes (0 OK, 1 Warning)
def check_bad_exit_code(exit_code):
    if exit_code not in (0,1):
        raise Exception(f'BAD_EXIT_CODE_{exit_code}')

# Check if file is 7-Zip supported
def is_szip_supported(in_path, padding=0, check=False, silent=False):
    try:
        szip_t = subprocess.run([get_szip_path(), 't', in_path, '-bso0', '-bse0', '-bsp0'], check=False)
        
        if check: check_bad_exit_code(szip_t.returncode)
    except:
        if not silent:
            printer(f'Error: 7-Zip could not check support for file {in_path}!', padding)
        
        return False
    
    return True

# Archive decompression via 7-Zip
def szip_decompress(in_path, out_path, in_name, padding=0, check=False, silent=False):
    if not in_name: in_name = 'archive'
    
    try:
        szip_x = subprocess.run([get_szip_path(), 'x', '-aou', '-bso0', '-bse0', '-bsp0', '-o' + out_path, in_path], check=False)
        
        if check: check_bad_exit_code(szip_x.returncode)
        
        if not os.path.isdir(out_path): raise Exception('EXTRACT_DIR_MISSING')
    except:
        if not silent:
            printer(f'Error: 7-Zip could not extract {in_name} file {in_path}!', padding)
        
        return 1
    
    if not silent:
        printer(f'Succesfull {in_name} decompression via 7-Zip!', padding)
    
    return 0
