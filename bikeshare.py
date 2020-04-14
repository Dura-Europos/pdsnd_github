import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january','february','march','april','may','june']
days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
filter_type = ['month','day','both','none']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York City, or Washington? \n").lower()
    while city not in CITY_DATA:
        city = input("Invalid input, please try again: ").lower()
    print("Looks like you want to check the database for {}. If not, please restart the program \n".format(city.title()))


    filter = input("Would you like to filter the data by month, day, or not at all? Type 'none' for no time filter: \n").lower()
    while filter not in filter_type:
        filter = input("Invalid input, please enter one of the following: 'month','day','both','none'\n").lower()
    # get user input for month (all, january, february, ... , june)
    if filter in ['month','both']:
        month = input("Which month - January, February, March, April, May, or June?\n").lower()
        while month not in months:
            month = input("Invalid input, please try again: ").lower()
    elif filter in ['day','none']:
        month = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter in ['day','both']:
        day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n").lower()
        while day not in days:
            day = input("Invalid input, please try again: ")
    elif filter in ['month','none']:
        day = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    pop_month = df['month'].value_counts()
    month = months[pop_month.index[0] - 1].title()
    print("Most common month: {}, Count: {}".format(month, pop_month.values[0]))

    # display the most common day of week
    pop_day = df['day_of_week'].value_counts()
    print("Most common day of week: {}, Count: {}".format(pop_day.index[0], pop_day.values[0]))

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    pop_hour = df['hour'].value_counts()
    print("Most Frequent Start Hour: {}, Count: {}".format(pop_hour.index[0], pop_hour.values[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].value_counts()
    print("The most commonly used start station: {}, Count: {}".format(popular_start.index[0], popular_start[0]))

    # display most commonly used end station
    popular_end = df['End Station'].value_counts()
    print("The most commonly used end station: {}, Count: {}".format(popular_end.index[0], popular_end[0]))

    # display most frequent combination of start station and end station trip
    combo = df.groupby(['Start Station', 'End Station']).size()
    pop_combo = combo[combo.values == combo.values.max()]
    print("The most frequent combination of start station and end station:")
    print(pop_combo, '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    print("Total travel time: {}".format(total))

    # display mean travel time
    mean = df['Trip Duration'].mean()
    print("Mean travel time: {}".format(mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        user_types = df['User Type'].value_counts()
        print("Here is the count by user type:")
        print(user_types, '\n')
    except KeyError:
        print("No Data for User Type.\n")

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print("Here is the count by gender:")
        print(gender, '\n')
    except KeyError:
        print("No Data for Gender.\n")

    # Display earliest, most recent, and most common year of birth
    try:
        year_min = df['Birth Year'].min()
        year_max = df['Birth Year'].max()
        year_mode = df['Birth Year'].mode()[0]
        print("The earliest birth year is: {}".format(year_min))
        print("The most recent birth year is: {}".format(year_max))
        print("The most common year of birth is: {}".format(year_mode))
    except KeyError:
        print("No Data for Birth Year.\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    counter = 0
    while True:
        # Get user input
        raw = input("Do you want to see 5 lines of raw data? enter 'yes' or 'no'\n").lower()
        # Address for invalid input situation
        while raw not in ['yes', 'no']:
            raw = input("Invalid answer, please type 'yes' or 'no'\n").lower()
        if raw == 'no':
            break
        # Address the situation where the database reaches the end of the line
        if (counter + 5) >= df.shape[0]:
            print("Reaching the end, printing the remaining lines of data:\n")
            print(df.iloc[counter:])
        # Print raw data
        print("Showing 5 lines of raw data:\n")
        print(df.iloc[counter:(counter+5)])
        counter += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
