#!/bin/python3
# Author: Ahmed Raouf
# Date Created: May 29, 2020
# Date Modified: June 17, 2020
# Description:
""" 
This program asks for the user's name, welcomes them to the project,
and then provides a selection menu for a user to choose from.
"""

# Imports
from enum import Enum


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
            print('This Header "{}" is too long, not valid.\n Header must be a string less than 30 '
                  'characters long.'.format(new_header))

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

    def load_default_data(self) -> object:
        self._data = [("Staten Island", "Private room", 70),
                      ("Brooklyn", "Private room", 50), ("Bronx", "Private room", 40),
                      ("Brooklyn", "Entire home/apt", 150), ("Manhattan", "Private room", 125),
                      ("Manhattan", "Entire home/apt", 196), ("Brooklyn", "Private room", 110),
                      ("Manhattan", "Entire home/apt", 170), ("Manhattan", "Entire home/apt", 165),
                      ("Manhattan", "Entire home/apt", 150), ("Manhattan", "Entire home/apt", 100),
                      ("Brooklyn", "Private room", 65), ("Queens", "Entire home/apt", 350),
                      ("Manhattan", "Private room", 99), ("Brooklyn", "Entire home/apt", 200),
                      ("Brooklyn", "Entire home/apt", 150), ("Brooklyn", "Private room", 99),
                      ("Brooklyn", "Private room", 120)]
        self._initialize_sets()

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
            property_labels = list(self._labels[DataSet.Categories.PROPERTY_TYPE])
            location_labels = list(self._labels[DataSet.Categories.LOCATION])
            print(f"                ", end="")
            for item in property_labels:
                print(f"{item:20}", end="")
            print()
            for item_one in location_labels:
                print(f"{item_one:15}", end="")
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

    def _table_statics(self, row_category: Categories, label: str):
        """Given a category from Categories Enum, and string matching one of the items
        in the category, calculate the Min, Max, and Avg rent for properties in that category
        with filtered values."""
        try:
            if not self._data:
                raise DataSet.EmptyDatasetError
            result = []
            property_labels = list(self._labels[DataSet.Categories.PROPERTY_TYPE])
            location_labels = list(self._labels[DataSet.Categories.LOCATION])
            labels = [property_labels[:] if item in location_labels else location_labels[:]
                      for item in self.get_active_labels(row_category)]
            for elem in labels[0]:
                min_max_avg = [item[2] for item in self._data if
                               all(x in item for x in [label, elem])
                               and label in self.get_active_labels(row_category)]
                if len(min_max_avg) == 0:
                    result.append([elem, 0, 0, 0])
                else:
                    result.append([elem, min(min_max_avg), max(min_max_avg), sum(min_max_avg)/len(min_max_avg)])
            return result
        except DataSet.EmptyDatasetError:
            print("Please Add a data set first!")

    def display_field_table(self, rows: Categories):
        """Displays a table of Min, Max and Average depending on
        Categories value passed. Utilizes filtered out data and
        _table_statistics to print out active labels and data."""
        try:
            if not self._data:
                raise DataSet.EmptyDatasetError
            print("The following data are from properties matching these criteria:")
            for item in self.get_active_labels(rows):
                print(f'- {item}')

            print(f'{"":20} Minimum {"":<12} Average {"":<12} Maximum ')
            property_labels = list(self._labels[DataSet.Categories.PROPERTY_TYPE])
            location_labels = list(self._labels[DataSet.Categories.LOCATION])
            labels = [property_labels[:] if item in location_labels else location_labels[:]
                      for item in self.get_active_labels(rows)]
            data = []
            for item in self.get_active_labels(rows):
                val = self._table_statics(rows, item)
                data.append(val)
            minimum = []
            maximum = []
            avg = []
            for items in data:
                for values in items:
                    if len(items):
                        minimum.append(values[1],)
                        maximum.append(values[2],)
                        avg.append(values[3],)
            # print(minimum)
            # print(maximum)
            # print(avg)
            pos_counter = len(labels[0]) * 2
            min_val = minimum[-pos_counter] + minimum[-(pos_counter // 2)]
            max_val = maximum[-pos_counter] + maximum[-(pos_counter // 2)]
            avg_val = avg[-pos_counter] + avg[-(pos_counter // 2)]
            while pos_counter is len(labels[0]*2):  # need a revisit!
                for label in labels[0]:
                    try:
                        print(f'{label:20} $ {min_val:<18.2f} $ {avg_val:<18.2f} $ {max_val:<18.2f}')
                    except TypeError:
                        print(f'{label:20} $ {"N/A":<18} $ {"N/A":<18} $ {"N/A":<18}')
                pos_counter -= 1
                break
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


def main() -> object:
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
