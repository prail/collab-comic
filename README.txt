This will grab all images of MIME type image/png and save them to a
directory named entries. (If you don't have one the script will create one for
you.) You can then do your fancy Bash or Powershell scripting on
this directory to upload to your site with the correct filename and
everything.

Dependencies:

pillow and Python 3's standard library.
You can just install the latest version of pillow from pypi and this should
work. Doesn't depend on anything fancy for PIL, only using it to check the
size of images.

Setup:

Create a new file named config.py populate this file with your POP3 server,
username, and password. Use config_example.py as a guide for how your config
file should look.
