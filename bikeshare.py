import time
import pandas as pd


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# I ran the below code commented out code to do sanity check on data and found:
# Chicago has NaN values for "Gender" and "Birth Year"
# New York City has NaN values for "User Type", "Gender" and "Birth Year"
# Washington does have NaN values and doesn't have a "Gender" and "Birth Year" column

# chicago = pd.read_csv("chicago.csv")
# new_york_city = pd.read_csv("new_york_city.csv")
# washington = pd.read_csv("washington.csv")
# print("NaN values in chicago, by column\n {}".format(chicago.isnull().sum()))
# print("NaN values in new_york_city, by column\n {}".format(new_york_city.isnull().sum()))
# print("NaN values in washington, by column\n {}".format(washington.isnull().sum()))

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Set this option to display all columns when printing
pd.set_option('display.max_columns', None)

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# month_list start with all at index 0, so there is no need to offset the index in the code, i.e january has index 1
month_list = ["all",
              "january",
              "february",
              "march",
              "april",
              "may",
              "june",
              ]

day_list = ["monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            "all"
            ]

city_list = ["chicago", "new york city", "washington"]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bike share data!')

    # Get the user input for the city
    gf_city = input("Please select the city that you want the data from, you options are: \n"
                    "Chicago\n"
                    "New York City\n"
                    "Washington\n"
                    ).lower()

    if gf_city not in city_list:
        while True:
            gf_city = input("\n"
                            "That is not a valid entry, please select one of the below options: \n"
                            "Chicago\n"
                            "New York City\n"
                            "Washington\n"
                           ).lower()
            if gf_city in city_list:
                break

    # Get the user input for the month
    gf_month = input("\n"
                     "Please select the month that you want the data from, you options are: \n"
                     "January, February, March, April, May, June or All\n"
                    ).lower()

    if gf_month not in month_list:
        while True:
            gf_month = input("\n"
                             "That is not a correct entry, please select one of the below options: \n"
                             "January, February, March, April, May, June, July or All\n"
                            ).lower()
            if gf_month in month_list:
                break

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    gf_day = input("\n"
                   "Please select the day that you want the data from, you options are: \n"
                   "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All \n"
                  ).lower()

    if gf_day not in day_list:
        while True:
            gf_day = input("\n"
                           "That is not a correct entry, please select one of the below options: \n"
                           "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All\n "
                          ).lower()
            if gf_day in day_list:
                break
    print('-' * 40)
    return gf_city, gf_month, gf_day


