"""
Cricket Players Performance Analysis (EDA)
Tools: Python, NumPy, Pandas, Matplotlib
- No seaborn
- No conclusions, only analysis tasks + plots

USAGE:
1) Put your Kaggle CSV path in CSV_PATH below.
2) Run: python cricket_eda.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# CONFIG: Put your CSV path here
# -----------------------------
CSV_PATH = r"C:\Users\User\OneDrive\Desktop\Capg\python\Day21\Task2\players_data_with_all_info.csv"


# -----------------------------
# Helper functions
# -----------------------------
def normalize_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names for easier matching."""
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    return df


def pick_col(df: pd.DataFrame, candidates):
    """Return the first existing column from candidates list, else None."""
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    return None


def to_numeric_safe(series: pd.Series):
    """Convert to numeric if possible; keep NaN for non-convertible values."""
    return pd.to_numeric(series, errors="coerce")


def safe_divide(a, b):
    """Elementwise divide with NaN where b==0 or NaN."""
    a = np.array(a, dtype="float64")
    b = np.array(b, dtype="float64")
    out = np.full_like(a, np.nan, dtype="float64")
    mask = (b != 0) & (~np.isnan(b)) & (~np.isnan(a))
    out[mask] = a[mask] / b[mask]
    return out


def print_section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


# -----------------------------
# Part 1: Data Loading & Understanding
# -----------------------------
print_section("PART 1: DATA LOADING & UNDERSTANDING")

df = pd.read_csv(CSV_PATH)
df = normalize_cols(df)

print("\nFirst 10 rows:")
print(df.head(10))

print("\nLast 5 rows:")
print(df.tail(5))

print("\nDataset shape (rows, cols):", df.shape)
print("\nColumn names:")
print(list(df.columns))

print("\nData types:")
print(df.dtypes)

# Missing values and duplicates
print("\nMissing values per column:")
print(df.isna().sum())

dup_count = df.duplicated().sum()
print("\nDuplicate records count:", int(dup_count))

# NumPy: count total numeric columns
numeric_cols = df.select_dtypes(include=[np.number]).columns
print("\nTotal numeric columns (NumPy/Pandas):", int(len(numeric_cols)))
print("Numeric columns:", list(numeric_cols))

# Manual stats (NumPy) for at least one numeric column
# Try Runs first; if not found, use the first numeric column.
runs_col = pick_col(df, ["Runs", "Run", "R", "Total Runs", "Runs_Scored"])
manual_col = runs_col if runs_col else (numeric_cols[0] if len(numeric_cols) > 0 else None)

if manual_col is not None:
    x = to_numeric_safe(df[manual_col]).to_numpy(dtype="float64")
    x = x[~np.isnan(x)]
    if x.size > 0:
        mean_x = np.sum(x) / x.size
        median_x = np.median(x)
        std_x = np.sqrt(np.sum((x - mean_x) ** 2) / x.size)  # population std
        print(f"\nManual basic stats (NumPy) for column: {manual_col}")
        print("Mean  :", mean_x)
        print("Median:", median_x)
        print("Std   :", std_x)
    else:
        print(f"\nManual stats skipped: column {manual_col} has no numeric values.")
else:
    print("\nManual stats skipped: no numeric column detected.")


# -----------------------------
# Part 2: Data Cleaning
# -----------------------------
print_section("PART 2: DATA CLEANING")

# 1) Handle missing values appropriately
# Strategy:
# - numeric columns: fill with median
# - non-numeric: fill with mode (if exists) else "Unknown"
df_clean = df.copy()

num_cols = df_clean.select_dtypes(include=[np.number]).columns
obj_cols = [c for c in df_clean.columns if c not in num_cols]

for c in num_cols:
    med = df_clean[c].median(numeric_only=True)
    df_clean[c] = df_clean[c].fillna(med)

for c in obj_cols:
    modes = df_clean[c].mode(dropna=True)
    fill_val = modes.iloc[0] if len(modes) else "Unknown"
    df_clean[c] = df_clean[c].fillna(fill_val)

print("\nAfter missing value handling:")
print("Missing values per column:")
print(df_clean.isna().sum())

