import unittest
from CS3A_Assignment import DataSet as dataset


class TestStringMethods(unittest.TestCase):
    """
        T.D.D for DataSet class.
    """

    # Set Up
    def setUp(self):
        data = ''
        self.dataset = dataset()

    # Test for getter with no argument provided
    def test_fail_if_no_header_argument(self):
        result = self.dataset.get_header
        self.assertFalse(result)
    
    # Test for getter with valid argument provided
    def test_pass_if_correct_header_argument(self):
        data = 'Sebastian'
        self.dataset.get_header = data
        result = self.dataset.get_header
        self.assertTrue(result)

    # Test for getter with invalid argument provided
    def test_fail_if_invalid_header_argument(self):
        data = 'Sebastiankskkskskskkskskskskkskskskskskskksks'
        self.dataset.get_header = data
        result = self.dataset.get_header
        self.assertFalse(result)

    # Test for setter with valid argument provided
    def test_pass_if_correct_header(self):
        data = 'Sebastian'
        self.dataset.get_header = data
        result = self.dataset.get_header
        self.assertTrue(result)

    # Test for setter with invalid argument provided
    def test_fail_if_incorrect_header_argument(self):
        data = 'Sebastiankskkskskskkskskskskkskskskskskskksks'
        self.dataset.get_header = data
        result = self.dataset.get_header
        self.assertFalse(result)




if __name__ == '__main__':
    unittest.main()