#!/usr/bin/env python
from unittest import TestCase, TestLoader, TextTestRunner


import test_vars
import qrfactory

class TestQRFactoryMethods(TestCase):
    def test_build_logo(self):
        '''Test ouput with only logo data'''
        qr = qrfactory.QRFactory()
        qr.build_logo(test_vars.logo)
        self.assertEqual(None, qr.output_qr()) # no ouput if only a logo input

    def test_build_qr(self):
        '''Test output with only qr data'''
        qr = qrfactory.QRFactory()
        qr.build_qrcode("asdfasdfas", "red", "yellow", 5)
        breakpoint()
        self.assertEqual(test_vars.test_qr_full, qr.output_qr())

    def test_logo_first(self):
        '''Test with inputting logo first'''
        qr = qrfactory.QRFactory()
        qr.build_logo(test_vars.logo)
        qr.build_qrcode("asdfasdfas")
        self.assertEqual(test_vars.test_qr_and_logo, qr.output_qr())

    def test_qr_first(self):
        '''Test with inputing qr data first'''
        qr = qrfactory.QRFactory()
        qr.build_qrcode("asdfasdfas")
        qr.build_logo(test_vars.logo)
        self.assertEqual(test_vars.test_qr_and_logo, qr.output_qr())

    def test_data_on_instantiation(self):
        '''Test with inputing data with instantiation of object'''
        qr = qrfactory.QRFactory(test_vars.logo, "asdfasdfas", "red", "yellow", 5)
        self.assertEqual(test_vars.test_qr_and_logo_full, qr.output_qr())

    def test_overwritten_logo(self):
        '''Test Overwritting logo'''
        qr = qrfactory.QRFactory()
        qr.build_logo(test_vars.alt_logo)
        qr.build_qrcode("asdfasdfas")
        qr.build_logo(test_vars.logo)
        self.assertEqual(test_vars.test_qr_and_logo, qr.output_qr())

    def test_overwritten_qr(self):
        '''Test Overwritting qr data'''
        qr = qrfactory.QRFactory()
        qr.build_qrcode("qwerqwerrweqrqwer")
        qr.build_logo(test_vars.logo)
        qr.build_qrcode("asdfasdfas")
        self.assertEqual(test_vars.test_qr_and_logo, qr.output_qr())

    def test_multiple_outputs_inputs(self):
        '''Test that multiple outputs and inputs don't change the result'''
        # Maybe went overboard with this one because of bug in svgutils -_-
        qr = qrfactory.QRFactory()
        qr.build_logo(test_vars.logo)
        qr.build_qrcode("asdfasdfas")
        self.assertEqual(test_vars.test_qr_and_logo, qr.output_qr())
        qr.build_qrcode("asdfasdfas")
        self.assertEqual(test_vars.test_qr_and_logo, qr.output_qr())
        qr.build_logo(test_vars.logo)
        self.assertEqual(test_vars.test_qr_and_logo, qr.output_qr())
        qr.build_qrcode("asdfasdfas")
        self.assertEqual(test_vars.test_qr_and_logo, qr.output_qr())
        qr.build_logo(test_vars.logo)
        self.assertEqual(test_vars.test_qr_and_logo, qr.output_qr())
        qr.build_logo(test_vars.logo)
        self.assertEqual(test_vars.test_qr_and_logo, qr.output_qr())
        self.assertEqual(test_vars.test_qr_and_logo, qr.output_qr())

if __name__ == '__main__':
    suite = TestLoader().loadTestsFromTestCase(TestQRFactoryMethods)
    TextTestRunner().run(suite)