# 2) Remove or handle duplicate rows
before = df_clean.shape[0]
df_clean = df_clean.drop_duplicates()
after = df_clean.shape[0]
print(f"\nDuplicates removed: {before - after}")

# 3) Convert necessary columns to correct data types
# Common numeric candidates in cricket datasets
likely_numeric = [
    "Matches", "Mat", "M",
    "Innings", "Inns", "I",
    "Runs", "Run", "R", "Total Runs", "Runs_Scored",
    "Balls", "BF", "Balls Faced",
    "Outs", "Dismissals",
    "Not Outs", "NO", "NotOut",
    "Wickets", "Wkt", "WKTS",
    "Overs", "Ov", "O",
    "Runs Conceded", "Conceded", "Runs_Conceded",
    "Average", "Avg", "Batting Average",
    "Strike Rate", "SR",
    "Economy", "Econ", "Economy Rate",
]

for name in likely_numeric:
    col = pick_col(df_clean, [name])
    if col is not None:
        df_clean[col] = to_numeric_safe(df_clean[col])

# 4) Create new calculated columns (NumPy where possible)
# Batting Strike Rate = (Runs / Balls) * 100
balls_col = pick_col(df_clean, ["Balls", "BF", "Balls Faced"])
runs_col = pick_col(df_clean, ["Runs", "Run", "R", "Total Runs", "Runs_Scored"])

if runs_col and balls_col:
    runs = to_numeric_safe(df_clean[runs_col]).to_numpy(dtype="float64")
    balls = to_numeric_safe(df_clean[balls_col]).to_numpy(dtype="float64")
    df_clean["Calc_Batting_Strike_Rate"] = safe_divide(runs * 100.0, balls)

# Bowling Economy = Runs Conceded / Overs
overs_col = pick_col(df_clean, ["Overs", "Ov", "O"])
rc_col = pick_col(df_clean, ["Runs Conceded", "Conceded", "Runs_Conceded", "RunsConceded"])

if rc_col and overs_col:
    rc = to_numeric_safe(df_clean[rc_col]).to_numpy(dtype="float64")
    ov = to_numeric_safe(df_clean[overs_col]).to_numpy(dtype="float64")
    df_clean["Calc_Bowling_Economy"] = safe_divide(rc, ov)

# Batting Average (if not available)
# If Outs exists, use Runs / Outs
# Else if Inns and Not Outs exist, outs = Inns - NotOuts
bat_avg_existing = pick_col(df_clean, ["Batting Average", "Average", "Avg"])

outs_col = pick_col(df_clean, ["Outs", "Dismissals"])
inns_col = pick_col(df_clean, ["Innings", "Inns", "I"])
notouts_col = pick_col(df_clean, ["Not Outs", "NO", "NotOut", "NotOuts"])

if bat_avg_existing is None and runs_col is not None:
    runs = to_numeric_safe(df_clean[runs_col]).to_numpy(dtype="float64")

    if outs_col is not None:
        outs = to_numeric_safe(df_clean[outs_col]).to_numpy(dtype="float64")
        df_clean["Calc_Batting_Average"] = safe_divide(runs, outs)

    elif inns_col is not None and notouts_col is not None:
        inns = to_numeric_safe(df_clean[inns_col]).to_numpy(dtype="float64")
        no = to_numeric_safe(df_clean[notouts_col]).to_numpy(dtype="float64")
        outs = inns - no
        df_clean["Calc_Batting_Average"] = safe_divide(runs, outs)

print("\nNew calculated columns created if inputs were available:")
new_cols = [c for c in ["Calc_Batting_Strike_Rate", "Calc_Bowling_Economy", "Calc_Batting_Average"] if c in df_clean.columns]
print(new_cols if new_cols else "None created (required source columns not found).")


# -----------------------------
# Part 3: Batting Analysis
# -----------------------------
print_section("PART 3: BATTING ANALYSIS")

player_col = pick_col(df_clean, ["Player", "Batsman", "Name", "Player Name"])
matches_col = pick_col(df_clean, ["Matches", "Mat", "M"])

