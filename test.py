#!/usr/bin/env python
import qrfactory
import unittest

test_qr = '<?xml version=\'1.0\' encoding=\'ASCII\' standalone=\'yes\'?>\n<svg xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" version="1.1" width="330.0" viewbox="0 0 330.0 330.0" height="330.0">\n  <g class="segno" transform="translate(0, 0) scale(10) ">\n    <path fill="#fff" d="M0 0h33v33h-33z"/>\n    <path stroke="#000" class="qrline" d="M4 4.5h7m4 0h2m1 0h2m2 0h7m-25 1h1m5 0h1m1 0h2m1 0h2m2 0h1m2 0h1m5 0h1m-25 1h1m1 0h3m1 0h1m3 0h1m7 0h1m1 0h3m1 0h1m-25 1h1m1 0h3m1 0h1m4 0h1m3 0h2m1 0h1m1 0h3m1 0h1m-25 1h1m1 0h3m1 0h1m2 0h2m2 0h1m4 0h1m1 0h3m1 0h1m-25 1h1m5 0h1m1 0h2m1 0h2m2 0h2m1 0h1m5 0h1m-25 1h7m1 0h1m1 0h1m1 0h1m1 0h1m1 0h1m1 0h7m-17 1h1m2 0h1m4 0h1m-13 1h4m1 0h2m2 0h1m4 0h2m3 0h1m-24 1h1m1 0h4m1 0h2m1 0h1m2 0h1m1 0h1m1 0h1m2 0h2m-21 1h1m1 0h1m2 0h3m1 0h1m1 0h6m1 0h1m1 0h2m-23 1h3m1 0h2m2 0h3m3 0h2m2 0h1m3 0h1m1 0h1m-24 1h2m2 0h2m4 0h5m2 0h2m2 0h1m1 0h1m-25 1h5m2 0h4m3 0h1m1 0h1m1 0h1m1 0h2m1 0h1m-18 1h1m4 0h1m1 0h1m2 0h2m2 0h2m-20 1h1m2 0h1m1 0h1m2 0h1m2 0h2m2 0h1m1 0h1m2 0h1m-23 1h5m1 0h3m2 0h1m1 0h1m1 0h6m1 0h1m1 0h1m-17 1h1m5 0h3m3 0h1m-21 1h7m1 0h1m2 0h1m1 0h4m1 0h1m1 0h1m1 0h1m-23 1h1m5 0h1m1 0h2m1 0h1m2 0h3m3 0h1m1 0h3m-25 1h1m1 0h3m1 0h1m1 0h1m1 0h1m3 0h1m1 0h7m-23 1h1m1 0h3m1 0h1m3 0h1m1 0h4m2 0h2m4 0h1m-25 1h1m1 0h3m1 0h1m2 0h2m3 0h4m1 0h1m3 0h1m-24 1h1m5 0h1m2 0h3m1 0h4m1 0h1m3 0h2m-24 1h7m2 0h2m4 0h2m3 0h1m1 0h3"/>\n  </g>\n</svg>\n'
test_qr_and_logo = '<?xml version=\'1.0\' encoding=\'ASCII\' standalone=\'yes\'?>\n<svg xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" version="1.1" width="330.0" viewbox="0 0 330.0 330.0" height="330.0">\n  <g>\n    <g class="segno" transform="translate(0, 0) scale(10) ">\n      <path fill="#fff" d="M0 0h33v33h-33z"/>\n      <path stroke="#000" class="qrline" d="M4 4.5h7m4 0h2m1 0h2m2 0h7m-25 1h1m5 0h1m1 0h2m1 0h2m2 0h1m2 0h1m5 0h1m-25 1h1m1 0h3m1 0h1m3 0h1m7 0h1m1 0h3m1 0h1m-25 1h1m1 0h3m1 0h1m4 0h1m3 0h2m1 0h1m1 0h3m1 0h1m-25 1h1m1 0h3m1 0h1m2 0h2m2 0h1m4 0h1m1 0h3m1 0h1m-25 1h1m5 0h1m1 0h2m1 0h2m2 0h2m1 0h1m5 0h1m-25 1h7m1 0h1m1 0h1m1 0h1m1 0h1m1 0h1m1 0h7m-17 1h1m2 0h1m4 0h1m-13 1h4m1 0h2m2 0h1m4 0h2m3 0h1m-24 1h1m1 0h4m1 0h2m1 0h1m2 0h1m1 0h1m1 0h1m2 0h2m-21 1h1m1 0h1m2 0h3m1 0h1m1 0h6m1 0h1m1 0h2m-23 1h3m1 0h2m2 0h3m3 0h2m2 0h1m3 0h1m1 0h1m-24 1h2m2 0h2m4 0h5m2 0h2m2 0h1m1 0h1m-25 1h5m2 0h4m3 0h1m1 0h1m1 0h1m1 0h2m1 0h1m-18 1h1m4 0h1m1 0h1m2 0h2m2 0h2m-20 1h1m2 0h1m1 0h1m2 0h1m2 0h2m2 0h1m1 0h1m2 0h1m-23 1h5m1 0h3m2 0h1m1 0h1m1 0h6m1 0h1m1 0h1m-17 1h1m5 0h3m3 0h1m-21 1h7m1 0h1m2 0h1m1 0h4m1 0h1m1 0h1m1 0h1m-23 1h1m5 0h1m1 0h2m1 0h1m2 0h3m3 0h1m1 0h3m-25 1h1m1 0h3m1 0h1m1 0h1m1 0h1m3 0h1m1 0h7m-23 1h1m1 0h3m1 0h1m3 0h1m1 0h4m2 0h2m4 0h1m-25 1h1m1 0h3m1 0h1m2 0h2m3 0h4m1 0h1m3 0h1m-24 1h1m5 0h1m2 0h3m1 0h4m1 0h1m3 0h2m-24 1h7m2 0h2m4 0h2m3 0h1m1 0h3"/>\n    </g>\n    <g transform="translate(120.0, 120.0) scale(1) ">\n      <defs/>\n      <rect fill="#000000" height="90" width="90" x="0" y="0"/>\n    </g>\n    <g transform="translate(130.0, 130.0) scale(0.972222222222) "><circle fill="#2F9A41" cx="36" cy="36" r="35.7"/>\n<g>\n\t<path fill="#FFFFFF" d="M24.5,18.2v-7.1h8.2v7.1H24.5z M24.5,60.9v-7.1h8.2v7.1H24.5z M32.8,25.3v-7.1h8.2v7.1H32.8z    M32.8,53.8v-7.1h8.2v7.1H32.8z M41,32.4v-7.1h8.2v7.1H41z M41,46.7v-7.1h8.2v7.1H41z M49.2,39.6v-7.1h8.2v7.1H49.2z"/>\n</g>\n</g>\n  </g>\n</svg>\n'
alt_logo = '<svg width="100" height="100" viewBox="0 0 100 100" ><circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow" /></svg>'

