import argparse
import glob
import zipfile
from pathlib import Path
import os.path as path
import json

existed_packages = set()
missing_dependencies = set()

def process(folder):
    files = glob.glob(path.normpath(folder) + "/**/*.var", recursive=True)
    for i in files:
        try:
            with zipfile.ZipFile(i) as myzip:
                with myzip.open('meta.json') as meta:
                    try:
                        meta_content = json.loads(meta.read())
                    except Exception as e:
                        print("VAR: "+i+" [ERROR Meta JSON Failed]: "+str(e)+"[ERROR]")
                    else:
                        filename = Path(i).stem
                        existed_packages.add(filename)
                        # also add latest version
                        existed_packages.add(Path(filename).stem+'.latest')
                        dependencies = meta_content.get('dependencies', {})
                        if dependencies:
                            for d in dependencies.keys():
                                missing_dependencies.add(d)
        except Exception as e:
            print("VAR: "+i+" [ERROR] "+str(e)+"[ERROR]")
    output = [x for x in missing_dependencies if x not in existed_packages]
    json.dump(output, open('output.json', 'w'), indent=4)
    print(f"========= Success: {len(output)} =========")

if __name__ == '__main__':
    parser = argparse.ArgumentParser('python3 main.py', description='export your favorite .var\'s dependencies\nSo you can more conveniently manage/delete dependencies')
    
    parser.add_argument('-f', help='folder that contains all your favorite .var(look,clothes,scene except dependencies) files', required=True)

    args = parser.parse_args()
    process(args.f)