# Decide batting average column to use
bat_avg_col = pick_col(df_clean, ["Batting Average", "Average", "Avg"])
if bat_avg_col is None and "Calc_Batting_Average" in df_clean.columns:
    bat_avg_col = "Calc_Batting_Average"

# Decide strike rate column to use
sr_col = pick_col(df_clean, ["Strike Rate", "SR"])
if sr_col is None and "Calc_Batting_Strike_Rate" in df_clean.columns:
    sr_col = "Calc_Batting_Strike_Rate"

# 1) Top 10 players by: Total Runs, Batting Average, Strike Rate
if player_col and runs_col:
    top_runs = df_clean[[player_col, runs_col]].sort_values(by=runs_col, ascending=False).head(10)
    print("\nTop 10 players by Total Runs:")
    print(top_runs)

if player_col and bat_avg_col:
    top_avg = df_clean[[player_col, bat_avg_col]].sort_values(by=bat_avg_col, ascending=False).head(10)
    print("\nTop 10 players by Batting Average:")
    print(top_avg)

if player_col and sr_col:
    top_sr = df_clean[[player_col, sr_col]].sort_values(by=sr_col, ascending=False).head(10)
    print("\nTop 10 players by Strike Rate:")
    print(top_sr)

# 2) Distribution of Runs (Histogram)
if runs_col:
    plt.figure()
    vals = to_numeric_safe(df_clean[runs_col]).dropna().to_numpy(dtype="float64")
    plt.hist(vals, bins=20)
    plt.title("Distribution of Runs")
    plt.xlabel("Runs")
    plt.ylabel("Frequency")
    plt.show()

# 3) Compare:
# - Runs vs Strike Rate (Scatter)
if runs_col and sr_col:
    plt.figure()
    x = to_numeric_safe(df_clean[runs_col]).to_numpy(dtype="float64")
    y = to_numeric_safe(df_clean[sr_col]).to_numpy(dtype="float64")
    mask = ~np.isnan(x) & ~np.isnan(y)
    plt.scatter(x[mask], y[mask])
    plt.title("Runs vs Strike Rate")
    plt.xlabel("Runs")
    plt.ylabel("Strike Rate")
    plt.show()

# - Matches vs Runs (Line or Scatter)
if matches_col and runs_col:
    plt.figure()
    x = to_numeric_safe(df_clean[matches_col]).to_numpy(dtype="float64")
    y = to_numeric_safe(df_clean[runs_col]).to_numpy(dtype="float64")
    mask = ~np.isnan(x) & ~np.isnan(y)
    plt.scatter(x[mask], y[mask])
    plt.title("Matches vs Runs")
    plt.xlabel("Matches")
    plt.ylabel("Runs")
    plt.show()

# 4) Calculate: mean runs, median strike rate, std of batting averages (NumPy)
if runs_col:
    r = to_numeric_safe(df_clean[runs_col]).to_numpy(dtype="float64")
    r = r[~np.isnan(r)]
    if r.size:
        mean_runs = np.mean(r)
        print("\nMean runs scored by all players (NumPy):", mean_runs)

if sr_col:
    s = to_numeric_safe(df_clean[sr_col]).to_numpy(dtype="float64")
    s = s[~np.isnan(s)]
    if s.size:
        median_sr = np.median(s)
        print("Median strike rate (NumPy):", median_sr)

if bat_avg_col:
    a = to_numeric_safe(df_clean[bat_avg_col]).to_numpy(dtype="float64")
    a = a[~np.isnan(a)]
    if a.size:
        std_avg = np.std(a)  # population std
        print("Standard deviation of batting averages (NumPy):", std_avg)


# -----------------------------
# Part 4: Bowling Analysis (if bowling stats available)
# -----------------------------
print_section("PART 4: BOWLING ANALYSIS (IF AVAILABLE)")

wickets_col = pick_col(df_clean, ["Wickets", "Wkt", "WKTS"])
econ_col = pick_col(df_clean, ["Economy Rate", "Economy", "Econ"])
if econ_col is None and "Calc_Bowling_Economy" in df_clean.columns:
    econ_col = "Calc_Bowling_Economy"

