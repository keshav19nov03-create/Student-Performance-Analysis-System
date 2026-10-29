"""Creates students.csv - a sample dataset of 60 students (fixed seed, so it is repeatable)."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 60

student_id = [f"MCA26-{i:03d}" for i in range(1, n + 1)]
section = rng.choice(["A", "B", "C"], n)
attendance = np.clip(rng.normal(80, 10, n), 50, 100).round(1)
study_hours = np.clip(rng.normal(3, 1.2, n), 0.5, 7).round(1)
ability = rng.normal(0, 1, n)

base = {"Python": 68, "DBMS": 64, "Networks": 60, "Maths": 55, "Communication": 70}
data = {"StudentID": student_id, "Section": section,
        "Attendance": attendance, "StudyHours": study_hours}
for subject, mean in base.items():
    marks = (mean + 0.35 * (attendance - 80) + 3.0 * (study_hours - 3)
             + 8 * ability + rng.normal(0, 6, n))
    data[subject] = np.clip(marks, 0, 100).round(0)

df = pd.DataFrame(data)

# a few deliberate defects so that the cleaning step has something to do
for row, col in [(5, "Maths"), (17, "DBMS"), (33, "Networks"), (48, "Python")]:
    df.loc[row, col] = np.nan
df = pd.concat([df, df.iloc[[10, 41]]], ignore_index=True)   # two duplicate rows

df.to_csv("students.csv", index=False)
print("students.csv created with", len(df), "rows")
