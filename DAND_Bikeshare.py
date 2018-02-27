import pandas as pd
import calendar

#Loading in the csv files
chicago= pd.read_csv("chicago.csv", parse_dates =["Start Time", "End Time"])
newyork=pd.read_csv("new_york_city.csv", parse_dates =["Start Time", "End Time"])
washington=pd.read_csv("washington.csv", parse_dates =["Start Time", "End Time"])

#Test_data for faster testing purposes
#n = 10000
#newyork= pd.read_csv("new_york_city.csv",skiprows=lambda i: i % n != 0,parse_dates =["Start Time", "End Time"])
#washington=pd.read_csv("washington.csv",skiprows=lambda i: i % n != 0, parse_dates =["Start Time", "End Time"] )
#chicago=pd.read_csv("chicago.csv", skiprows=lambda i: i % n != 0,parse_dates =["Start Time", "End Time"] )

#Adding trips column to enable calculating summary statistics
def counting_column(city):
    city['Trips']=1


counting_column(newyork)
counting_column(washington)
counting_column(chicago)

def get_city():
    '''Asks the user for a city and returns a filtered data frame for future functions.

    Args:
        none.
    Returns:
        (str) Data frame for particular city .
    '''

    print("Hello! Let\'s explore some US bikeshare data!")

    city = "some_city"  # To initialise the while loop which follows
    valid_city = ["chicago", "newyork", "washington"]

    # while loop used to keep repeating until user inputs valid input.

    while city not in valid_city:

        city = input('\nWould you like to see data for Chicago, New York, or Washington?\n')

        # makes string lower case and removes spaces
        city = city.lower()
        city = city.replace(" ", "")

        if city == "chicago":

            return (chicago)

        elif city == "newyork":

            return (newyork)

        elif city == "washington":

            return (washington)

        else:

            print("\nI am sorry I do not recognise that city")

def get_time_period():
    '''Asks the user for a time period and returns the specified filter.

    Args:
        none.
    Returns:
        Time period which the user wishes to filter by
    '''

    time_period="some_period"   #To initialise the while loop which follows
    valid_time_periods=["month", "day", "none"]

    #while loop used to keep repeating until user inputs valid input.

    while time_period not in valid_time_periods:


        time_period = input('\nWould you like to filter the data by month, day, or not at'
                        ' all? Type "none" for no time filter.\n')

        # makes string lower case and removes spaces to capture a wider variety of user input
        time_period = time_period.lower()
        time_period = time_period.replace(" ", "")

        if time_period in valid_time_periods:
            return (time_period)

        else:
            print("\nI am sorry I do not recognise that time period")

def get_month():
    '''Asks the user for a month and returns the specified month.

    Args:
        none.
    Returns:
        Month which the user wishes to filter by
    '''

    month = "some_month"  # To initialise the while loop which follows
    valid_months = ["january", "february", "march", "april", "may", "june"]

    #while loop used to keep repeating until user inputs valid input.

    while month not in valid_months:

        month = input('\nWhich month? January, February, March, April, May, or June?\n')

        # makes string lower case and removes spaces to capture a wider variety of user input
        month = month.lower()
        month = month.replace(" ", "")

        if month in valid_months:
            return(month)

        else:
            print("\nI am sorry I do not recognise that month")

def get_day():
    '''Asks the user for a day and returns the specified day.

    Args:
        none.
    Returns:
        The day which the user wishes to filter by
    '''

    day = "some_day"  # To initialise the while loop which follows
    valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    while day not in valid_days:

        day = input('\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday\n')

        # makes string lower case and removes spaces to capture a wider variety of user input
        day = day.lower()
        day = day.replace(" ", "")

        if day in valid_days:
            return (day)

        else:
            print("\nI am sorry I do not recognise that day")
            
#Following function is to create a data frame which is filtered by the time period the user specifies

def time_classifier(city, time_period):
    '''
    Args:
        City and time period specified by user
    Returns:
        Filters the data frame by specified time period
    '''


    months = ["january", "february", "march", "april", "may", "june"]
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    # Filter data frame to only include data from specified time period

    if time_period in months:

        converter={"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june":6}

        frame=city.loc[city['Start Time'].dt.month == converter[time_period]]


    elif time_period in days:

        frame = city.loc[city['Start Time'].dt.weekday_name == time_period.capitalize]

    else:
        frame=city

    return(frame)

#Following functions retrieve most popular month, day and hour

