
# DumbGDrive

This is a dumb G-Drive hook-in designed to be, first and foremost, scriptable.
If you want to implement a command-line hook, be my guest, and I set it up so you can do so, but I don't want to 
go through the effort.

I use the Google Client Library for Python and install that in a container environment. 

## Getting Started

To install on Mox, use Singularity to pull it in the directory you want to install to. 
If you want to use my Client ID file for authorization, feel free. Otherwise it's really easy to get your own. My credentials only work for `...@uw.edu` accounts.

```shell script
module load singularity
singularity pull dumbgdrive docker://mccoygroup/dumbgdrive:latest
mkdir -p gdrive
cp /usr/lusers/b3m2a1/client_id.json ./gdrive/
```

You can then run it in interactive mode

```shell script
./dumbgdrive
# DumbGDrive Interactive Session
# >>> files_api = Files()
# >>> files_api.list()
# [{'kind': 'drive#file', 'id': '0B36y0W6EYg39c3RhcnRlcl9maWxl', 'name': 'Getting started', 'mimeType': 'application/pdf'}]
```

or in script mode

```shell script
./dumbgdrive --script <path_to_script>.py <script_args>
```

everything needs to be relative to `$PWD`, though, or else you'll need to pass other args to Singularity

## Writing Scripts

Rather than document how to do things, [here's a link to Google's own documentation](https://developers.google.com/drive/api/v3/about-files)

Anything you want to do can be done from there, first probably by building a `Service` object or using the `Files` one I provide. 
Look at the source to see how the `list` method is written and compare that to what's [here](https://developers.google.com/drive/api/v3/quickstart/python).

If you have a script you want to add as a method to a service, feel free to add it and submit a PR. 
If you want to contribute a default script to put in the `scripts`, folder, that's cool too.
I'm not taking requests for extensions at this moment, though.

The scripts in the scripts can serve as good examples, e.g.

```shell script
dumbgdrive --script find_files.py --pageSize=1
# {'id': '1IODSf2B4Gd-uaec8dBQemDx_H2b_aGy5JyjS-XHefVY', 'name': 'Chem 162 Online Resource Collection'}
```

## Extensions

One thing that would be really nice to have is higher-level interfaces, i.e. things like a `File` class or `Drive` class which can be returned by things like `FilesService.list()` and which can do stuff like `file.download(<path>)` or be returned by a `File.upload(file)` classmethod constructor.

If anyone wants to write this, I'd appreciate it. 
