import pandas as pd

# Define the input file path
csv_file_path = 'Assignment_Timecard.csv'

# Load the CSV file data into a pandas DataFrame
df = pd.read_csv(csv_file_path)

datetime_format = '%m/%d/%Y %I:%M %p'

# Convert time columns to datetime objects
df['Time'] = pd.to_datetime(df['Time'], format = datetime_format)
df['Time Out'] = pd.to_datetime(df['Time Out'], format = datetime_format)

# Sort the DataFrame
df.sort_values(by=['Employee Name', 'Time'])

# Initialize variables
prev_employee = None
prev_shift_end = None
min_diff = pd.Timedelta(hours=1)
max_diff = pd.Timedelta(hours=10)
max_duration = pd.Timedelta(hours=14)
next_day = pd.Timedelta(days=1)

# Initialize sets for storing answers to prevent repetition
a = set()
b = set()
c = set()

for index, row in df.iterrows():
    curr_shift_start = row['Time']
    curr_shift_end = row['Time Out']

    
    if (curr_shift_end - curr_shift_start) > max_duration:
        c.add((prev_employee,row['Position ID']))

    if prev_employee is None or prev_employee != row['Employee Name']:
        prev_employee = row['Employee Name']
        prev_shift_end = curr_shift_end
        consecutive_days = 1

    else:
        time_diff = curr_shift_start - prev_shift_end

        if min_diff < time_diff < max_diff:
            b.add((prev_employee,row['Position ID']))


        # handle null values
        if(pd.notna(curr_shift_start) and pd.notna(prev_shift_end)):
            shift_gap = curr_shift_start.date() - prev_shift_end.date()
            
            if shift_gap > next_day:
                consecutive_days = 1
                
            elif shift_gap == next_day:
                consecutive_days += 1
                
            if pd.notna(curr_shift_end) and (curr_shift_end.date() - curr_shift_start.date()) == pd.Timedelta(days=1):
                consecutive_days +=1
                
        if consecutive_days == 7:
            a.add((prev_employee,row['Position ID']))

        prev_shift_end = curr_shift_end

# display output
print('Employees who have worked for 7 consecutive days:\n')

for i,j in enumerate(a):
    print(i+1,':\t',j)

print('\n\nEmployees who have less than 10 hours of time between shifts but greater than 1 hour:\n')

for i,j in enumerate(b):
    print(i+1,':\t',j)

print('\n\nEmployee who has worked for more than 14 hours in a single shift :\n')

for i,j in enumerate(c):
    print(i+1,':\t',j)
