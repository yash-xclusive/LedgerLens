import pandas as pd

def flag_duplicate_payments(df: pd.DataFrame) -> pd.DataFrame:
    """Flag exact repeated transaction references; does not label fraud."""
    out=df.copy()
    out["duplicate_reference"] = out["transaction_reference"].duplicated(keep=False)
    return out

def flag_unusual_amounts(df: pd.DataFrame, multiplier: float = 3.0) -> pd.DataFrame:
    """Simple transparent outlier flag using median absolute deviation."""
    out=df.copy()
    amounts=pd.to_numeric(out["amount"], errors="coerce")
    median=amounts.median()
    deviations=(amounts-median).abs()
    mad=deviations.median()
    if pd.isna(mad) or mad == 0:
        out["unusual_amount"] = False
    else:
        robust_z=0.6745*deviations/mad
        out["unusual_amount"] = robust_z > multiplier
    return out