def popular_month(frame):
    '''
    Args:
        1. frame: Data frame consisting of data for city and time period specified by user
    Returns:
        Most and least popular month
    '''

    print("\nLoading month statistics")

    highest_month=frame.groupby(frame['Start Time'].dt.strftime('%B'))['Trips'].sum().idxmax(axis=0)
    highest_value=frame.groupby(frame['Start Time'].dt.strftime('%B'))['Trips'].sum().max()

    lowest_month = chicago.groupby(chicago['Start Time'].dt.strftime('%B'))['Trips'].sum().idxmin(axis=0)
    lowest_value = chicago.groupby(chicago['Start Time'].dt.strftime('%B'))['Trips'].sum().min()

    print("\nMost popular month: {} ( {:,} trips)".format(highest_month, highest_value))
    print("Least popular month: {}  ({:,} trips)".format(lowest_month, lowest_value))


def popular_day(frame, time_period):
    '''
    Args:
        1. frame: Data frame consisting of data for city and time period specified by user
        2. time_period: time period specified by user
    Returns:
        Most and least popular day for period specified by user
    '''

    print("\nLoading day statistics")

    highest_day = frame.groupby(frame['Start Time'].dt.strftime('%A'))['Trips'].sum().idxmax(axis=0)
    highest_value = frame.groupby(frame['Start Time'].dt.strftime('%A'))['Trips'].sum().max()

    lowest_day = frame.groupby(frame['Start Time'].dt.strftime('%A'))['Trips'].sum().idxmin(axis=0)
    lowest_value = frame.groupby(frame['Start Time'].dt.strftime('%A'))['Trips'].sum().min()

    # Separating case where user specifies month with period where user does not specify month so we can give the user a
    # clearer description.

    # make the set months to enable us to write a simple if statement
    months = ["january", "february", "march", "april", "may", "june"]

    if time_period == "none":
        print("\nMost popular day: {} ({:,} trips)".format(highest_day,highest_value))
        print("Least popular day: {} ({:,} trips)".format(lowest_day,lowest_value))

    elif time_period in months:
        # Capitalising for printing in the string
        print_period = time_period.title()

        print("\nMost popular day for {} : {} ({:,} trips)".format(print_period, highest_day,highest_value))
        print("Least popular day for {}: {} ({:,} trips)".format(print_period,lowest_day,lowest_value))

def popular_hour(frame, time_period):
    '''
    Args:
        1. frame: Data frame consisting of data for city and time period specified by user
        2. time_period: time period specified by user

    Returns:
        Most and least popular hour with number of trips
    '''
    print("\nLoading hour statistics")

    highest_hour = frame.groupby(frame['Start Time'].dt.strftime('%H'))['Trips'].sum().idxmax(axis=0)
    highest_value = frame.groupby(frame['Start Time'].dt.strftime('%H'))['Trips'].sum().max()

    lowest_hour = frame.groupby(frame['Start Time'].dt.strftime('%H'))['Trips'].sum().idxmin(axis=0)
    lowest_value = frame.groupby(frame['Start Time'].dt.strftime('%H'))['Trips'].sum().min()

    months = ["january", "february", "march", "april", "may", "june"]
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    if time_period == "none":

        print("\nMost popular starting hour: {} ({:,} trips)".format(highest_hour,highest_value))
        print("Least popular starting hour: {} ({:,} trips)".format(lowest_hour,lowest_value))

    elif time_period in months + days:
        # Capitalising for printing in the string
        print_period = time_period.title()

        print("\nMost popular starting hour for {}: {} ({:,} trips)".format(print_period,highest_hour,highest_value))
        print("Least popular starting hour for {}: {} ({:,} trips)".format(print_period,lowest_hour,lowest_value))
            
#Following functions return information about trips such as duration and geography of trips.

def trip_duration(frame):

    '''
    Args:
        1. frame: Data frame consisting of data for city and time period specified by user

    Returns:
        Total trip duration and average trip duration for a time period and city specified by user.
    '''

    # Calculating total duration and getting it in the format hours,minutes and seconds.

    print('\n Loading duration statistics')
    total_duration = frame["Trip Duration"].sum()

    total_duration_minutes, total_duration_seconds = divmod(total_duration, 60)
    total_duration_hours, total_duration_minutes = divmod(total_duration_minutes, 60)

    # Calculating average duration and getting it in the format hours,minutes and seconds.

    average_duration = frame["Trip Duration"].mean()

    average_duration_minutes, average_duration_seconds = divmod(average_duration, 60)
    average_duration_hours, average_duration_minutes = divmod(average_duration_minutes, 60)

    print("\nTotal duration:  {:,} hours {:.0f} minutes and {:.0f} seconds".format(total_duration_hours,
                                                                                        total_duration_minutes,
                                                                                        total_duration_seconds))

    print("Average duration: {:,} hours {:.0f} minutes and {:.0f} seconds".format(average_duration_hours,
                                                                                          average_duration_minutes,
                                                                                          average_duration_seconds))

