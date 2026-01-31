import csv
from datetime import datetime
import pandas as pd
from pathlib import Path

FILE_PATH = Path(__file__).resolve().parent.parent / "data" / "mental_data.csv"

def save_result(tool, score, severity=None, subscale=None, extra=None):
    file_exists = FILE_PATH.exists()

    with open(FILE_PATH, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "tool",
                "subscale",
                "score",
                "severity",
                "extra"
            ])

        writer.writerow([
            datetime.now().isoformat(),
            tool,
            subscale,
            score,
            severity,
            extra
        ])

def load_data(tool=None):
    if not FILE_PATH.exists():
        return pd.DataFrame()

    df = pd.read_csv(FILE_PATH, parse_dates=["timestamp"])

    # normalize tool column
    df["tool"] = df["tool"].str.upper().str.replace("-", "").str.strip()

    if tool:
        tool = tool.upper().replace("-", "")
        df = df[df["tool"] == tool]

    return df.sort_values("timestamp")