if wickets_col or econ_col:
    # 1) Top 10 bowlers by Wickets and Economy Rate
    if player_col and wickets_col:
        top_wkts = df_clean[[player_col, wickets_col]].sort_values(by=wickets_col, ascending=False).head(10)
        print("\nTop 10 bowlers by Wickets:")
        print(top_wkts)

    if player_col and econ_col:
        top_econ = df_clean[[player_col, econ_col]].sort_values(by=econ_col, ascending=True).head(10)
        print("\nTop 10 bowlers by Best (Lowest) Economy Rate:")
        print(top_econ)

    # 2) Wickets distribution (Histogram)
    if wickets_col:
        plt.figure()
        w = to_numeric_safe(df_clean[wickets_col]).dropna().to_numpy(dtype="float64")
        plt.hist(w, bins=20)
        plt.title("Distribution of Wickets")
        plt.xlabel("Wickets")
        plt.ylabel("Frequency")
        plt.show()

    # 3) Economy Rate vs Wickets (Scatter)
    if wickets_col and econ_col:
        plt.figure()
        w = to_numeric_safe(df_clean[wickets_col]).to_numpy(dtype="float64")
        e = to_numeric_safe(df_clean[econ_col]).to_numpy(dtype="float64")
        mask = ~np.isnan(w) & ~np.isnan(e)
        plt.scatter(e[mask], w[mask])
        plt.title("Economy Rate vs Wickets")
        plt.xlabel("Economy Rate")
        plt.ylabel("Wickets")
        plt.show()

    # 4) Average wickets per player, best economy, correlation (NumPy)
    if wickets_col:
        w = to_numeric_safe(df_clean[wickets_col]).to_numpy(dtype="float64")
        w = w[~np.isnan(w)]
        if w.size:
            print("\nAverage wickets per player (NumPy):", np.mean(w))

    if econ_col:
        e = to_numeric_safe(df_clean[econ_col]).to_numpy(dtype="float64")
        e = e[~np.isnan(e)]
        if e.size:
            print("Best (lowest) economy rate (NumPy):", np.min(e))

    if wickets_col and econ_col:
        w = to_numeric_safe(df_clean[wickets_col]).to_numpy(dtype="float64")
        e = to_numeric_safe(df_clean[econ_col]).to_numpy(dtype="float64")
        mask = ~np.isnan(w) & ~np.isnan(e)
        if np.sum(mask) >= 2:
            corr = np.corrcoef(w[mask], e[mask])[0, 1]
            print("Correlation between wickets and economy (NumPy):", corr)
else:
    print("Bowling stats not detected (no wickets/economy columns found).")


# -----------------------------
# Part 5: Team-Based Analysis
# -----------------------------
print_section("PART 5: TEAM-BASED ANALYSIS")

team_col = pick_col(df_clean, ["Team", "Team Name", "IPL Team", "Country", "Franchise"])

if team_col:
    # 1) Total runs per team
    if runs_col:
        team_runs = df_clean.groupby(team_col, dropna=False)[runs_col].sum().sort_values(ascending=False)
        print("\nTotal runs scored per team:")
        print(team_runs)

    # 2) Average batting average per team
    if bat_avg_col:
        team_avg = df_clean.groupby(team_col, dropna=False)[bat_avg_col].mean().sort_values(ascending=False)
        print("\nAverage batting average per team:")
        print(team_avg)

    # 3) Total wickets per team
    if wickets_col:
        team_wkts = df_clean.groupby(team_col, dropna=False)[wickets_col].sum().sort_values(ascending=False)
        print("\nTotal wickets per team:")
        print(team_wkts)

    # 4) Bar chart: Team vs Total Runs
    if runs_col:
        plt.figure()
        team_runs.plot(kind="bar")
        plt.title("Team vs Total Runs")
        plt.xlabel("Team")
        plt.ylabel("Total Runs")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    # 5) Bar chart: Team vs Total Wickets
    if wickets_col:
        plt.figure()
        team_wkts.plot(kind="bar")
        plt.title("Team vs Total Wickets")
        plt.xlabel("Team")
        plt.ylabel("Total Wickets")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()