def popular_stations(frame):
    '''
    Args:
        1. frame: Data frame consisting of data for city and time period specified by user

    Returns:
        Most and least popular start station and most popular journey
    '''

    print('\n Loading geographical statistics')

    most_popular_start = frame["Start Station"].max()
    least_popular_start = frame["Start Station"].min()

    most_popular_end = frame["End Station"].max()
    least_popular_end = frame["End Station"].min()

    most_popular_journey = frame.groupby(["Start Station", "End Station"])['Trips'].sum().idxmax()

    print("\nMost popular start station: {}".format(most_popular_start))
    print("Least popular start station: {}".format(least_popular_start))
    print("\nMost popular end station: {}".format(most_popular_end))
    print("Least popular end station: {}".format(least_popular_end))
    print("\nMost popular journey: {} to {}".format(most_popular_journey[0], most_popular_journey[1]))

#Following functions return information about the user

def users(frame):
    '''
        Args:
            1. frame: Data frame consisting of data for city and time period specified by user

        Returns:
            Counts for each user type
    '''

    print('\n Loading user statistics')

    user_summary = frame.groupby("User Type").sum()
    user_summary["Trips"] = user_summary['Trips'].map('{:,.0f}'.format)
    print("\n", user_summary[["Trips"]])
    
def gender(frame):
    '''
        Args:
            1. frame: Data frame consisting of data for city and time period specified by user

        Returns:
            Counts for each gender
    '''

    print('\n Loading gender statistics')

    gender_summary = frame.groupby("Gender").sum()
    gender_summary["Trips"] = gender_summary['Trips'].map('{:,.0f}'.format)
    print("\n", gender_summary[["Trips"]])

def birth_years(frame):
    '''   Args:
            1. frame: Data frame consisting of data for city and time period specified by user

        Returns:
            Earliest, latest and most popular birth year'''

    print('\n Loading birth year statistics')

    #Find the birth year for the oldest and youngest user and also the most popular birth year
    oldest = frame["Birth Year"].min()
    youngest = frame["Birth Year"].max()
    popular = int(frame["Birth Year"].mode()[0])

    print("\nEarliest Birth Year: {:.0f}".format(oldest))
    print("Most Recent Birth Year: {:.0f}".format(youngest))
    print("Most Popular Birth Year: {}".format(popular))

def display_data(frame):
    '''
    Args:
        1. frame: Data frame consisting of data for city and time period specified by user

    Returns:
    Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.
    '''

    summary_frame= frame[["Start Station", "End Station","Start Time", "Trip Duration", "User Type"]]

    first_line=0

    display = input('\nWould you like to view individual trip data?''Type \'yes\' or \'no\'.\n ')

    #Makes case lower and removes spaces to capture a wider variety of user input
    display.lower()
    display = display.replace(" ", "")

    #While loop to prompt user to enter yes or no if they enter something else
    while display not in ["yes", "no"]:

        print("\nI am sorry I do not recognise that input")

        display = input('\nWould you like to view individual trip data?''Type \'yes\' or \'no\'. \n')

        display.lower()
        display = display.replace(" ", "")

    if display == "no":
            return

    while display == "yes" :

        while display not in ["yes", "no"]:

            print("\nI am sorry I do not recognise that input")

            display = input('\nWould you like to view individual trip data?''Type \'yes\' or \'no\'.\n ')

            display.lower()
            display = display.replace(" ", "")

        if display == "no":
            break

        print(summary_frame[first_line: first_line + 5])


        first_line+=5

        display = input('\nWould you like to view 5 more lines of individual trip data?''Type \'yes\' or \'no\'.\n ')



def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.

    Args:
        none.
    Returns:
        none.
    '''

    # Filter by city (Chicago, New York, Washington)
    city = get_city()

    # Filter by time period (month, day, none)
    time_period = get_time_period()

    #Find the specific time frame user wants to filter by
    if time_period == "none":

        time_period=time_period

    if time_period == "month":

        time_period=get_month()

    if time_period== "day":

        time_period=get_day()

    #Time classifier is implemented to filter the data frame
    frame=time_classifier(city, time_period)


    # Outputs most popular month
    if time_period == 'none':
        popular_month(frame)

    #Outputs most popular day for time period specified by user
    if time_period == 'none' or 'month':
        popular_day(frame, time_period)

    #Outputs most popular hour for tie period specified by user
    if time_period == 'none' or 'month' or 'day':
        popular_hour(frame, time_period)

    # Outputs total and average trip duration
    trip_duration(frame)

    # Outpurs the most popular start station, end station and journey
    popular_stations(frame)

    # Outputs counts of each user type
    users(frame)


    #Washington not included due to lack of data on users
    if str (city) != "washington":

        #Outputs gender count on user for specified city and time frame
        gender(frame)

        # Outputs oldest, most recent and most common birth year
        birth_years(frame)

    # Display five lines of data at a time if user specifies
    #
    display_data(frame)


    #Restart?
    restart = input('\n Would you like to restart? Type \'yes\' or \'no\'.')
    if restart.lower() == 'yes':
        statistics()


if __name__ == "__main__":
	statistics()