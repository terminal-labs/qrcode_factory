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
import io
import StringIO

import segno
import svgutils.transform as sg
import svgwrite ##TODO use this to replace svgutils

class QRFactory:
    def __init__(self, module_color=None,background_color=None,scale_factor=None):
        self.module_color = module_color if module_color else "#000000"
        self.background_color = background_color if background_color else "#2F9A41"
        self.scale_factor = scale_factor if scale_factor else 10 # Scale so that SVG output logo isn't pixelated.

    def input_for_encoding(self,to_encode):
        ## Create base QR Code
        self.QRsvg = io.BytesIO()
        qr = segno.make(to_encode, micro=False, error='H')
        qr.save(self.QRsvg, color=self.module_color, background=self.background_color, kind='svg')
        # outputting base qr code to StringIO buffer
    def base_qr_code(self):
        self.fig_qr = sg.fromstring(self.QRsvg.getvalue())
        self.qr_size = float(self.fig_qr.get_size()[0]) # only grab first size because it's a square
        self.middle = (self.qr_size*self.scale_factor)/2 # typically not an integer

    def input_logo(self,logo=None):
        ## TODO assure that input is BytesIO
        ## Load image to embed
        self.fig_logo = sg.fromstring(logo.getvalue())

    def config_logo(self):
        ## This method will create the small background image that goes behind the logo, effectilly a matte. We needed it for our logo
        ## But it may not be necessary for MVP of site. Something we could add later as it is probably one of the trickyer things to generalize.
        # TODO: Following line needs to be more robust for arbitrary SVGs.
        self.logo_size = float(self.fig_logo.root.get('viewBox').split()[2]) # only grab first size because it's a square

        ## Create embedded image's solid background. It will provide a 1 module ("pixel") wide margin in all directions.
        self.logo_box_size = 9*self.scale_factor # must represent an odd number of modules since qr code lengths are odd modules long.
        fig_background = svgwrite.Drawing('background.svg', size=(self.logo_box_size, self.logo_box_size))
        fig_background.add(fig_background.rect(insert=(0,0), size=(self.logo_box_size, self.logo_box_size), fill=self.module_color))
        fig_background.save()
        self.fig_background = sg.fromfile('background.svg')

    def create_plots(self):
        ### Creating plots to be combined into final SVG
        ## Create QR code plot
        self.plot_qr = self.fig_qr.getroot()
        self.plot_qr.moveto(0, 0, scale=self.scale_factor)

        ## Create background plot
        # Create a solid background behind the logo, extending such that there
        # is one whole pixel of background in the margin around the logo
        self.plot_background = self.fig_background.getroot()
        background_translation = self.middle - self.logo_box_size/2 # center the background
        self.plot_background.moveto(background_translation, background_translation)

        ## Create logo plot
        self.plot_logo = self.fig_logo.getroot()
        logo_translation = self.middle - 7*self.scale_factor/2 # center the logo
        # Scale to fit logo in a 7 module wide box in the center.
        self.plot_logo.moveto(logo_translation, logo_translation, scale=7*self.scale_factor/self.logo_size)

    def output_qr(self):
        ## Combine plots into single SVG
        fig = sg.SVGFigure(self.qr_size*self.scale_factor, self.qr_size*self.scale_factor)
        fig.append([self.plot_qr, self.plot_background, self.plot_logo]) # Order Matters. First is lowest z-index.
        return fig

def main(logo, to_encode, outfile=None):
    '''Create a qrcode with a logo.

    Encode data  as an svg and overlay a logo with a matte backdrop on
    top of it to produce a final qr code svg with a logo.

      - **parameters**, **types**, **return** and **return types**::

    :param logo: logo svg as io.BytesIO object
    :param to_encode: data to be encoded as a qr code
    :param outfile: name of final svg file to produce
    :type logo: io.BytesIO object
    :type to_encode: str
    :type outfile: str
    :return: Final svg as string if imported, None if ran from shell
    :rtype: str if imported, None if ran from the shell
    '''
    qr = QRFactory()
    qr.input_for_encoding(to_encode=to_encode)
    qr.base_qr_code()
    qr.input_logo(logo)
    qr.config_logo()
    qr.create_plots()
    fig = qr.output_qr()
    if outfile:
        fig.save(outfile) # save file when called via shell
    else:
        return fig.to_str() # return svg as string for general use

if __name__ == '__main__':
    logo = io.BytesIO(open("logo.svg").read())
    main(logo, "http://goo.gl/aVZvN1", "qrcode_with_logo.svg")
