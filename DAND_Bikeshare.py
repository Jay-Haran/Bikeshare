import pandas as pd
import calendar

#Making a combined data frame in pandas.

#Loading in the csv files
chicago_data= pd.read_csv("chicago.csv")
new_york_data=pd.read_csv("new_york_city.csv")
washington_data=pd.read_csv("washington.csv")

#Test_data for faster testing purposes
#n = 10000
#new_york_data = pd.read_csv("new_york_city.csv",skiprows=lambda i: i % n != 0)
#washington_data=pd.read_csv("washington.csv",skiprows=lambda i: i % n != 0)
#chicago_data=pd.read_csv("chicago.csv", skiprows=lambda i: i % n != 0)

#Adding city name as a column so we can filter the data back after
chicago_data['City']="Chicago"
new_york_data['City']="New York"
washington_data['City']="Washington"

#Adding the data frames together to enable us to add common columns for further analysis
#This will aid with analysis and readability later
city_set=[chicago_data, new_york_data, washington_data]
city_data=pd.concat(city_set)

#Converting months to time and adding distinct columns for analysis
city_data['Start Time']=pd.to_datetime(city_data["Start Time"])
city_data['End Time']=pd.to_datetime(city_data["End Time"])

city_data['Date']=city_data["Start Time"].dt.date
city_data['Month']=city_data["Start Time"].dt.month
city_data['Month'] = city_data['Month'].apply(lambda x: calendar.month_name[x])
city_data['Day']=city_data["Start Time"].dt.weekday_name
city_data['Hour']=city_data["Start Time"].dt.hour

#Removing seconds from time for readability
city_data['Start Time']=city_data["Start Time"].map(lambda t: t.strftime('%H:%M'))
city_data['End Time']=city_data["End Time"].map(lambda t: t.strftime('%H:%M'))

#Adding journey and total trips column to enable better analysis
city_data["Journey"]=city_data["Start Station"] + " to " + city_data["End Station"]
city_data["Total Trips"]=1

#Filtering back down to cities
#Total trips column was added to so program can output tables which give the user more information
chicago=city_data.loc[city_data['City'] == "Chicago"].copy()
newyork=city_data.loc[city_data['City'] == "New York"].copy()
washington=city_data.loc[city_data['City'] == "Washington"].copy()

#Following functions are to gather user input

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
        # Capitalise first letter of time period since that is how it is represented in month column
        Month_filter = time_period.capitalize()

        frame = city.loc[city['Month'] == Month_filter].copy()

    elif time_period in days:
        Day_filter = time_period.capitalize()

        frame = city.loc[city['Day'] == Day_filter].copy()

    else:
        frame=city

    return(frame)

#Following functions retrieve most popular month, day and hour

def popular_month(frame):
    '''
    Args:
        1. frame: Data frame consisting of data for city and time period specified by user
    Returns:
        A summary of trips by month
    '''

    frame_month_summary = frame.groupby("Month").sum()
    frame_month_summary = frame_month_summary.reindex(["January", "February", "March", "April", "May", "June"])

    highest_month = frame_month_summary.idxmax(axis=0).loc["Total Trips"]
    lowest_month = frame_month_summary.idxmin(axis=0).loc["Total Trips"]

    highest_value = frame_month_summary["Total Trips"].max()
    lowest_value = frame_month_summary["Total Trips"].min()

    # Creating a column with trips separated by commas for thousands for readability
    frame_month_summary["Trips"] = frame_month_summary['Total Trips'].map('{:,.0f}'.format)

    print(frame_month_summary[["Trips"]])
    print("\nMost popular month: {} ( {:,} trips)".format(highest_month, highest_value))
    print("Least popular month: {}  ({:,} trips)".format(lowest_month, lowest_value))


