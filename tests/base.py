import os
from django.test import LiveServerTestCase, override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


# device sizes
SMALL_MOBILE  = {'width':  320, 'height':  570}
COMMON_MOBILE = {'width':  360, 'height':  640}
BIG_MOBILE =    {'width':  720, 'height': 1280}
SMALL_DESKTOP = {'width': 1280, 'height':  800}
LARGE_DESKTOP = {'width': 1440, 'height':  900}

# needs the basic static file storage to properly serve files
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class FunctionalTestCase(StaticLiveServerTestCase):
    device = None
    dimensions = COMMON_MOBILE

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)
        from selenium import webdriver
        cls.browser = webdriver.Firefox()
        cls.browser.set_window_size(cls.dimensions['width'], cls.dimensions['height'])

    def build_url(self, url):
        return self.host + url

    def get(self, url, host=None):
        full_url = self.build_url(url)
        self.browser.get(full_url)

    def set_size(self, size_config):
        self.browser.set_window_size(
            size_config['width'],
            size_config['height'])

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.host = os.environ.get('ACCEPTANCE_TEST_HOST', self.live_server_url)

    def click_on(self, text):
        self.browser.find_element_by_link_text(text).click()

    @classmethod
    def tearDownClass(cls, *args, **kwargs):
        cls.browser.close()
        super().tearDownClass(*args, **kwargs)

    def screenshot(self, filename):
        path = os.path.join('tests/screenshots', filename)
        self.browser.save_screenshot(path)

    def handle_input(self, elements, value):
        input_type = elements[0].get_attribute('type')
        if input_type == 'checkbox':
            for element in elements:
                if element.get_attribute('value') == value:
                    element.click()
        elif input_type == 'radio':
            for element in elements:
                if element.get_attribute('value') == value:
                    element.click()
        else:
            elements[0].send_keys(value)

    def fill_form(self, **answers):
        for name, value in answers.items():
            input_elements = self.browser.find_elements_by_name(name)
            self.handle_input(input_elements, value)
        form = self.browser.find_element_by_tag_name('form')
        form.submit()

# relevant: http://selenium-python.readthedocs.io/faq.html#how-to-scroll-down-to-the-bottom-of-a-page
class ScreenSequenceTestCase(FunctionalTestCase):

    def build_filepath(self, prefix, i, method):
        if not prefix:
            prefix = getattr(self, 'sequence_prefix', self.__class__.__name__)
        filename = '{prefix}-{index:03d}__{method}.png'.format(
            prefix=prefix, index=i, method=method)
        return filename

    def run_sequence(self, prefix, sequence, size=COMMON_MOBILE, full_height=True):
        self.set_size(size)
        for i, step in enumerate(sequence):
            att_name, args, kwargs = step
            method = getattr(self, att_name)
            method(*args, **kwargs)
            if full_height:
                body = self.browser.find_element_by_tag_name('body')
                height = max(size['height'], int(body.get_attribute('scrollHeight')))
                self.set_size(dict(width=size['width'], height=height))
            self.screenshot(self.build_filepath(prefix, i, att_name))


class DEVICES:
    Apple_iPhone_3GS = "Apple iPhone 3GS"
    Apple_iPhone_4 = "Apple iPhone 4"
    Apple_iPhone_5 = "Apple iPhone 5"
    Apple_iPhone_6 = "Apple iPhone 6"
    Apple_iPhone_6_Plus = "Apple iPhone 6 Plus"
    BlackBerry_Z10 = "BlackBerry Z10"
    BlackBerry_Z30 = "BlackBerry Z30"
    Google_Nexus_4 = "Google Nexus 4"
    Google_Nexus_5 = "Google Nexus 5"
    Google_Nexus_S = "Google Nexus S"
    HTC_Evo_Touch_HD_Desire_HD_Desire = "HTC Evo, Touch HD, Desire HD, Desire"
    HTC_One_X_EVO_LTE = "HTC One X, EVO LTE"
    HTC_Sensation_Evo_3D = "HTC Sensation, Evo 3D"
    LG_Optimus_2X_Optimus_3D_Optimus_Black = "LG Optimus 2X, Optimus 3D, Optimus Black"
    LG_Optimus_G = "LG Optimus G"
    LG_Optimus_LTE_Optimus_4X_HD = "LG Optimus LTE, Optimus 4X HD" 
    LG_Optimus_One = "LG Optimus One"
    Motorola_Defy_Droid_Droid_X_Milestone = "Motorola Defy, Droid, Droid X, Milestone"
    Motorola_Droid_3_Droid_4_Droid_Razr_Atrix_4G_Atrix_2 = "Motorola Droid 3, Droid 4, Droid Razr, Atrix 4G, Atrix 2"
    Motorola_Droid_Razr_HD = "Motorola Droid Razr HD"
    Nokia_C5_C6_C7_N97_N8_X7 = "Nokia C5, C6, C7, N97, N8, X7"
    Nokia_Lumia_7X0_Lumia_8XX_Lumia_900_N800_N810_N900 = "Nokia Lumia 7X0, Lumia 8XX, Lumia 900, N800, N810, N900"
    Samsung_Galaxy_Note_3 = "Samsung Galaxy Note 3"
    Samsung_Galaxy_Note_II = "Samsung Galaxy Note II"
    Samsung_Galaxy_Note = "Samsung Galaxy Note"
    Samsung_Galaxy_S_III_Galaxy_Nexus = "Samsung Galaxy S III, Galaxy Nexus"
    Samsung_Galaxy_S_S_II_W = "Samsung Galaxy S, S II, W"
    Samsung_Galaxy_S4 = "Samsung Galaxy S4"
    Sony_Xperia_S_Ion = "Sony Xperia S, Ion"
    Sony_Xperia_Sola_U = "Sony Xperia Sola, U"
    Sony_Xperia_Z_Z1 = "Sony Xperia Z, Z1"
    Amazon_Kindle_Fire_HDX7 = "Amazon Kindle Fire HDX 7″"
    Amazon_Kindle_Fire_HDX8_9 = "Amazon Kindle Fire HDX 8.9″"
    Amazon_Kindle_Fire_First_Generation = "Amazon Kindle Fire (First Generation)"
    Apple_iPad_1_2_iPad_Mini = "Apple iPad 1 / 2 / iPad Mini"
    Apple_iPad_3_4 = "Apple iPad 3 / 4"
    BlackBerry_PlayBook = "BlackBerry PlayBook"
    Google_Nexus_10 = "Google Nexus 10"
    Google_Nexus_7_2 = "Google Nexus 7 2"
    Google_Nexus_7 = "Google Nexus 7"
    Motorola_Xoom_Xyboard = "Motorola Xoom, Xyboard"
    Samsung_Galaxy_Tab_7_7_8_9_10_1 = "Samsung Galaxy Tab 7.7, 8.9, 10.1"
    Samsung_Galaxy_Tab = "Samsung Galaxy Tab"
    Notebook_with_touch = "Notebook with touch"