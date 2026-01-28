import datetime as dt
import pandas as pd
import os, re
import numpy as np

#################################################
# Function to get dates for the semester
#################################################

# Dictionary to map weekdays to their index
day_to_index = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}


# Function to get dates for a specific weekday
def get_dates(start, end, weekdays, year):
    """
    Returns a list of dates that fall on a specific weekday between two dates.
        - start: The start date of the semester.
        - end: The end date of the semester.
        - weekdays: Weekdays to filter the dates (e.g., 'Tue', 'Thu').
        - year: The year of the semester.
    """
    weekdaysnum = [day_to_index[day] for day in weekdays]
    start_date = dt.datetime.strptime(start + "/" + str(year), "%m/%d/%Y")
    end_date = dt.datetime.strptime(end + "/" + str(year), "%m/%d/%Y")
    dates = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() in weekdaysnum:
            dates.append(current_date.strftime("%a %m/%d"))
        current_date += dt.timedelta(days=1)
    return dates

#################################################
# Function to write table to latex
#################################################

def latex(df, filename=None):
    lines = []
    if filename is None:
        for i in range(df.shape[0]):
            lines.append(" & ".join([str(x) for x in df.iloc[i]]) + " \\\\")
        return lines
    else:
        with open(filename, "w") as f:
            for i in range(df.shape[0]):
                f.write(" & ".join([str(x) for x in df.iloc[i]]) + " \\\\\n")

#################################################
# Create syllabus
#################################################

# Initialize
sem = "spring"
class_days = ["Mon"]

# Fall semester dates
if sem == "fall":
    dates = get_dates("08/23", "12/12", class_days, 2025)
    break_ = get_dates("11/24", "11/30", class_days, 2025)
    examday = "Mon 12/15"
    add_holidays = ["Mon 09/01"]
    holiday_names = ["Labor Day"]

# Spring semester dates
if sem == "spring":
    dates = get_dates("01/17", "05/08", class_days, 2026)
    break_ = get_dates("03/30", "04/05", class_days, 2026)
    examday = "Mon 05/11"
    add_holidays = ["Mon 01/19"]
    holiday_names = ["MLK Day"]

# Set the midterm date
midterm_idx = 9

# Add final exam date
dates.append(examday)

# Collect indices for breaks, review classes, and exams
add_holidays_idx = [dates.index(add_holiday) for add_holiday in add_holidays]
break_idx = dates.index(break_[0])
final_idx = len(dates) - 1

# Create list with just lecture dates
rm_idxs = [
    break_idx,
    midterm_idx,
    final_idx,
] + add_holidays_idx
lec_dates = [date for i, date in enumerate(dates) if i not in rm_idxs]
n_lec_dates = len(lec_dates)

# If only one class day, remove the day from dates column
if len(class_days) == 1:
    dates = [date[4:] for date in dates]
    lec_dates = [date[4:] for date in lec_dates]

# Create a DataFrame with the dates
df = pd.DataFrame(
    {
        "Date": lec_dates,
        "Lecture": range(1, n_lec_dates + 1),
        "Topics": "",
        "References": "",
        "Due": "",
    },
    dtype="object",
)

#################################################
# Specify syllabus content
#################################################

# Lecture 1
df.loc[df["Lecture"] == 1, "Topics"] = "Consumer Preferences and Choice"
df.loc[df["Lecture"] == 1, "References"] = "Ch. 3-4"
#df.loc[df["Lecture"] == 1, "References"] = "3.1-3.6, 4.1-4.5"

# Lecture 2
df.loc[df["Lecture"] == 2, "Topics"] = "Demand Analysis and Consumer Welfare"
df.loc[df["Lecture"] == 2, "References"] = "Ch. 5-6"
#df.loc[df["Lecture"] == 2, "References"] = "5.1-5.4, 5.7-5.8, 6.1-6.2"

# Lecture 3
df.loc[df["Lecture"] == 3, "Topics"] = "Production, Costs, and Firm Supply"
df.loc[df["Lecture"] == 3, "References"] = "Ch. 9-11"