def popular_day(frame, time_period):
    '''
    Args:
        1. frame: Data frame consisting of data for city and time period specified by user
        2. time_period: time period specified by user
    Returns:
        A summary of trips by day
    '''
    #make the set months to enable us to write a simple if statement
    months = ["january", "february", "march", "april", "may", "june"]

    # Filter data frame by assigning "frame" to only include data from specified month.
    #if time_period in months:

    frame_day_summary = frame.groupby("Day").sum()
    frame_day_summary = frame_day_summary.reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    highest_day = frame_day_summary.idxmax(axis=0).loc["Total Trips"]
    lowest_day = frame_day_summary.idxmin(axis=0).loc["Total Trips"]

    highest_value = frame_day_summary["Total Trips"].max()
    lowest_value = frame_day_summary["Total Trips"].min()

    # Creating a column with trips separated by commas for thousands for readability
    frame_day_summary["Trips"] = frame_day_summary['Total Trips'].map('{:,.0f}'.format)

    # Separating case where user specifies month with period where user does not specify month so we can give the user a
    # clearer description.
    if time_period == "none":
        print(frame_day_summary[["Trips"]])
        print("\nMost popular day: {} ({:,} trips)".format(highest_day,highest_value))
        print("Least popular day: {} ({:,} trips)".format(lowest_day,lowest_value))

    if time_period in months:
        # Capitalising for printing in the string
        print_period = time_period.title()

        print(frame_day_summary[["Trips"]])
        print("\nMost popular day for {} :{} ({:,} trips)".format(print_period, highest_day,highest_value))
        print("Least popular day for {}: {} ({:,} trips)".format(print_period,lowest_day,lowest_value))

def popular_hour(frame, time_period):
    '''
    Args:
        1. frame: Data frame consisting of data for city and time period specified by user
        2. time_period: time period specified by user

    Returns:
        Most and least popular hour with the option for the user to request a full summary of trips by hour
    '''
    months = ["january", "february", "march", "april", "may", "june"]
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    frame_hour_summary = frame.groupby("Hour").sum()

    # Renaming index/hours in am/pm format. I chose to write it and not implement a function for readability
    frame_hour_summary.rename(
        {0: "12am", 1: "1am", 2: "2am", 3: "3am", 4: "4am", 5: "5am", 6: "6am", 7: "7am", 8: "8am", 9: "9am",
         10: "10am",
         11: "11am", 12: "12pm", 13: "1pm", 14: "2pm", 15: "3pm", 16: "4pm", 17: "5pm", 18: "6pm", 19: "7pm",
         20: "8pm", 21: "9pm", 22: "10pm", 23: "11pm"}, inplace=True)

    highest_hour = frame_hour_summary.idxmax(axis=0).loc["Total Trips"]
    lowest_hour = frame_hour_summary.idxmin(axis=0).loc["Total Trips"]

    highest_value = frame_hour_summary["Total Trips"].max()
    lowest_value = frame_hour_summary["Total Trips"].min()

    # Creating a column with trips separated by commas for thousands for readability
    frame_hour_summary["Trips"] = frame_hour_summary['Total Trips'].map('{:,.0f}'.format)

    if time_period == "none":

        print("\nMost popular starting hour: {} ({:,} trips)".format(highest_hour,highest_value))
        print("Least popular starting hour: {} ({:,} trips)".format(lowest_hour,lowest_value))
    if time_period in months + days:
        # Capitalising for printing in the string
        print_period = time_period.title()

        print("\nMost popular starting hour for {}: {} ({:,} trips)".format(print_period,highest_hour,highest_value))
        print("Least popular starting hour for {}: {} ({:,} trips)".format(print_period,lowest_hour,lowest_value))

    #Extra code if user wants detailed breakdown

    detailed_time_breakdown= "initialised"

    while detailed_time_breakdown not in ("yes", "no"):

        detailed_time_breakdown=input("\nWould you like to see total trips for every hour of the day? Type 'yes' or 'no'.\n" )

        detailed_time_breakdown.lower()
        detailed_time_breakdown = detailed_time_breakdown.replace(" ", "")

        if detailed_time_breakdown == "no":
            break

        if detailed_time_breakdown == "yes":
            print(frame_hour_summary[["Trips"]])

        else:
            print("\nI am sorry I do not recognise that input")
            
