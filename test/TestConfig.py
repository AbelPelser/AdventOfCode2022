import os
import re


class TestConfig(object):
    # Allow subclasses to override setUp
    @classmethod
    def setUpClass(cls):
        cls.day_n = int(''.join(re.findall('\\d+', cls.__name__)))
        if cls is not TestConfig and cls.setUp is not TestConfig.setUp:
            orig_setUp = cls.setUp

            def setUpOverride(self, *args, **kwargs):
                TestConfig.setUp(self)
                return orig_setUp(self, *args, **kwargs)

            cls.setUp = setUpOverride

    def setUp(self):
        while 'test' in os.getcwd() or 'puzzles' in os.getcwd():
            os.chdir('..')
        print(os.getcwd())
        os.chdir(f'./puzzles/Day{self.day_n}')
