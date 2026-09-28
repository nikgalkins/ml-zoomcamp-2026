from pathlib import Path
import nbformat as nbf

root = Path(__file__).resolve().parent.parent
cells = []

def markdown(text):
    cells.append(nbf.v4.new_markdown_cell(text.strip()))

def code(text):
    cells.append(nbf.v4.new_code_cell(text.strip()))

markdown("""
# Machine Learning Zoomcamp 2026 — Homework 1

A step-by-step learning notebook for [the official 2026 homework](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/cohorts/2026/homework/01-intro/homework.md).
The questions below are paraphrased from that assignment.

Data: [official 2026 car fuel-efficiency CSV](https://raw.githubusercontent.com/DataTalksClub/machine-learning-zoomcamp/main/cohorts/2026/data/car_fuel_efficiency_2026.csv).
The downloaded `car_fuel_efficiency_2026.csv` is beside this notebook. Run the cells from top to bottom in a Python environment with pandas and NumPy installed.
All results below are calculated from this file. Q1 reports the pandas version used to execute this notebook; your version may differ in another environment.
""")

markdown("""
## Q1 — Installed pandas

**Question:** Which pandas release is running in this notebook?
""")
code("""
import pandas as pd
import numpy as np

pandas_version = pd.__version__
print("pandas version:", pandas_version)
""")
markdown("`pd.__version__` reads the version string from the imported pandas package. `pd` and `np` are the usual short names for pandas and NumPy.")

markdown("""
## Q2 — Dataset size

**Question:** What is the number of rows in the CSV?
""")
code("""
df = pd.read_csv("car_fuel_efficiency_2026.csv")
record_count = df.shape[0]
print("Dataset shape (rows, columns):", df.shape)
print("Number of records:", record_count)
""")
markdown("`pd.read_csv()` loads the CSV into a DataFrame, a table with named columns. `df.shape` gives `(rows, columns)`, so `df.shape[0]` counts records; the header is not a record.")

markdown("""
## Q3 — Fuel categories

**Question:** How many distinct fuel categories occur in the data?
""")
code("""
fuel_type_count = df["fuel_type"].nunique()
print("Fuel categories:", df["fuel_type"].unique())
print("Number of fuel types:", fuel_type_count)
""")
markdown("Selecting `df[\"fuel_type\"]` gives one column as a Series. `unique()` shows its distinct values, and `nunique()` counts them. By default, `nunique()` excludes missing values.")

markdown("""
## Q4 — Columns containing gaps

**Question:** How many columns contain at least one missing entry?
""")
code("""
missing_counts = df.isna().sum()
columns_with_missing = (missing_counts > 0).sum()
print("Missing entries by column:")
print(missing_counts)
print("Number of columns with missing values:", columns_with_missing)
""")
markdown("`isna()` marks missing entries with `True`. The first `sum()` counts them in each column. Comparing those counts with zero identifies columns containing gaps; the second `sum()` counts these columns because `True` counts as 1.")

markdown("""
## Q5 — Best efficiency among Asian cars

**Question:** Among cars whose origin is Asia, what is the largest MPG value?
""")
code("""
asia_cars = df[df["origin"] == "Asia"]
max_asia_efficiency = asia_cars["fuel_efficiency_mpg"].max()
print("Maximum fuel efficiency for Asia (MPG):", max_asia_efficiency)
""")
markdown("`df[\"origin\"] == \"Asia\"` creates a Boolean mask. Indexing `df` with it keeps only Asian cars. `max()` finds the largest value in their fuel-efficiency column.")

markdown("""
## Q6 — Horsepower before and after filling gaps

**Question:** Calculate the horsepower median and mode. Replace missing horsepower with the mode, then recalculate the median. Does it rise, fall, or stay the same?
""")
code("""
median_before = df["horsepower"].median()
horsepower_modes = df["horsepower"].mode()
horsepower_mode = horsepower_modes.iloc[0]
horsepower_filled = df["horsepower"].fillna(horsepower_mode)
median_after = horsepower_filled.median()

if median_after > median_before:
    median_change = "increased"
elif median_after < median_before:
    median_change = "decreased"
else:
    median_change = "unchanged"

print("Median before filling:", median_before)
print("Most frequent horsepower value(s):", horsepower_modes.tolist())
print("Value used to fill gaps:", horsepower_mode)
print("Missing horsepower entries after filling:", horsepower_filled.isna().sum())
print("Median after filling:", median_after)
print("Median change:", median_change)
""")
markdown("`median()` finds the middle value and ignores missing entries. `mode()` returns the most frequent value(s); `.iloc[0]` selects the first. `fillna()` returns a Series with gaps filled using that value. We keep it separately so the original DataFrame stays available for later questions.")

