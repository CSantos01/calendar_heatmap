from events_extracter import events_extracter

months = {"January": 31, "February": 28, "March": 31, "April": 30, "May": 31,
          "June": 30, "July": 31, "August": 31, "September": 30, "October": 31,
          "November": 30, "December": 31}

for month in months:
    for day in range(1, months[month] + 1):
        events = events_extracter(month, day)
        print(f"{month} {day}: {events} events")