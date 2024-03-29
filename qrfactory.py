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
import copy # to fix bug where fig_qr seems corrupted by fig_qr.getroot()

import segno
import svgutils.transform as sg
import svgwrite ##TODO refactor to use this to replace svgutils if possible

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
        self.logo = logo
        self.to_encode = to_encode

        if to_encode is not None: # We have data to encode, save qr data
            self.build_qrcode(self.to_encode)

        if logo is not None and to_encode is not None: # Save logo data
            self.build_logo(self.logo)

    def build_qrcode(self, to_encode=None, module_color=None, background_color=None, scale_factor=None):
        '''Create base QR Code'''
        if not (self.to_encode or to_encode): # If we have no data, we can't do anything.
            return

        # If any data has changed, save it.
        if to_encode:
            self.to_encode = to_encode
        if module_color:
            self.module_color = module_color
        if background_color:
            self.background_color = background_color
        if scale_factor:
            self.scale_factor = scale_factor

        self.QRsvg = io.BytesIO()
        self.qr = segno.make(self.to_encode, micro=False, error='H')
        # saving base qr code to StringIO buffer
        self.qr.save(self.QRsvg, color=self.module_color, background=self.background_color, kind='svg')
        self.fig_qr = sg.fromstring(self.QRsvg.getvalue())
        self.qr_size = float(self.fig_qr.get_size()[0]) # only grab first size because it's a square
        self.middle = (self.qr_size*self.scale_factor)/2 # typically not an integer
        # print(self.qr_size)

    def build_logo(self, logo):
        '''This method will create the small background image that goes
        behind the logo, effectilly a matte. We needed it for our logo
        but it may not be necessary for MVP of site. Something we
        could add later as it is probably one of the trickier things
        to generalize.
        '''
        self.logo = logo
        ## Load image to embed
        # TODO: Surround this line with a try/except to prove the sting is an SVG (XMLSyntaxError?)
        self.fig_logo = sg.fromstring(self.logo.encode())
        # TODO: Following line needs to be more robust for arbitrary SVGs.
        self.logo_size = self._svg_size(self.fig_logo)

        ## Create embedded image's solid background. It will provide
        ## a 1 module ("pixel") wide margin in all directions.
        self.logo_box_size = 9*self.scale_factor # must represent an odd number of modules since qr code lengths are odd modules long.
        fig_background = svgwrite.Drawing(filename='noname.svg', size=(self.logo_box_size, self.logo_box_size))
        fig_background.add(fig_background.rect(insert=(0,0), size=(self.logo_box_size, self.logo_box_size), fill=self.module_color))
        self.fig_background = sg.fromstring(fig_background.tostring()) # patch data from svgwrite to svgutils

    def _svg_size(self, svg):
        # Look for a hieght and width, and return the larger of the two.
        if svg.root.get('viewBox'):
            view = 'viewBox'
        elif svg.root.get('viewbox'):
            view = 'viewbox'
        else:
            view = False
        if view:
            width = float(svg.root.get(view).split()[2])
            height = float(svg.root.get(view).split()[3])
        size = max(width, height)
        return size

    def _create_plots_qr(self):
        '''Creating qr plot for final SVG'''
        # deepcopy used to fix bug where svgutil clobbers contents on getroot
        local_fig_qr = copy.deepcopy(self.fig_qr) # copy fig
        self.plot_qr = self.fig_qr.getroot()
        self.fig_qr = local_fig_qr # reset fig after clobbering
        self.plot_qr.moveto(0, 0, scale=self.scale_factor)

    def _create_plots_logo(self):
        '''Creating logo and background plots to be combined into final SVG'''
        ## Create background plot
        # Create a solid background behind the logo, extending such that there
        # is one whole pixel of background in the margin around the logo.
        # deepcopy used to fix bug where svgutil clobbers contents on getroot.
        local_fig_background = copy.deepcopy(self.fig_background) # copy fig
        self.plot_background = self.fig_background.getroot()
        self.fig_background = local_fig_background # reset fig after clobbering
        background_translation = self.middle - self.logo_box_size/2 # center the background
        self.plot_background.moveto(background_translation, background_translation)

        ## Create logo plot
        # deepcopy used to fix bug where svgutil clobbers contents on getroot
        local_fig_logo = copy.deepcopy(self.fig_logo) # copy fig
        self.plot_logo = self.fig_logo.getroot()
        self.fig_logo = local_fig_logo # reset fig after clobbering
        logo_translation = self.middle - 7*self.scale_factor/2 # center the logo
        # Scale to fit logo in a 7 module wide box in the center.
        self.plot_logo.moveto(logo_translation, logo_translation, scale=7*self.scale_factor/self.logo_size)

    def output_qr(self):
        '''Combine plots into single SVG'''
        try:
            self._create_plots_qr()
        except AttributeError as e: # We never got data to encode, and never produced a qrcode. Nothing to ouput.
            return None

        fig = sg.SVGFigure(self.qr_size*self.scale_factor, self.qr_size*self.scale_factor)

        try: # Logo and background are set
            self._create_plots_logo()
            fig.append([self.plot_qr, self.plot_background, self.plot_logo]) # Order Matters. First is lowest z-index.
        except AttributeError as e: # We never got a logo svg, just ouput a qr code.
            fig.append(self.plot_qr) # Just a qr code
        return fig.to_str() # Can only save to a file or be cast into a string


if __name__ == '__main__':
    '''Build a qrcode with a logo inside it'''
    ##TODO: allow for inputting data via command args instead of hardcoded defaults.
    with open("logo.svg") as fp:
        logo = fp.read()
    to_encode = "trml.io"
    background_color = "#2F9A41"
    qrcode = QRFactory(logo, to_encode, background_color=background_color)
    with open("qrcode_with_logo.svg", "wb") as fp:
        fp.write(qrcode.output_qr())
