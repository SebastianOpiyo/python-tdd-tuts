""" This program asks for the user's name, welcomes them to the project,
and then provides a selection menu for a user to choose from.
"""

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
    """ Provide an output whenever a user selects an option. """
    currency_options(home_currency)
    while True:
        print()
        print('{}'.format(dataset.get_header))
        print_menu()
        try:
            selection = int(input("What is your choice? "))
        except ValueError:   # Talk about why this needs to be here
            print("Please enter a number only")
            continue
        if selection == 1:
            print("Average rent functionality is not implemented yet")
        elif selection == 2:
            print("Minimum rent functionality is not implemented yet")
        elif selection == 3:
            print("Maximum rent functionality is not implemented yet")
        elif selection == 4:
            print("Location functionality is not implemented yet")
        elif selection == 5:
            print("Property type functionality is not implemented yet")
        elif selection == 6:
            print("Location filter functionality is not implemented yet")
        elif selection == 7:
            print("Property type functionality is not implemented yet")
        elif selection == 8:
            print("Load data functionality is not implemented yet")
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


class DataSet:
    """This is the base class with setter and getter header methods."""
    def __init__(self,):
        self.__header = ''
        self.header_length = 30
        self.__data = None
    
    @property
    def get_header(self):
        return self.__header

    @get_header.setter
    def get_header(self, new_header):
        # Error checking for passed in header. 
        if not (isinstance(new_header, str) and len(new_header) <= self.header_length):
            self.__header = ''
            print('This Header "{}" is too long, not valid. '.format(new_header))
            print('Header must be a string less than 30 characters long.')
        else:
            self.__header = new_header
            return self.__header
        # try:
        #     if (isinstance(new_header, str) and len(new_header) <= self.header_length):
        #         self.__header = new_header
        #     return self.__header
        # except ValueError as e:
        #     print(str(e))
        #     print('This Header "{}" is too long, not valid. '.format(new_header))
        #     print('Header must be a string less than 30 characters long')
        # else:
        #     self.__header = ''
        #     return self.__header


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
        header = air_bnb.get_header
        while not header:
            air_bnb.get_header = input("Enter a header for the menu: ")
            header=air_bnb.get_header
            
    print(air_bnb.get_header)
    menu(air_bnb)


# if __name__ == "__main__":
# unit_test()


if __name__ == "__main__":
    main()


"""
--- sample run #1 ---
Please enter your name: A
Hi A, welcome to Foothill's database project. 
What is your home currency? MON
What is your home currency? GBP
USD     EUR     CAD     GBP     CHF     NZD     AUD     JPY
12.50	11.25	17.50	10.00	11.88	20.75	20.25	1349.00	
25.00	22.50	35.00	20.00	23.75	41.50	40.50	2698.00	
37.50	33.75	52.50	30.00	35.62	62.25	60.75	4047.00	
50.00	45.00	70.00	40.00	47.50	83.00	81.00	5396.00	
62.50	56.25	87.50	50.00	59.38	103.75	101.25	6745.00	
75.00	67.50	105.00	60.00	71.25	124.50	121.50	8094.00	
87.50	78.75	122.50	70.00	83.12	145.25	141.75	9443.00	
100.00	90.00	140.00	80.00	95.00	166.00	162.00	10792.00	
112.50	101.25	157.50	90.00	106.88	186.75	182.25	12141.00	
Main Menu
1 -  Print Average Rent by Location and Property Type 
2 -  Print Minimum Rent by Location and Property Type 
3 -  Print Maximum Rent by Location and Property Type 
4 -  Print Min/Avg/Max by Location 
5 -  Print Min/Avg/Max by Property Type 
6 -  Adjust Location Filters 
7 -  Adjust Property Type Filters 
8 -  Load Data 
9 -  Quit 
What is your choice? 1
Average rent functionality is not implemented yet 
Main Menu
1 -  Print Average Rent by Location and Property Type 
2 -  Print Minimum Rent by Location and Property Type 
3 -  Print Maximum Rent by Location and Property Type 
4 -  Print Min/Avg/Max by Location 
5 -  Print Min/Avg/Max by Property Type 
6 -  Adjust Location Filters 
7 -  Adjust Property Type Filters 
8 -  Load Data 
9 -  Quit 
What is your choice? 9
Goodbye! Thank you for using the database 
"""