import unittest
from CS3A_Assignment import DataSet as dataset


class TestStringMethods(unittest.TestCase):
    """
        T.D.D for DataSet class.
    """

    def setUp(self):
        self._dataset = dataset()
        self._data = self._dataset.load_default_data

    """
    ********************************************
    * Tests for Data loading from the CSV file.*
    ********************************************
    """
    def test_data_file_loading(self):
        self.assertEqual(len(self._dataset.load_file()), 48895,
                         msg="The length of the data is not correct!")

    """
    ******************************************************
    * Tests for Getter & Setter Handling Begin from here.*
    ******************************************************
    """

    def test_fail_if_no_header_argument(self):
        """Test for getter"""
        result = self._dataset.header
        self.assertFalse(result)

    def test_pass_if_correct_header_argument(self):
        """ Test for getter"""
        header_data = 'Sebastian'
        self._dataset.header = header_data
        result = self._dataset.header
        self.assertTrue(result)

    def test_fail_if_invalid_header_argument(self):
        """Test for getter """
        header_data = 'Sebastiankskkskskskkskskskskkskskskskskskksks'
        with self.assertRaises(ValueError):
            self._dataset.header = header_data
            result = self._dataset.header
            self.assertFalse(result)

    def test_pass_if_correct_header(self):
        """Test for setter"""
        header_data = 'Sebastian'
        self._dataset.header = header_data
        result = self._dataset.header
        self.assertTrue(result)

    def test_fail_if_incorrect_header_argument(self):
        """Test for setter"""
        header_data = 'Sebastiankskkskskskkskskskskkskskskskskskksks'
        with self.assertRaises(ValueError):
            self._dataset.header = header_data
            result = self._dataset.header
            self.assertTrue(result)

    """
    *******************************************
    * Tests for Data Handling Begin from here.*
    *******************************************
    """
    def test_raise_empty_dataset_error(self):
        """Test _cross_table_statistics --
        The method load_default_data() has been refactored. All it does
        is call other methods.
        """
        result = True
        if self._dataset.load_default_data():
            result = None
            self.assertFalse(result)
        self.assertTrue(result)

    def test_invalid_property_type_returns_none_tuple(self):
        descriptor_one = "Staten Island"
        descriptor_two = "Entire cripa/apt"
        result = self._dataset._cross_table_statistics(descriptor_one, descriptor_two)
        if result is None:
            self.assertFalse(result)
        self.assertFalse(result)
    
    def test_invalid_borrow_returns_none_tuple(self):
        descriptor_one = "Aghhd Blaslasasla"
        descriptor_two = "Private room"
        result = self._dataset._cross_table_statistics(descriptor_one, descriptor_two)
        if result is None:
            self.assertFalse(result)
        self.assertFalse(result)

    def test_unmatching_rows_returns_none_tuple(self):
        descriptor_one = "Aghhd Blaslasasla"
        descriptor_two = "Gooakakkakkakaak"
        result = self._dataset._cross_table_statistics(descriptor_one, descriptor_two)
        if result is None:
            self.assertFalse(result)
        self.assertFalse(result)

    def test_one_matching_rows_returns_correct_tuple(self):
        descriptor_one = "Bronx"
        descriptor_two = "Private room"
        result = self._dataset._cross_table_statistics(descriptor_one, descriptor_two)
        if result is None:
            self.assertFalse(result)
        self.assertTrue(result)

    def test_multiple_matching_rows_returns_correct_tuple(self):
        descriptor_one = "Brooklyn"
        descriptor_two = "Private room"
        result = self._dataset._cross_table_statistics(descriptor_one, descriptor_two)
        if result is None:
            self.assertFalse(result)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