#Following functions return information about trips such as duration and geography of trips.

def trip_duration(frame):

    '''
    Args:
        1. frame: Data frame consisting of data for city and time period specified by user

    Returns:
        Total trip duration and average trip duration for a time period and city specified by user.
    '''

    # Calculating total duration and getting it in the format hours,minutes and seconds.

    total_duration = frame["Trip Duration"].sum()

    total_duration_minutes, total_duration_seconds = divmod(total_duration, 60)
    total_duration_hours, total_duration_minutes = divmod(total_duration_minutes, 60)

    # Calculating average duration and getting it in the format hours,minutes and seconds.

    average_duration = frame["Trip Duration"].mean()

    average_duration_minutes, average_duration_seconds = divmod(average_duration, 60)
    average_duration_hours, average_duration_minutes = divmod(average_duration_minutes, 60)

    print("\nTotal duration:  {:.0f} hours {:.0f} minutes and {:.0f} seconds".format(total_duration_hours,
                                                                                        total_duration_minutes,
                                                                                        total_duration_seconds))

    print("Average duration: {:.0f} hours {:.0f} minutes and {:.0f} seconds".format(average_duration_hours,
                                                                                          average_duration_minutes,
                                                                                          average_duration_seconds))

def popular_stations(frame):
    '''
    Args:
        1. frame: Data frame consisting of data for city and time period specified by user

    Returns:
        Most and least popular start station and most popular journey
    '''
    most_popular_start = frame["Start Station"].max()
    least_popular_start = frame["Start Station"].min()

    most_popular_end = frame["End Station"].max()
    least_popular_end = frame["End Station"].min()

    most_popular_journey = frame["Journey"].max()

    print("\nMost popular start station: {}".format(most_popular_start))
    print("Least popular start station: {}".format(least_popular_start))
    print("\nMost popular end station: {}".format(most_popular_end))
    print("Least popular end station: {}".format(least_popular_end))
    print("\nMost popular journey: {}".format(most_popular_journey))

#Following functions return information about the user

def users(frame):
    '''
        Args:
            1. frame: Data frame consisting of data for city and time period specified by user

        Returns:
            Counts for each user type
    '''

    user_summary = frame.groupby("User Type").sum()
    user_summary["Trips"] = user_summary['Total Trips'].map('{:,.0f}'.format)
    print("\n", user_summary[["Trips"]])
    
def gender(frame):
    '''
        Args:
            1. frame: Data frame consisting of data for city and time period specified by user

        Returns:
            Counts for each gender
    '''

    gender_summary = frame.groupby("Gender").sum()
    gender_summary["Trips"] = gender_summary['Total Trips'].map('{:,.0f}'.format)
    print("\n", gender_summary[["Trips"]])

def birth_years(frame):
    '''   Args:
            1. frame: Data frame consisting of data for city and time period specified by user

        Returns:
            Earliest, latest and most popular birth year'''

    #Find the birth year for the oldest and youngest user and also the most popular birth year
    oldest = frame["Birth Year"].min()
    youngest = frame["Birth Year"].max()
    popular = int(frame.mode()["Birth Year"][0])

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

    summary_frame= frame[["City", "Start Station", "End Station","Date", "Start Time", "End Time", "User Type"]]

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

    #Get the month the user wants to filter by if they choose month
    if time_period == "month":

        time_period=get_month()

    if time_period== "day":

        time_period = get_day()

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
    if str (city["City"][0])!= "Washington":

        #Outputs gender count on user for specified city and time frame
        gender(frame)

        # Outputs oldest, most recent and most common birth year
        birth_years(frame)

    # Display five lines of data at a time if user specifies
    #
    display_data(frame)


    #Restart?
    restart = input('Would you like to restart? Type \'yes\' or \'no\'.')
    if restart.lower() == 'yes':
        statistics()


if __name__ == "__main__":
	statistics()
