
# DumbGDrive

This is a dumb G-Drive hook-in designed to be, first and foremost, scriptable.
If you want to implement a command-line hook, be my guest, and I set it up so you can do so, but I don't want to 
go through the effort.

I use the Google Client Library for Python and install that in a container environment. 

To install on Mox, use Singularity to pull it in the directory you want to install to and use my Client ID file for authorization

```shell script
module load singularity
singularity pull dumbgdrive docker://mccoygroup/dumbgdrive:latest
mkdir -p gdrive
cp /gscratch/stf/b3m2a1/client_id.json ./gdrive/
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
./dumbgdrive --script=<path_to_script>.py
```

everything needs to be relative to `$PWD`, though, or else you'll need to pass other args to Singularity


