import time
import pandas as pd
import numpy as np
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! \n')
    
    #  get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    print("(chicago, new york city, washington) which of these cities would you like to explore?")
    city = input("Enter name of city here: ").lower()
    while city not in CITY_DATA:
        print('\nOOPS!! Seems your input was invalid, please try again and enter a valid city')
        city = input("Enter name of city here: ").lower()  
        
    #  get user input for month (all, january, february, ... , june)
    while True:
        print("\nwhich month (from january to june) would you like to explore?"
              " enter 'all' if you would like to explore all 6 months\n")
        
        month = input('enter (january, february, march, april, may, june or all): ').lower()
        if month not in MONTHS:
             print('\nOOPS!! Seems your input was invalid, please try again and enter a valid month')
             continue
        else:
            break
            
       
    #  get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednessday','thursday', 'friday','saturday', 'sunday', 'all']
    while True:
        print("\n\n\nwhich day(from monday to sunday) would you like to explore?"
              " enter 'all' if you would like to explore all days\n")
        
        day = input('enter (sunday, monday, tuesday, wednessday, thursday, friday, saturday or all): ').lower()
        if day not in days:
             print('\n\nOOPS!! Seems your input was invalid, please try again and enter a valid day')
             continue
        else:
            break

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
    # load the data into the dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert the Start Time column to DateTime data type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Create new column 'month' and 'day' from 'Start Time'
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # Filter df by month if specified
    if month != 'all':
        month = MONTHS.index(month) + 1
        df = df[df['month'] == month]
    
    # Filter df by day if specified
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    print('The Most Common Month Is: {}'.format(df['month'].mode()[0]))

    # Display the most common day of week
    print('The Most Common Day Is: {}'.format( df['day_of_week'].mode()[0]) )

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The Most Common Hour Is: {}'.format( df['hour'].mode()[0]) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print('The Most Common Start Station Is: {}'.format(df['Start Station'].mode()[0]))

    print('The Most Common End Station Is: {}'.format(df['End Station'].mode()[0]))

    # Display most frequent combination of start station and end station trip
    combination_station = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count')
    freq_combo = combination_station.loc[ combination_station['count'].idxmax(), ['Start Station','End Station'] ]
    print('({}) to ({}) is the most frequent trip combination'.format(freq_combo['Start Station'], freq_combo['End Station']))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    secs = df['Trip Duration'].sum()
    print('Total Travel Time of {} seconds, which is over {} days of travelling!!!'.format(secs, secs//86400))

    print('Average Travel Time of {} seconds'.format(df['Trip Duration'].mean()) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #  Display counts of user types
    print('HERE IS THE DATA ON USER TYPES:')
    print(df['User Type'].value_counts().to_frame())

    #  Display counts of gender
    print('\nHERE IS THE DATA ON GENDER AND BIRTH YEAR:')
    if city != 'washington':
        print(df['Gender'].value_counts().to_frame())

    # Display earliest, most recent, and most common year of birth
        print('\n\nBIRTHYEAR:')
        print('The Oldest User Was Born In:',int(df['Birth Year'].min()) )
        print('The Youngest User Was Born In:',int(df['Birth Year'].max()) )
        print('The Most Common Year Of Birth Is:',int(df['Birth Year'].mode()[0]))
    else:
        print('Data not avaliable for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """ Displays raw data to the user, upon their request."""
    # Start from row 0
    row = 0 
    user_input = input("Would you like to see 5 rows of raw data? (please type yes or no): ").lower()
    while True:
        if user_input not in ['yes', 'no']:
            print('\nInvalid input, try again!!')
            user_input = input("Would you like to see 5 rows of raw data? (please type yes or no): ").lower()
        else:
            break
    
    if user_input == 'no':
        print('Thank you bye')
    else:
        # Ensure we dont move past the number of rows, recall .shape returns number of (row,column)
        while row+5 < df.shape[0]: 
            print(df.iloc[row:row+5])
            row += 5
            new_input = input("Would you like to view 5 more rows? (type yes or no): ").lower()
            if new_input != 'yes':
                print('Thank you bye')
                break
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