markdown("""
## Q7 — Computing regression weights

**Question:** Take the first seven Asian cars in file order and retain `vehicle_weight` and `model_year`, in that order, as NumPy matrix `X`. Form `X.T @ X`, invert it, and compute `w = inv(X.T @ X) @ X.T @ y` for `y = [1100, 1300, 800, 900, 1000, 1100, 1200]`. What is the total of the weights?
""")
code("""
X = asia_cars[["vehicle_weight", "model_year"]].head(7).to_numpy()
print("X shape:", X.shape)
print("X (vehicle_weight, model_year):")
print(X)

print("X.T shape:", X.T.shape)
print("X.T:")
print(X.T)
""")
markdown("Double brackets select two columns in the specified order. `head(7)` takes the first seven rows without sorting. `to_numpy()` extracts the numeric array: seven observations and two features give `X` shape `(7, 2)`. `.T` swaps rows and columns, giving `(2, 7)`.")

code("""
XTX = X.T @ X
print("XTX shape:", XTX.shape)
print("XTX:")
print(XTX)

XTX_inverse = np.linalg.inv(XTX)
print("Inverse of XTX shape:", XTX_inverse.shape)
print("Inverse of XTX:")
print(XTX_inverse)
""")
markdown("`@` performs matrix multiplication. Multiplying `(2, 7)` by `(7, 2)` produces a `(2, 2)` matrix. `np.linalg.inv()` computes its inverse, also `(2, 2)`; an inverse exists here because this matrix is nonsingular.")

code("""
y = np.array([1100, 1300, 800, 900, 1000, 1100, 1200])
print("y shape:", y.shape)

inverse_times_transpose = XTX_inverse @ X.T
print("Inverse of XTX @ X.T shape:", inverse_times_transpose.shape)

w = inverse_times_transpose @ y
weights_sum = w.sum()
print("w shape:", w.shape)
print("w (vehicle_weight coefficient, model_year coefficient):")
print(w)
print("Sum of weights:", weights_sum)
print("Sum rounded to 3 decimal places:", round(weights_sum, 3))
""")
markdown(r"""
Multiplying `(2, 2)` by `(2, 7)` gives `(2, 7)`. Multiplying that result by the seven-element vector `y`, shape `(7,)`, gives two coefficients, shape `(2,)`. `w.sum()` adds them; rounding happens only for display.

**Why this is linear regression:** The prediction vector is `X @ w`. Least squares chooses `w` to minimize the sum of squared differences between these predictions and `y`. Setting the derivatives to zero gives the normal equations, `(X.T @ X) @ w = X.T @ y`. When `X.T @ X` is invertible, solving them gives `inv(X.T @ X) @ X.T @ y`.

Here each of the two selected features gets one coefficient. There is no intercept because we did not add a column of ones. The target `y` is the supplied exercise vector, not the dataset's MPG column.
""")

markdown("## Calculated summary\n\nThe following cell reuses the results calculated above.")
code("""
print(f"Q1 -> pandas {pandas_version}")
print(f"Q2 -> {record_count} records")
print(f"Q3 -> {fuel_type_count} fuel types")
print(f"Q4 -> {columns_with_missing} columns with missing values")
print(f"Q5 -> {max_asia_efficiency} MPG")
print(f"Q6 -> median {median_before} -> {median_after}; {median_change} (fill value: {horsepower_mode})")
print(f"Q7 -> sum of weights = {weights_sum:.12f} (rounded: {weights_sum:.3f})")
""")

nb = nbf.v4.new_notebook(cells=cells)
nb.metadata.kernelspec = {
    "display_name": "Python 3", "language": "python", "name": "python3"
}
nbf.write(nb, root / "01_intro_homework.ipynb")
print(f"Created notebook with {len(cells)} cells.")
