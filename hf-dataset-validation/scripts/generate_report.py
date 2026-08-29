import sys
import pandas as pd
from pathlib import Path

def generate_report(filepath):
    """Generate a text report for a dataset."""
    
    report = []
    report.append("=" * 60)
    report.append("DATASET VALIDATION REPORT")
    report.append("=" * 60)
    report.append(f"\nFile: {filepath}\n")
    
    if not Path(filepath).exists():
        report.append(f"ERROR: File not found: {filepath}")
        return "\n".join(report)
    
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        report.append(f"ERROR: Could not read file: {e}")
        return "\n".join(report)
    
    # Basic stats
    report.append("BASIC STATISTICS")
    report.append(f"  Rows: {len(df)}")
    report.append(f"  Columns: {len(df.columns)}")
    report.append(f"  Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Column info
    report.append("\nCOLUMN INFORMATION")
    for col in df.columns:
        dtype = df[col].dtype
        non_null = df[col].notna().sum()
        report.append(f"  {col}: {dtype} ({non_null}/{len(df)} non-null)")
    
    # Data quality
    report.append("\nDATA QUALITY")
    missing = df.isna().sum().sum()
    report.append(f"  Missing values: {missing}")
    duplicates = df.duplicated().sum()
    report.append(f"  Duplicate rows: {duplicates}")
    
    # Recommendations
    report.append("\nRECOMMENDATIONS")
    if missing > 0:
        report.append("  - Handle missing values (drop or impute)")
    if duplicates > 0:
        report.append("  - Remove duplicate rows")
    report.append("  - Document dataset and preprocessing steps")
    report.append("  - Add LICENSE and README.md files")
    
    report.append("\n" + "=" * 60)
    return "\n".join(report)

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py <filepath>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    print(generate_report(filepath))

if __name__ == "__main__":
    main()