else:
    print("Team column not detected (no Team/Country/Franchise-like column found).")


# -----------------------------
# Part 6: Advanced Analysis
# -----------------------------
print_section("PART 6: ADVANCED ANALYSIS")

# 1) Identify:
# - Most consistent batsman (low std deviation in runs)
#   This requires multiple rows per player (e.g., season-wise stats or match-wise rows).
if player_col and runs_col:
    runs_per_player_std = df_clean.groupby(player_col)[runs_col].std()  # std across rows
    # If each player appears only once, std will be NaN for all
    if runs_per_player_std.notna().any():
        most_consistent = runs_per_player_std.dropna().sort_values(ascending=True).head(10)
        print("\nMost consistent batsmen (lowest std in runs across rows) - Top 10:")
        print(most_consistent)
    else:
        print("\nConsistency metric skipped: each player likely appears once (no per-player std available).")

# - Most impactful bowler (high wickets + low economy)
#   Create an impact score using NumPy: wickets / economy (higher is better)
if player_col and wickets_col and econ_col:
    w = to_numeric_safe(df_clean[wickets_col]).to_numpy(dtype="float64")
    e = to_numeric_safe(df_clean[econ_col]).to_numpy(dtype="float64")
    impact = safe_divide(w, e)  # wickets per unit economy
    df_clean["Impact_Score_Wkts_per_Econ"] = impact

    top_impact = df_clean[[player_col, wickets_col, econ_col, "Impact_Score_Wkts_per_Econ"]] \
        .sort_values(by="Impact_Score_Wkts_per_Econ", ascending=False) \
        .head(10)
    print("\nMost impactful bowlers (high wickets + low economy via wickets/economy) - Top 10:")
    print(top_impact)

# 2) Create:
# - Box plot for batting averages
if bat_avg_col:
    plt.figure()
    vals = to_numeric_safe(df_clean[bat_avg_col]).dropna().to_numpy(dtype="float64")
    plt.boxplot(vals, vert=True)
    plt.title("Box Plot of Batting Averages")
    plt.ylabel("Batting Average")
    plt.show()

# - Pie chart for distribution of players by role
role_col = pick_col(df_clean, ["Role", "Player Type", "Type", "Playing Role", "Specialist"])
if role_col:
    role_counts = df_clean[role_col].value_counts(dropna=False)
    plt.figure()
    plt.pie(role_counts.values, labels=role_counts.index.astype(str), autopct="%1.1f%%")
    plt.title("Distribution of Players by Role")
    plt.show()
else:
    print("\nRole column not detected (no Role/Player Type-like column found). Pie chart skipped.")

# 3) Correlation matrix using NumPy (numeric columns only)
num_df = df_clean.select_dtypes(include=[np.number]).copy()
if num_df.shape[1] >= 2:
    # Fill any remaining NaNs in numeric-only frame (safety) with column medians
    for c in num_df.columns:
        num_df[c] = num_df[c].fillna(num_df[c].median())

    data = num_df.to_numpy(dtype="float64")
    corr = np.corrcoef(data, rowvar=False)  # columns correlation

    print("\nCorrelation matrix (NumPy) for numeric columns:")
    corr_df = pd.DataFrame(corr, index=num_df.columns, columns=num_df.columns)
    print(corr_df)

    # 4) Visualize correlation heat-style using Matplotlib only
    plt.figure(figsize=(10, 8))
    plt.imshow(corr, aspect="auto")
    plt.title("Correlation Heat-Style (Matplotlib Only)")
    plt.xticks(ticks=np.arange(len(num_df.columns)), labels=num_df.columns, rotation=90)
    plt.yticks(ticks=np.arange(len(num_df.columns)), labels=num_df.columns)

    # annotate values (optional but useful for analysis)
    for i in range(corr.shape[0]):
        for j in range(corr.shape[1]):
            plt.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center", fontsize=7)

    plt.colorbar()
    plt.tight_layout()
    plt.show()
else:
    print("\nCorrelation analysis skipped: not enough numeric columns found.")

print_section("DONE (All requested analysis tasks executed where columns were available)")