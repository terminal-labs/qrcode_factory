#!/usr/bin/env python
#########################################
# This is a simple tool to create a qrcode with an embedded image
# overlayed over it's center. All image manipulation is done in svg
# format to preserve resolutions.
#
# Current values are hardcoded for my particular use case. The only
# currently used value that may be hard to genrealize is the embedded
# image itself. SVGs can encode image sizes in a number of ways. This
# does not handle all ways of specifying image sizes.
#########################################

import segno
import svgutils.transform as sg
import svgwrite

# Initial vars
module_color = "#000000"
background_color = "#2F9A41"
scale_factor = 10 # Scale so that SVG output logo isn't pixelated.

# Create base QR Code
qr = segno.make('http://goo.gl/aVZvN1', micro=False, error='H')
qr.save('qrcode.svg', color=module_color, background=background_color)
fig_qr = sg.fromfile('qrcode.svg')
qr_size = float(fig_qr.get_size()[0]) # only grab first size because it's a square
middle = (qr_size*scale_factor)/2 # typically not an integer

# Load image to embedd in the center
fig_logo = sg.fromfile('logo.svg')
# Following line needs to be more robust for arbitrary SVGs.
logo_size = float(fig_logo.root.get('viewBox').split()[2]) # only grab first size because it's a square

# Create embedded image's solid background. It will provide a 1 module ("pixel") wide margin in all directions.
logo_box_size = 9*scale_factor # must represent an odd number of modules since qr code lengths are odd modules long.
fig_background = svgwrite.Drawing('background.svg', size=(logo_box_size, logo_box_size))
fig_background.add(fig_background.rect(insert=(0,0), size=(logo_box_size, logo_box_size), fill=module_color))
fig_background.save()
fig_background = sg.fromfile('background.svg')

### Creating plots to be combined into final SVG
## Create QR code plot
plot_qr = fig_qr.getroot()
plot_qr.moveto(0, 0, scale=scale_factor)

## Create background plot
# Create a solid background behind the logo, extending such that there
# is one whole pixel of background in the margin around the logo
plot_background = fig_background.getroot()
background_translation = middle - logo_box_size/2 # center the background
plot_background.moveto(background_translation, background_translation)

## Create logo plot
plot_logo = fig_logo.getroot()
logo_translation = middle - 7*scale_factor/2 # center the logo
# Scale to fit logo in a 7 module wide box in the center.
plot_logo.moveto(logo_translation, logo_translation, scale=(7*scale_factor)/logo_size)

## Combine plots into single SVG
fig = sg.SVGFigure(qr_size*scale_factor, qr_size*scale_factor)
fig.append([plot_qr, plot_background, plot_logo]) # Order Matters. First is lowest z-index.
fig.save("qrcode_with_logo.svg")
