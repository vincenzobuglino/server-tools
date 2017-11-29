# -*- coding: utf-8 -*-
# © 2016 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree
from openerp.tools.misc import mute_logger
from openerp.tests.common import TransactionCase


class ExtractorCase(TransactionCase):
    def setUp(self):
        super(ExtractorCase, self).setUp()

        # Shortcut
        self.imgs_from_html = self.env["ir.fields.converter"].imgs_from_html
        self.logger = ('openerp.addons.html_image_url_extractor'
                       '.models.ir_fields_converter')

    def test_mixed_images_found(self):
        """Images correctly found in <img> elements and backgrounds."""
        content = u"""
            <div>
                <!-- src-less img -->
                <img/>
                <p/>
                <img src="/path/0"/>
                <img src="/path/1"/>
                <img src="/path/2"/>
                <img src="/path/3"/>
                <section style="background : URL('/path/4');;background;ö;">
                    <div style='BACKGROUND-IMAGE:url(/path/5)'>
                        <p style="background:uRl(&quot;/path/6&quot;)">
                            <img src="/path/7"/>
                        </p>
                    </div>
                </section>
            </div>
            """

        # Read all images
        for n, url in enumerate(self.imgs_from_html(content)):
            self.assertEqual("/path/%d" % n, url)
        self.assertEqual(n, 7)

        # Read only first image
        for n, url in enumerate(self.imgs_from_html(content, 1)):
            self.assertEqual("/path/%d" % n, url)
        self.assertEqual(n, 0)

    def test_empty_html(self):
        """Empty HTML handled correctly."""
        with mute_logger(self.logger):
            for laps, text in self.imgs_from_html(""):
                self.assertTrue(False)  # You should never get here

        with self.assertRaises(etree.XMLSyntaxError):
            with mute_logger(self.logger):
                list(self.imgs_from_html("", fail=True))

    def test_false_html(self):
        """``False`` HTML handled correctly."""
        with mute_logger(self.logger):
            for laps, text in self.imgs_from_html(False):
                self.assertTrue(False)  # You should never get here

        with self.assertRaises(TypeError):
            list(self.imgs_from_html(False, fail=True))

    def test_bad_html(self):
        """Bad HTML handled correctly."""
        with mute_logger(self.logger):
            for laps, text in self.imgs_from_html("<<bad>"):
                self.assertTrue(False)  # You should never get here

        try:
            # Newer versions of lxml parse this as
            # '<html><body><p>&lt;<bad/></p></body></html>'
            # so the exception is not guaranteed
            with mute_logger(self.logger):
                images = list(self.imgs_from_html("<<bad>", fail=True))
            self.assertFalse(images)
        except etree.ParserError:
            pass
