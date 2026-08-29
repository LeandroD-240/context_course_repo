import json
import sys
import pandas as pd
from pathlib import Path

def validate_csv(filepath):
    """Validate a CSV dataset file."""
    
    errors = []
    warnings = []
    report = {
        "filepath": filepath,
        "format": "csv",
        "errors": errors,
        "warnings": warnings,
        "metadata": {}
    }
    
    # Check file exists
    if not Path(filepath).exists():
        errors.append(f"File not found: {filepath}")
        return report
    
    try:
        # Load file
        df = pd.read_csv(filepath)
        report["metadata"]["rows"] = len(df)
        report["metadata"]["columns"] = list(df.columns)
        report["metadata"]["dtypes"] = {k: str(v) for k, v in df.dtypes.items()}
        
        # Check for missing values
        missing = df.isna().sum()
        if missing.any():
            report["metadata"]["missing_values"] = missing.to_dict()
        
        # Check for duplicates
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            warnings.append(f"Found {dup_count} duplicate rows")
        
        # Check for empty strings
        for col in df.select_dtypes(include='object').columns:
            empty = (df[col].str.strip() == '').sum()
            if empty > 0:
                warnings.append(f"Column '{col}' has {empty} empty strings")
        
    except Exception as e:
        errors.append(f"Error reading file: {str(e)}")
    
    return report

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_dataset.py <filepath>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    report = validate_csv(filepath)
    print(json.dumps(report, indent=2))
    
    if report["errors"]:
        sys.exit(1)

if __name__ == "__main__":
    main()