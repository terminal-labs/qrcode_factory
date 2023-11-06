# qrcode

This is a simple python script meant to be run from the cli, that takes a logo in svg format, and overlays the logo on top of the svg, in it's center. Exact parameters are hard-coded in the script. This was made to serve Terminal Labs's own need, so we didn't put much effort into generalizing this. But you should be able to alter the hard-coded paramters and starting files to match your need.

## Install

To use, without changing anything create an environment with the needed requirements. You can either:

```shell
# Activate/install python 3.11.6 through any means
pip install -r requirements.lock
```

or, if you have Rye installed:

```shell
rye pin 3.11.6
rye sync
```

This is not compatible with Python 3.12 at this time.

## Use

```shell
python qrfactory.py
```

Will run, out of the box, and generate a readable QR code with the TL logo in the center, pointing to a shortened url that forwards to terminallabs.com.

To customize this, you can:

- swap out the logo for any other square svg
- change the data that's encoded into the QR code, currently living at `to_encode = "http://goo.gl/aVZvN1"` in the script
- change the background color, currently living at `background_color = "#2F9A41"`

Note that the longer the encoded string is, the more complex the QR code is.
