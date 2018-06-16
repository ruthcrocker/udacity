import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city = None
    while city not in ('chicago', 'new york city', 'washington'):
        city = input("Would you like to explore data for Chicago, New York City or Washington? ").strip().lower()
        if city in ('chicago', 'new york city', 'washington'):
            print("You have selected {}".format(city.title()))
        else:
            print("This is an invalid input, please select a valid city.")

    # get user input for month (all, january, february, ... , june)
    month = None
    while month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
        month = input("Which month would you like to filter the data to? (type 'all' for no filter) ").strip().lower()
        if month in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("You have selected {}".format(month.title()))
        else:
            print("This is an invalid input, please select a valid month (January - June).")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    while day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
        day = input("Which day of the week would you like to filter the data to? (type 'all' for no filter) ").strip().lower()
        if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print("You have selected {}".format(day.title()))
        else:
            print("This is an invalid input, please select a valid day.")

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
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
    months = ['january', 'february', 'march', 'april', 'may', 'june']

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most popular month was: {}'.format(months[popular_month - 1].title()))

    # display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    print('The most popular day was: {}'.format(popular_dow))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular start hour was: {}'.format(popular_hour))

    print("\nThis took {:.2f} seconds.".format((time.time() - start_time)))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start = df['Start Station'].mode()[0]
    print('The most popular start station was: {}'.format(pop_start))

    # display most commonly used end station
    pop_end = df['End Station'].mode()[0]
    print('The most popular end station was: {}'.format(pop_end))

    # display most frequent combination of start station and end station trip
    df['journey'] = df['Start Station'] + ' to ' + df['End Station']
    pop_combo = df['journey'].mode()[0]
    print('The most popular journey was from: \n{}'.format(pop_combo))

    print("\nThis took {:.2f} seconds.".format((time.time() - start_time)))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum() / 60 / 60 / 24
    print('The total travel time was: {} days'.format(round(total_time,2)))

    # display mean travel time
    mean_time = df['Trip Duration'].mean() / 60
    print('The mean travel time was: {} minutes'.format(round(mean_time,2)))

    print("\nThis took {:.2f} seconds.".format((time.time() - start_time)))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    users_total = df['User Type'].count()
    print('Total number of users: {}'.format(users_total))
    print('Breakdown of user types:\n{}'.format(user_types))

    if city in ('chicago', 'new york city'):
        # Display counts of gender (only for Chicago & New York City)
        gender = df['Gender'].value_counts()
        print('\nBreakdown of gender:\n{}'.format(gender))

        # Display earliest, most recent, and most common year of birth (only for Chicago & New York City)
        print('\nBreakdown of year of birth:')
        min_dob = int(df['Birth Year'].min())
        max_dob = int(df['Birth Year'].max())
        mean_dob = int(df['Birth Year'].mean())
        mode_dob = int(df['Birth Year'].mode()[0])
        print('The earliest year of birth was: {}'.format(min_dob))
        print('The most recent year of birth was: {}'.format(max_dob))
        print('The average year of birth was: {}'.format(mean_dob))
        print('The most common year of birth was: {}'.format(mode_dob))

    print("\nThis took {:.2f} seconds.".format((time.time() - start_time)))
    print('-'*40)

def raw_data(df):
    """Displays raw data at user request"""
    raw = input('\nWould you like to see the raw data?(Y/N)')
    start = 0
    while raw.lower() == 'y':
        print(df.iloc[start:start+5])
        start += 5
        raw = input('Would you like to see 5 more rows?')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
