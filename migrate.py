import argparse
from copy import deepcopy
import glob
import subprocess
import sys
import zipfile
from pathlib import Path
import os.path as path
import json


success = 0
overwrite = False

win=mac=False
if sys.platform.startswith("darwin"):mac=True
elif sys.platform.startswith("win"):win=True

def copyWithSubprocess(cmd):
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def copy_file(src, dist):
    global success
    
    cmd=None
    if mac: cmd=['cp', src, dist]
    elif win: cmd=['xcopy', src, dist, f'/Y{"" if overwrite else "/D"}']

    if cmd:
        copyWithSubprocess(cmd)
        success += 1
        print(f"Success copy {src}")

def process(src_folder, dist_folder):
    with open('output.json', 'r', encoding='utf-8') as f:
        dependencies = set(json.load(f))
        missing = deepcopy(dependencies)
        dependencies_without_ver = [x[:-7] for x in dependencies if x.endswith('.latest')]
        not_used = {}

        all_len = len(dependencies)
        files = glob.glob(path.normpath(src_folder) + "/**/*.var", recursive=True)
        for i in files:
            try:
                d = Path(i).stem
                ver = int(d.split('.')[-1])
                if d in dependencies:
                    copy_file(i, dist_folder)
                    if d in missing:
                        missing.remove(d)
                else:
                    name_without_ver = Path(d).stem
                    if ver > not_used.get(name_without_ver, [0, ''])[0]:
                        not_used[name_without_ver] = [ver, i]
            except Exception as e:
                print("VAR: "+i+" [ERROR] "+str(e)+"[ERROR]")
        print('========= process latest =========')
        # latest version
        for k, [_, file] in not_used.items():
            if k in dependencies_without_ver:
                copy_file(file, dist_folder)
                missing.remove(k+'.latest')
        print(f"========= Success: {success}/{all_len} =========")
        json.dump(list(missing), open('missing.json', 'w', encoding='utf-8'), indent=4)
        print(f"========= {len(missing)} Missing dependencies were been output to missing.json =========")

if __name__ == '__main__':
    parser = argparse.ArgumentParser('python3 migrate.py', description='migrate your dependencies from folder to vam,base to output.json')
    
    parser.add_argument('-s', help='folder that contains all your dependencies files (can be nest)', required=True)
    parser.add_argument('-d', help='folder that you want your dependencies place in (for example: /path/to/vam/AddonPackages)', required=True)
    parser.add_argument('-o', help='overwrite dist if existed, default is False', default=False, action='store_true')

    args = parser.parse_args()
    if args.o:
        overwrite = True
    process(args.s, args.d)