def load_data(ld_city, ld_month, ld_day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) ld_city - name of the city to analyze
        (str) ld_month - name of the month to filter by, or "all" to apply no month filter
        (str) ld_day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        ld_df - Pandas DataFrame containing city data filtered by month and day
    """
    # Read values from CSV file
    ld_df = pd.read_csv(CITY_DATA[ld_city])

    # Covert "Start Time" from string to date_time
    ld_df['Start Time'] = pd.to_datetime(ld_df['Start Time'])

    # Create two new columns "month" and "day" which will be used for filtering
    ld_df['month'] = ld_df['Start Time'].dt.month
    ld_df['day'] = ld_df['Start Time'].dt.weekday
    ld_df['hour'] = ld_df['Start Time'].dt.hour

    # Filter by month if applicable
    if ld_month != 'all':
        # use the index of the months list to get the corresponding int

        ld_month = month_list.index(ld_month)

        # filter by month to create the new dataframe
        ld_df = ld_df[ld_df['month']== ld_month]

    # Filter by day of week if applicable
    if ld_day != 'all':
        # Find weekday as a integer, no offset needed as "all" is in position 0
        ld_weekday = day_list.index(ld_day)
        # filter by day of week to create the new dataframe
        ld_df = ld_df[ld_df['day'] == ld_weekday]
    return ld_df


def time_stats(ts_df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    ts_most_common_month_int = int(ts_df['month'].mode())
    print("The most common month is {}".format(month_list[ts_most_common_month_int]))

    # Display the most common day of week
    ts_most_common_day_int = int(ts_df['day'].mode())
    print("The most common day is {}".format(day_list[ts_most_common_day_int]))

    # Display the most common start hour
    ts_most_common_hour_int = int(ts_df['hour'].mode())
    print("The most common hour is {}".format(ts_most_common_hour_int))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(ss_df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Find the most commonly used start station
    ss_most_common_start_station = ss_df['Start Station'].mode()[0]
    ss_most_common_start_station_count = ss_df.groupby(['Start Station'])['Start Station'].count().max()
    print("The most common start station is {} with a count of {}\n"
          .format(ss_most_common_start_station,ss_most_common_start_station_count ))

    # Find the most commonly used end station
    ss_most_common_end_station = ss_df['End Station'].mode()[0]
    ss_most_common_end_station_count = ss_df.groupby(['End Station'])['End Station'].count().max()
    print("The most common end station is {} with a count of {}\n"
          .format(ss_most_common_end_station, ss_most_common_end_station_count))

    # Display most frequent combination of start station and end station trip
    ss_most_common_start_end_combination = ss_df.groupby(['Start Station','End Station']).size().idxmax()
    ss_most_common_start_end_combination_count = ss_df.groupby(['Start Station','End Station']).size().max()
    print('The most common Start - End Station combination is: \n{} and {} \nwith a count of {} '
          .format(ss_most_common_start_end_combination[0], ss_most_common_start_end_combination[1],
          ss_most_common_start_end_combination_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(tds_df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate the total travel time
    tsd_total_trip_duration_hrs = tds_df['Trip Duration'].sum()/3600
    print("The total trip duration was {} Hrs".format(tsd_total_trip_duration_hrs))

    # Calculate the mean travel time
    tsd_mean_trip_duration_min = tds_df['Trip Duration'].mean()/60
    print("The mean trip duration was {} Minutes".format(tsd_mean_trip_duration_min))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(us_df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    us_user_types_counts = us_df.groupby(['User Type'])['User Type'].count()
    print('The user type counts are:')
    for i in range(0,len(us_user_types_counts) ):
        print("User {} has a count of {}".format(us_user_types_counts.index[i], us_user_types_counts[i]))
    print('\n')
    # Display counts of gender
    print('Gender data is:')
    try:
        us_gender_counts = us_df.groupby(['Gender'])['Gender'].count()
        print('The gender counts are:')
        for i in range(0,len(us_gender_counts) ):
            print("User {} has a count of {}".format(us_gender_counts.index[i], us_gender_counts[i]))
    except KeyError:
        print('Gender data is not available for this city')
    finally:
        # Display earliest, most recent, and most common year of birth
        print('\nThe birth year statistics are:')
        try:
            us_birth_year_min = int(us_df['Birth Year'].min())
            us_birth_year_max = int(us_df['Birth Year'].max())
            us_birth_year_most_common = int(us_df['Birth Year'].mode())
            print('The earliest year is is {}'.format(us_birth_year_min))
            print('The latest year is {}'.format(us_birth_year_max))
            print('The most common year is {}'.format(us_birth_year_most_common))
        except KeyError:
            print('Birth date data is not available')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def raw_data(rd_df):
    """Prints 5 lines of raw data."""
    start_index = 0
    stop_index = 5
    yes_no_list = ['yes', 'no']
    print('\nGetting raw data...\n')
    start_time = time.time()
    while True:
        yes_no_input = input('Would you like to print 5 lines of data enter "yes" or "no" \n').lower()
        if yes_no_input not in yes_no_list:
            while True:
                yes_no_input = input('That is not a valid entry please enter "yes" or "no" \n').lower()
                if yes_no_input in yes_no_list:
                    break
        if yes_no_input == 'yes':
            print('\nFiltered raw data, records {} to {}'.format(start_index, stop_index))
            print(rd_df[start_index:stop_index])
            start_index += 5
            stop_index += 5
        else:
            break
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

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

