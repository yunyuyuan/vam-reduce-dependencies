> This project is used to reduce VAM AddonPackages size.

## Features
* **main.py**: generate all missing dependencies of a folder that contains .var files(include its subfolders), output to `output.json`
* **migrate.py**: walk through a folder(include its subfolders), if some .var file is in `output.json`, then copy it to VAM AddonPackages.


## Step 0
Make sure you have python3.11 installed.

## Step 1
rename `/path/to/vam/AddonPackages` to `/path/to/vam/AddonPackages-backup`

## Step 2
create a new empty folder `/path/to/vam/AddonPackages`

## Step 3
move all **your favorite** .var files from `/path/to/vam/AddonPackages-backup` to `/path/to/vam/AddonPackages`

## Step 4
generate a `output.json` file(contains all necessary dependencies that **your favorite** .var files need) for your favorite `.var` files.
```sh
python .\main.py -f "/path/to/vam/AddonPackages"
```

## Step 5
copy all necessary dependencies from AddonPackages-backup to the AddonPackages folder, base on the `output.json` file.
```sh
python .\migrate.py -s "/path/to/vam/AddonPackages-backup" -d "/path/to/vam/AddonPackages"
```

## Step 6
rerun `step 5 and step 6` until the output.json is empty or small(that means all dependencies you have were processed, rest in output.json are some dependencies you don't have).

## Step 7
delete `/path/to/vam/AddonPackages`