# Lecture 4
df.loc[df["Lecture"] == 4, "Topics"] = "Competitive Market Equilibrium"
df.loc[df["Lecture"] == 4, "References"] = "Ch. 12"

#df.loc[df["Lecture"] == 4, "References"] = "12.1–12.8"

# Lecture 5
df.loc[df["Lecture"] == 5, "Topics"] = "Welfare Analysis and Efficiency"
df.loc[df["Lecture"] == 5, "References"] = "Ch. 13"
#df.loc[df["Lecture"] == 5, "References"] = "12.9–12.10, 13.7–13.8"

# Lecture 6
df.loc[df["Lecture"] == 6, "Topics"] = "Monopoly and Market Power"
df.loc[df["Lecture"] == 6, "References"] = "Ch. 14"

# Lecture 7
df.loc[df["Lecture"] == 7, "Topics"] = "Imperfect Competition and Oligopoly"
df.loc[df["Lecture"] == 7, "References"] = "Ch. 15"

# Lecture 8
df.loc[df["Lecture"] == 8, "Topics"] = "Labor Markets"
df.loc[df["Lecture"] == 8, "References"] = "Ch. 16"

# Lecture 9
df.loc[df["Lecture"] == 9, "Topics"] = "Asymmetric Information"
df.loc[df["Lecture"] == 9, "References"] = "Ch. 18"

# Lecture 10
df.loc[df["Lecture"] == 10, "Topics"] = "Externalities and Public Goods"
df.loc[df["Lecture"] == 10, "References"] = "Ch. 19-20"

# Lecture 11
df.loc[df["Lecture"] == 11, "Topics"] = "Choice Under Uncertainty"
df.loc[df["Lecture"] == 11, "References"] = "Ch. 7"

# Lecture 12
df.loc[df["Lecture"] == 12, "Topics"] = "Introduction to Game Theory"
df.loc[df["Lecture"] == 12, "References"] = "Ch. 8"

# Lecture 13
df.loc[df["Lecture"] == 13, "Topics"] = "Add. Topics/Review"
df.loc[df["Lecture"] == 13, "References"] = ""


# Problem set due dates
df.loc[df["Lecture"] == 3, "Due"] = "PS 1"
df.loc[df["Lecture"] == 6, "Due"] = "PS 2"
df.loc[df["Lecture"] == 9, "Due"] = "PS 3"
df.loc[df["Lecture"] == 12, "Due"] = "PS 4"

#################################################
# Put it all together
#################################################

# Add back all original dates
df_tmp = pd.DataFrame({"Date": dates})
df = df_tmp.merge(df, on="Date", how="left")

# Add description for additional dates
# df.loc[break_idx, "Date"] = ""
if sem == "fall":
    df.loc[break_idx, "Topics"] = "Fall Recess"
if sem == "spring":
    df.loc[break_idx, "Topics"] = "Spring Recess"
for i, add_holiday in enumerate(add_holidays_idx):
    df.loc[add_holiday, "Date"] = dates[add_holiday]
    df.loc[add_holiday, "Topics"] = holiday_names[i]
df.loc[midterm_idx, "Topics"] = "Midterm Exam"
df.loc[final_idx, "Topics"] = "Final Exam"

# Replace missing values with empty strings
df = df.fillna("")

#################################################
# Create latex table
#################################################

# Get the latex lines
lines = latex(df)

# Special multicolumn rows
splrows = df[df["Lecture"] == ""].index
for row in splrows:
    lines[row] = (
        df.loc[row, "Date"]
        + " & "
        + f'\\multicolumn{{3}}{{c}}{{{df.loc[row, "Topics"]}}}'
        + " & "
        + " \\\\"
    )

# # Add horizontal lines
for row in range(len(lines)-1):
    lines[row] += "\\Xhline{1.75\\arrayrulewidth} "

# Remove \\\\ from the last line
lines[-1] = lines[-1].replace(" \\\\", "")

# Write to file
with open("syllabus/schedule.tex", "w") as f:
    for line in lines:
        f.write(line + "\n")

#################################################