class TestQRFactoryMethods(unittest.TestCase):
    def test_overwritten_input(self):
        qr = qrfactory.QRFactory()
        print "alt_logo = ", alt_logo
        qr.build_logo(alt_logo)
        qr.build_qrcode("asdfasdfas")
        qr.build_logo(open("logo.svg").read())
        self.assertEqual(test_qr_and_logo, qr.output_qr())

    def test_logo_first(self):
        qr = qrfactory.QRFactory()
        qr.build_logo(open("logo.svg").read())
        qr.build_qrcode("asdfasdfas")
        self.assertEqual(test_qr_and_logo, qr.output_qr())

    def test_qr_first(self):
        qr = qrfactory.QRFactory()
        qr.build_qrcode("asdfasdfas")
        qr.build_logo(open("logo.svg").read())
        self.assertEqual(test_qr_and_logo, qr.output_qr())

    def test_build_logo(self):
        qr = qrfactory.QRFactory()
        qr.build_logo(open("logo.svg").read())
        self.assertEqual(None, qr.output_qr()) # no ouput if only a logo input

    def test_build_qr(self):        
        qr = qrfactory.QRFactory()
        qr.build_qrcode("asdfasdfas")
        self.assertEqual(test_qr, qr.output_qr())

        
if __name__ == '__main__':
    unittest.main()
