"""Student Performance Analysis System - NumPy, Pandas and Matplotlib."""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")                      # save charts to files, no window needed
import matplotlib.pyplot as plt

SUBJECTS = ["Python", "DBMS", "Networks", "Maths", "Communication"]
PASS_MARK = 40
GRADE_BINS = [0, 40, 50, 60, 70, 80, 90, 101]
GRADE_LABELS = ["F", "D", "C", "B", "A", "A+", "O"]
os.makedirs("charts", exist_ok=True)


def load_data(path):
    df = pd.read_csv(path)
    print(f"Rows loaded: {len(df)}   Columns: {len(df.columns)}")
    print("Missing values per column:")
    print(df.isnull().sum()[df.isnull().sum() > 0].to_string())
    return df


def clean_data(df):
    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"Duplicate rows removed: {before - len(df)}")
    for sub in SUBJECTS:                   # fill a missing mark with the subject average
        df[sub] = df[sub].fillna(round(df[sub].mean()))
    print("Missing marks filled with subject mean.")
    return df


def compute_results(df):
    df["Total"] = df[SUBJECTS].sum(axis=1)
    df["Percentage"] = (df["Total"] / (len(SUBJECTS) * 100) * 100).round(2)
    df["Grade"] = pd.cut(df["Percentage"], GRADE_BINS, labels=GRADE_LABELS, right=False)
    failed = (df[SUBJECTS] < PASS_MARK).any(axis=1)
    df["Result"] = np.where(failed, "Fail", "Pass")
    df.loc[failed, "Grade"] = "F"
    df["Rank"] = df["Percentage"].rank(ascending=False, method="min").astype(int)
    return df


def subject_statistics(df):
    rows = {}
    for sub in SUBJECTS:
        m = df[sub].to_numpy()
        rows[sub] = [np.mean(m), np.median(m), np.std(m), np.max(m), np.min(m),
                     (m >= PASS_MARK).mean() * 100]
    cols = ["Mean", "Median", "Std Dev", "Max", "Min", "Pass %"]
    return pd.DataFrame(rows, index=cols).T.round(2)


def correlation_report(df):
    corr = df[["Attendance", "StudyHours", "Percentage"]].corr().round(3)
    slope, intercept = np.polyfit(df["Attendance"], df["Percentage"], 1)
    return corr, slope, intercept


def save_chart(name):
    plt.tight_layout()
    plt.savefig(f"charts/{name}.png", dpi=150)
    plt.close()


def make_charts(df, stats, corr, slope, intercept):
    plt.figure(figsize=(6.4, 3.2))                                    # 1 subject averages
    bars = plt.bar(stats.index, stats["Mean"], color="#3b6ea5")
    plt.bar_label(bars, fmt="%.1f")
    plt.ylabel("Average marks"); plt.title("Subject-wise average marks"); plt.ylim(0, 100)
    save_chart("fig1_subject_average")

    plt.figure(figsize=(6.4, 3.2))                                    # 2 grade distribution
    counts = df["Grade"].value_counts().reindex(GRADE_LABELS[::-1], fill_value=0)
    bars = plt.bar(counts.index.astype(str), counts.values, color="#c0504d")
    plt.bar_label(bars)
    plt.xlabel("Grade"); plt.ylabel("Number of students"); plt.title("Grade distribution")
    plt.ylim(0, counts.max() * 1.15)
    save_chart("fig2_grade_distribution")

    plt.figure(figsize=(6.4, 3.2))                                    # 3 histogram
    plt.hist(df["Percentage"], bins=10, color="#5b9a5b", edgecolor="white")
    plt.axvline(df["Percentage"].mean(), color="black", linestyle="--", label="Mean")
    plt.xlabel("Percentage"); plt.ylabel("Students"); plt.legend()
    plt.title("Distribution of overall percentage")
    save_chart("fig3_percentage_histogram")

    plt.figure(figsize=(6.4, 3.2))                                    # 4 attendance vs result
    plt.scatter(df["Attendance"], df["Percentage"], color="#3b6ea5", s=22)
    x = np.linspace(df["Attendance"].min(), df["Attendance"].max(), 50)
    plt.plot(x, slope * x + intercept, color="red", label=f"Trend line (slope = {slope:.2f})")
    plt.xlabel("Attendance (%)"); plt.ylabel("Percentage"); plt.legend()
    plt.title("Attendance vs overall percentage")
    save_chart("fig4_attendance_scatter")

    plt.figure(figsize=(6.4, 3.2))                                    # 5 box plot
    plt.boxplot([df[s] for s in SUBJECTS], tick_labels=SUBJECTS)
    plt.ylabel("Marks"); plt.title("Spread of marks in each subject")
    save_chart("fig5_subject_boxplot")

    plt.figure(figsize=(4.6, 3.6))                                    # 6 correlation heatmap
    plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    plt.xticks(range(3), corr.columns, rotation=20); plt.yticks(range(3), corr.index)
    for i in range(3):
        for j in range(3):
            plt.text(j, i, corr.iloc[i, j], ha="center", va="center")
    plt.colorbar(); plt.title("Correlation matrix")
    save_chart("fig6_correlation_heatmap")


def main():
    print("=" * 52); print("STEP 1: LOADING DATA"); print("=" * 52)
    df = load_data("students.csv")
    print("\n" + "=" * 52); print("STEP 2: CLEANING DATA"); print("=" * 52)
    df = clean_data(df)
    df = compute_results(df)

    print("\n" + "=" * 52); print("STEP 3: SUBJECT STATISTICS"); print("=" * 52)
    stats = subject_statistics(df)
    print(stats.to_string())

    print("\n" + "=" * 52); print("STEP 4: RESULT SUMMARY"); print("=" * 52)
    print(f"Total students     : {len(df)}")
    passed = (df["Result"] == "Pass").sum()
    print(f"Passed / Failed    : {passed} / {len(df) - passed}")
    print(f"Class average      : {df['Percentage'].mean():.2f}%")
    print(f"Highest percentage : {df['Percentage'].max():.2f}%")
    print(f"Lowest percentage  : {df['Percentage'].min():.2f}%")
    print("\nTop 5 students:")
    print(df.nsmallest(5, "Rank")[["Rank", "StudentID", "Section", "Total", "Percentage", "Grade"]]
          .to_string(index=False))
    risk = df[(df["Percentage"] < 50) | (df["Attendance"] < 75)]
    print(f"\nStudents needing attention (below 50% or attendance below 75%): {len(risk)}")
    print("\nSection-wise performance:")
    print(df.groupby("Section").agg(Students=("StudentID", "count"),
                                    Average=("Percentage", "mean"),
                                    PassRate=("Result", lambda r: (r == "Pass").mean() * 100)).round(2).to_string())

    print("\n" + "=" * 52); print("STEP 5: CORRELATION ANALYSIS"); print("=" * 52)
    corr, slope, intercept = correlation_report(df)
    print(corr.to_string())
    print(f"Trend line: Percentage = {slope:.3f} x Attendance + {intercept:.2f}")

    make_charts(df, stats, corr, slope, intercept)
    df.sort_values("Rank").to_csv("result_report.csv", index=False)
    print("\n6 charts saved in the charts folder; result_report.csv created.")


if __name__ == "__main__":
    main()
