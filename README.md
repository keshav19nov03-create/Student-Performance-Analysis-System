# Student Performance Analysis System

### A Python mini project using NumPy, Pandas and Matplotlib

## About the Project

Teachers keep student marks in spreadsheets, but finding useful information from them takes a lot of manual work. Calculating the percentage, grade, pass/fail result and rank of every student, and then finding which subject is weak, is slow and mistakes are easy to make.

This project does that work with a small Python program. It reads the marks of 60 students in five subjects from a CSV file, cleans the data, calculates the results and statistics, and saves six charts and a result file. The same program can be used on real marks by replacing the CSV file.

I made this as my Python mini project to practise working with data using NumPy, Pandas and Matplotlib.

## Features

- Reads student data from a CSV file
- Cleans the data: removes duplicate rows and fills missing marks with the subject average
- Calculates total, percentage, grade, pass/fail result and rank of every student
- Calculates mean, median, standard deviation, highest, lowest and pass percentage of every subject
- Lists the top five students and the students who need attention
- Compares the three sections of the class
- Finds how attendance and study hours are related to the percentage
- Saves six charts and a `result_report.csv` file

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Main programming language |
| NumPy | Mean, median, standard deviation, pass percentage and the trend line (`np.polyfit`) |
| Pandas | Reading the CSV, cleaning, adding columns, grouping by section and sorting |
| Matplotlib | Bar charts, histogram, scatter plot, box plot and heat map |

## Requirements

- Python 3.9 or newer
- NumPy
- Pandas
- Matplotlib 3.9 or newer

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/student-performance-analysis.git
cd student-performance-analysis
```

### 2. Install the libraries

```bash
pip install -r requirements.txt
```

### 3. Create the sample dataset (optional)

`students.csv` is already included. To create it again, run:

```bash
python generate_data.py
```

The data is made with a fixed random seed (42), so everyone gets exactly the same file.

### 4. Run the analysis

```bash
python student_analysis.py
```

Run the commands from inside the project folder, because the program reads `students.csv` and saves the charts in the `charts` folder of the current directory.

## How It Works

The program is a pipeline and every step is a separate function:

| Function | What it does |
|---|---|
| `load_data()` | Reads the CSV into a DataFrame and prints the number of missing values |
| `clean_data()` | Drops duplicate rows and fills every blank mark with the average of that subject |
| `compute_results()` | Adds Total, Percentage, Grade, Result and Rank columns |
| `subject_statistics()` | Uses NumPy to get mean, median, standard deviation, max, min and pass % of each subject |
| `correlation_report()` | Finds the correlation matrix and fits a straight line of percentage against attendance |
| `make_charts()` | Draws and saves the six charts |
| `main()` | Calls all the steps in order and prints the summary |

## Dataset

Real marks of students are private, so `generate_data.py` creates a sample dataset of 60 students. Four marks are left blank and two rows are copied on purpose, so the file has 62 rows and the cleaning step has real defects to fix.

| Column | Description |
|---|---|
| `StudentID` | Unique ID such as MCA26-001 |
| `Section` | Class section: A, B or C |
| `Attendance` | Attendance percentage (50 to 100) |
| `StudyHours` | Average hours of study per day (0.5 to 7) |
| `Python`, `DBMS`, `Networks`, `Maths`, `Communication` | Marks out of 100 in each subject |

Columns added by the program: `Total` (out of 500), `Percentage`, `Grade`, `Result` and `Rank`.

**Grading rule:** O (90 and above), A+ (80-89), A (70-79), B (60-69), C (50-59), D (40-49) and F. A student who scores below 40 in even one subject gets Fail and grade F. Students with the same percentage get the same rank.

**Important:** the dataset is made by a program for practice. It does not contain any real student's marks, so the results should not be read as facts about real students.

## Results

Output of `python student_analysis.py` on the sample data (the full output is saved in `sample_output.txt`):

- Total students: **60**, passed: **55**, failed: **5**
- Class average: **62.62%** (highest 78.00%, lowest 36.60%)
- Weakest subject: **Maths** (average 53.37)
- Students needing attention (below 50% or attendance below 75%): **15**
- Section averages: A 62.60, B 62.61, C 62.64 (almost equal)
- Correlation of attendance and percentage: **0.298**, trend line: Percentage = 0.349 x Attendance + 34.65

### Charts

The charts are saved in the `charts` folder.

| | |
|---|---|
| ![Subject-wise average marks](charts/fig1_subject_average.png) | ![Grade distribution](charts/fig2_grade_distribution.png) |
| ![Distribution of overall percentage](charts/fig3_percentage_histogram.png) | ![Attendance vs overall percentage](charts/fig4_attendance_scatter.png) |
| ![Spread of marks in each subject](charts/fig5_subject_boxplot.png) | ![Correlation matrix](charts/fig6_correlation_heatmap.png) |

## Project Structure

```text
student-performance-analysis/
├── README.md
├── requirements.txt
├── generate_data.py        # creates students.csv
├── student_analysis.py     # cleaning, calculations, charts
├── students.csv            # sample dataset (62 rows)
├── result_report.csv       # results of every student, sorted by rank
├── sample_output.txt       # console output of one run
└── charts/                 # six saved charts
```

## Limitations

- The column names in the CSV must be exactly the same as in the sample file, otherwise the program stops with an error.
- Marks are assumed to be out of 100.
- It works on one class at a time and has no login or database.

## What I Learned

- Reading and cleaning a CSV file with Pandas
- Using NumPy for statistics and for fitting a straight line
- Grouping, sorting and ranking data in a DataFrame
- Drawing and labelling different types of charts with Matplotlib
- Splitting a program into small functions
- Writing documentation for a GitHub project

## Future Scope

- Use real marks of a class (with permission) and compare different semesters
- Add a simple window with Tkinter or a web page with Streamlit so that a teacher can upload a file and see the charts
- Predict the final result of a student from internal marks, attendance and study hours using scikit-learn

## Academic Information

- **Project:** Student Performance Analysis System Using Python, NumPy, Pandas and Matplotlib
- **Submitted by:** Keshav Kumar
- **UID:** 26MCC20092
- **Program:** MCA (CC & DevOps), Section 26MCC-101
- **Semester:** 1st
- **Project guide:** Dr. Nisha Sharma
- **University:** University Institute of Computing, Chandigarh University, Punjab
- **Academic session:** 2026-27

## References

- [Python Documentation](https://docs.python.org/3/)
- [NumPy Documentation](https://numpy.org/doc/)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/)
