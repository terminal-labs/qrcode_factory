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

import segno
import svgutils.transform as sg
import svgwrite ##TODO use this to replace svgutils

class QRFactory:
    def __init__(self, logo=None, to_encode=None, module_color="#000000", background_color="#FFFFFF", scale_factor=10):
        '''Create a qrcode with a logo.

        Encode data  as an svg and overlay a logo with a matte backdrop on
        top of it to produce a final qr code svg with a logo.

          - **parameters**, **types**, **return** and **return types**::

        :param logo: logo svg as a string
        :param to_encode: data to be encoded as a qr code
        :param module_color: color of the svg module data (lighter color usually)
        :param background_color: color of the svg module data and logo matte background (darker color usually)
        :param scale_factor: Resolition to upscale the qrcode to so that the logo doesn't look pixelated by contrast
        :type logo: str
        :type to_encode: str
        :type module_color: str
        :type background_color: str
        :type scale_factor: int
        :return: Final svg as string if imported, None if ran from shell
        :rtype: str if imported, None if ran from the shell
        '''
        self.module_color = module_color
        self.background_color = background_color
        self.scale_factor = scale_factor

        if to_encode is not None: # Make base qr code
            self.base_qr_code(to_encode)

        if logo is not None and to_encode is not None: # put logo on qrcode
            self.logo(logo)
            self.create_plots()

    def base_qr_code(self, to_encode):
        ## Create base QR Code
        self.QRsvg = io.BytesIO()
        qr = segno.make(to_encode, micro=False, error='H')
        # saving base qr code to StringIO buffer
        qr.save(self.QRsvg, color=self.module_color, background=self.background_color, kind='svg')
        self.fig_qr = sg.fromstring(self.QRsvg.getvalue())
        self.qr_size = float(self.fig_qr.get_size()[0]) # only grab first size because it's a square
        self.middle = (self.qr_size*self.scale_factor)/2 # typically not an integer

    def logo(self, logo):
        ## This method will create the small background image that goes
        ## behind the logo, effectilly a matte. We needed it for our logo
        ## but it may not be necessary for MVP of site. Something we
        ## could add later as it is probably one of the trickyer things
        ## to generalize.


        ## Load image to embed
        # TODO: Surround this line with a try/except to prove the sting is a n SVG (XMLSyntaxError?)
        self.fig_logo = sg.fromstring(logo)
        # TODO: Following line needs to be more robust for arbitrary SVGs.
        self.logo_size = float(self.fig_logo.root.get('viewBox').split()[2]) # only grab first size because it's a square

        ## Create embedded image's solid background. It will provide
        ## a 1 module ("pixel") wide margin in all directions.
        self.logo_box_size = 9*self.scale_factor # must represent an odd number of modules since qr code lengths are odd modules long.
        fig_background = svgwrite.Drawing(filename='noname.svg', size=(self.logo_box_size, self.logo_box_size))
        fig_background.add(fig_background.rect(insert=(0,0), size=(self.logo_box_size, self.logo_box_size), fill=self.module_color))
        self.fig_background = sg.fromstring(fig_background.tostring()) # patch data from svgwrite to svgutils

    def create_plots(self): #TODO: Not sure this method and output_qr should be separate. Consider condsolidating.
        ### Creating plots to be combined into final SVG
        ## Create QR code plot
        self.plot_qr = self.fig_qr.getroot()
        self.plot_qr.moveto(0, 0, scale=self.scale_factor)

        ## Create background plot
        if (self.fig_logo and self.fig_background): # if no logo is set, don't embed one (or it's background)
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
        if (self.plot_logo and self.plot_background): # Logo and background are set
            fig.append([self.plot_qr, self.plot_background, self.plot_logo]) # Order Matters. First is lowest z-index.
        else:
            fig.append(self.plot_qr) # Just a qr code
        return fig.to_str() # Can only save to a file or be cast into a string


if __name__ == '__main__':
    ##TODO: allow for inputting data via command args instead of hardcoded defaults.
    logo = open("logo.svg").read()
    to_encode = "http://goo.gl/aVZvN1"
    qr = QRFactory(logo, to_encode, background_color="#2F9A41")
    open("qrcode_with_logo.svg", "w+").write(qr.output_qr())
