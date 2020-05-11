

from ..CLI import CLI
from ..Request import Uploader
import os

params = CLI.get_parse_dict(
    (
        "dir",
        dict(
            default="", type=str,
            help="Directory to upload"
        )
    )
)

d = params['dir']
dirname = os.path.basename(d)
for f in os.listdir(d):
    file = os.path.join(d, f)
    print('Uploaded {file} to {name} (id={id})'.format(
        file=file,
        **Uploader(file, folder=dirname).upload()
    ))