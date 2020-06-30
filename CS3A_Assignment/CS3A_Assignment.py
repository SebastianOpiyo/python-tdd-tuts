#!/bin/python3
# Author: Sebastian Opiyo
# Date Created: May 29, 2020
# Date Modified: June 17, 2020
# Description: Learning OOP by use of the capstone project.
""" 
This program asks for the user's name, welcomes them to the project,
and then provides a selection menu for a user to choose from.
"""

# Imports
from enum import Enum
import csv


conversions = {
    "USD": 1,
    "EUR": .9,
    "CAD": 1.4,
    "GBP": .8,
    "CHF": .95,
    "NZD": 1.66,
    "AUD": 1.62,
    "JPY": 107.92
}

home_currency = ""


class DataSet(object):
    """The DataSet class will present summary tables based on
    information imported from a .csv file.
    """
    header_length = 30

    def __init__(self, header=""):
        self._data = None
        try:
            self.header = header
        except ValueError:
            self.header = ""
        self._labels = {
            DataSet.Categories.LOCATION: set(),
            DataSet.Categories.PROPERTY_TYPE: set()
        }
        self._active_labels = {
            DataSet.Categories.LOCATION: set(),
            DataSet.Categories.PROPERTY_TYPE: set()
        }

    class EmptyDatasetError(Exception):
        """Custom Error class that raises the Empty data set error in case of one."""
        pass

    class Categories(Enum):
        LOCATION = 0
        PROPERTY_TYPE = 1

    class Stats(Enum):
        MIN = 0
        AVG = 1
        MAX = 2

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, new_header: str):
        try:
            if isinstance(new_header, str) and (len(new_header) < self.header_length):
                self._header = new_header
            else:
                raise ValueError
        except ValueError:
            pass
            # print('This Header "{}" is too long, not valid.\n Header must be a string less than 30 '
            #       'characters long.'.format(new_header))

    def _cross_table_statistics(self, descriptor_one: str, descriptor_two: str):
        """ Given a label from each category, calculate summary
        statistics for the items matching both labels.

        Keyword arguments:
            descriptor_one -- the label for the first category
            descriptor_two -- the label for the second category

        Returns a tuple of min, average, max from the matching rows."""
        if not self._data:
            raise DataSet.EmptyDatasetError
        value_list = [item[2] for item in self._data if
                      item[0] == descriptor_one and item[1] == descriptor_two]
        if len(value_list) == 0:
            return None, None, None
        return min(value_list), sum(value_list) / len(value_list), max(value_list)

    def load_default_data(self):
        self._data = self.load_file()
        self._initialize_sets()

    @staticmethod
    def load_file():
        """Load all the data from AB_NYC_2019.csv file into self._data"""
        with open('AB_NYC_2019.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            return_list = []
            next(csv_reader)
            for line in csv_reader:
                item = line[1], line[2], int(line[3])
                return_list.append(item)
            return return_list

    @staticmethod
    def bubble_sort(list_to_sort: list):
        """By use of bubble sort and recursion, the static function
        orders the labels alphabetically in ascending order."""
        count = 0
        array = list_to_sort[:]
        for idx in range(len(array) - 1):
            if array[idx] > array[idx + 1]:
                array[idx], array[idx + 1] = array[idx + 1], array[idx]
                count += 1
        if count == 0:
            return array
        else:
            return DataSet.bubble_sort(array)

    def _initialize_sets(self):
        """Examine the category labels in self._data and create a set for each category
        containing the labels.
        """

        if not self._data:
            raise DataSet.EmptyDatasetError
        for category in self.Categories:
            self._labels[category] = set([i[category.value] for i in self._data])
            self._active_labels[category] = self._labels[category].copy()

    def display_cross_table(self, stat: Stats):
        """ prints the table of statistics. Depends on whether the values are Min, Avg or Max.
        Use _cross_table_statistics() method to calculate values that appear in the table.
        """
        try:
            if not self._data:
                raise DataSet.EmptyDatasetError
            property_labels = DataSet.bubble_sort(list(self._labels[DataSet.Categories.PROPERTY_TYPE]))
            location_labels = DataSet.bubble_sort(list(self._labels[DataSet.Categories.LOCATION]))
            print(f"                ", end="")
            for item in property_labels:
                print(f"{item:20}", end="")
            print()
            for item_one in location_labels:
                print(f" {item_one:15}", end="")
                for item_two in property_labels:
                    value = self._cross_table_statistics(item_one,
                                                         item_two)[stat.value]
                    if value is None:
                        print(f"$ {'N/A':<18}", end="")
                    else:
                        print(f"$ {value:<18.2f}", end="")
                print()
        except DataSet.EmptyDatasetError:
            print("Please Add a data set first!")

    def _alternate_category_type(self, first_category_type):
        """ Given one of the two Category Enum entries, return the
        other one.
        """
        if first_category_type is self.Categories.LOCATION:
            second_category_type = self.Categories.PROPERTY_TYPE
        else:
            second_category_type = self.Categories.LOCATION
        return second_category_type

    def _table_statistics(self, row_category: Categories, descriptor: str):
        """ Given a category and a label from that category, calculate
        summary statistics for the rows that match that label.
        Include only rows where the alternate category's label is
        active.
        Keyword arguments:
        row_category -- a category from the Categories Enum
        descriptor -- a label from row_category
        Returns a tuple of min, average, max from the matching rows.
        """
        try:
            if not self._data:
                raise DataSet.EmptyDatasetError
            detail_category = self._alternate_category_type(row_category)
            value_list = [item[2] for item in self._data if
                          item[row_category.value] == descriptor and
                          item[detail_category.value] in
                          self._active_labels[detail_category]]
            if len(value_list) == 0:
                return None, None, None
            return min(value_list), sum(value_list) / len(value_list), \
                max(value_list)
        except DataSet.EmptyDatasetError:
            print("Please Add a data set first!")

    def display_field_table(self, rows: Categories):
        """ Given a category, display one row for each label in that
        category with min, avg, max displayed for each row.
        Include only rows where the alternate category's label is active
        """
        try:
            if not self._data:
                raise DataSet.EmptyDatasetError
            detail_category = self._alternate_category_type(rows)
            print("The following data are from properties "
                  "matching these criteria:")
            for label in self.get_active_labels(detail_category):
                print(f"- {label}")
            print(f"                    Minimum             Average             Maximum ")

            for descriptor in DataSet.bubble_sort(self._labels[rows]):
                min_value, avg_value, max_value = \
                    self._table_statistics(rows, descriptor)
                print(f"{descriptor:20}", end="")
                if min_value is None:
                    print(f"{'N/A':20}{'N/A':20}{'N/A':20}", end="")
                else:
                    print(f"$ {min_value:<18.2f}$ {avg_value:<18.2f}$ "
                          f"{max_value:<18.2f}", end="")
                print()
        except DataSet.EmptyDatasetError:
            print("Please Add a data set first!")

    def get_labels(self, category: Categories):
        """Returns a list of items in _labels[category]"""
        if not self._data:
            raise DataSet.EmptyDatasetError
        return list(self._labels[category])

    def get_active_labels(self, category: Categories):
        """Returns a list of items in _active_labels[category]"""
        if not self._data:
            raise DataSet.EmptyDatasetError
        return list(self._active_labels[category])

    def toggle_active_labels(self, category: Categories, descriptor: str):
        """Does add if not exist or remove labels if existing from _active_labels,
        allowing user to filter out certain property types or locations.
        """
        if not self._data:
            raise DataSet.EmptyDatasetError
        try:
            if descriptor not in self._labels[category]:
                raise KeyError
            elif descriptor in self._labels[category]:
                self._active_labels[category].add(descriptor) \
                    if descriptor not in self._active_labels[category] else \
                    self._active_labels[category].remove(descriptor)
        except KeyError:
            print('The entry is non-existent!!!')


def manage_filters(dataset: DataSet, category: DataSet.Categories):
    """Prints a menu-like list of all labels for a given category indicating
    which whether the state is active or inactive and allowing user to make
    necessary changes in a loop till done.
    """
    while True:
        print("The following labels are in the dataset:")
        for index, value in enumerate(dataset.get_labels(category), start=1):
            print(f'{index}: {value:20}  ACTIVE' if value in dataset.get_active_labels(category)
                  else f'{index}: {value:20}  INACTIVE')
        try:
            toggle_selection = int(input(
                "Please select an item to toggle or enter a blank line when you are finished: "))
            if toggle_selection:
                try:
                    dataset.toggle_active_labels(category, dataset.get_labels(category)[toggle_selection - 1])
                    continue
                except IndexError:
                    print('Value entered not within range, please enter a number from one of the options!!')
            elif toggle_selection == "":
                break
        except ValueError:
            print("Please enter a number from one of the options or _ to terminate.")
            break
        print(dataset.get_active_labels(category))


def print_menu():
    """ Print out all of the options that a user can select. """
    print("Main Menu")
    print(1, "- ", "Print Average Rent by Location and Property Type ")
    print(2, "- ", "Print Minimum Rent by Location and Property Type ")
    print(3, "- ", "Print Maximum Rent by Location and Property Type ")
    print(4, "- ", "Print Min/Avg/Max by Location ")
    print(5, "- ", "Print Min/Avg/Max by Property Type ")
    print(6, "- ", "Adjust Location Filters ")
    print(7, "- ", "Adjust Property Type Filters ")
    print(8, "- ", "Load Data ")
    print(9, "- ", "Quit ")


def menu(dataset):
    """ Present user with option to access the Airbnb dataset. """
    currency_options(home_currency)
    print()
    while True:
        print()
        print(dataset.header)
        print_menu()
        try:
            selection = int(input("What is your choice? "))
        except ValueError:
            print("Please enter a number only")
            continue
        if selection == 1:
            try:
                dataset.display_cross_table(DataSet.Stats.AVG)
            except dataset.EmptyDatasetError:
                print("Please Load Dataset First!!")
        elif selection == 2:
            try:
                dataset.display_cross_table(DataSet.Stats.MIN)
            except dataset.EmptyDatasetError:
                print("Please Load a Dataset First!!")
        elif selection == 3:
            try:
                dataset.display_cross_table(DataSet.Stats.MAX)
            except dataset.EmptyDatasetError:
                print("Please Load a Dataset First!!")
        elif selection == 4:
            try:
                dataset.display_field_table(DataSet.Categories.PROPERTY_TYPE)
            except dataset.EmptyDatasetError:
                print("Please Load a Dataset First!!")
        elif selection == 5:
            try:
                dataset.display_field_table(DataSet.Categories.LOCATION)
            except dataset.EmptyDatasetError:
                print("Please Load a Dataset First!!")
        elif selection == 6:
            try:
                manage_filters(dataset=dataset, category=dataset.Categories.LOCATION)
            except dataset.EmptyDatasetError:
                print("Please Load a Dataset First!!")
        elif selection == 7:
            try:
                manage_filters(dataset=dataset, category=dataset.Categories.PROPERTY_TYPE)
            except dataset.EmptyDatasetError:
                print("Please Load a Dataset First!!")
        elif selection == 8:
            dataset.load_default_data()
            print("Data Loaded Successfully!")
        elif selection == 9:
            print("Goodbye!  Thank you for using the database")
            break
        else:
            print("Please enter a number between 1 and 9")


def currency_converter(quantity: float, source_curr: str, target_curr: str):
    """ Calculates the value after converting money from a currency """
    if source_curr not in conversions or target_curr not in \
            conversions or quantity <= 0:
        raise ValueError
    in_usd = quantity / conversions[source_curr]
    in_target = in_usd * conversions[target_curr]
    return in_target


def currency_options(base_curr="EUR"):
    """ Print out a table of options for converting base_curr to all
    other currencies
    """
    print(f"Options for converting from {base_curr}:")
    for target in conversions:
        print(f"{target:10}", end="")
    print()
    for i in range(10, 100, 10):
        for target in conversions:
            print(f"{currency_converter(i, base_curr, target):<10.2f}", end="")
        print()


def main():
    """ Obtain the user's name, welcome them to the project, and then
    call the menu function to display a selection menu for the user
    to choose from.
    """

    air_bnb = DataSet()

    global home_currency
    name = input("Please enter your name: ")
    message = "Hi " + name + ", welcome to Foothill's database project."
    print(message)

    while home_currency not in conversions:
        home_currency = input("What is your home currency? ")
    else:
        header = air_bnb.header
        while not header:
            air_bnb.header = input("Enter a header for the menu: ")
            header = air_bnb.header

    print(air_bnb.header)
    menu(air_bnb)


if __name__ == "__main__":
    main()
