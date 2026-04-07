import pandas as pd
from typing import Union

def analyze_case_duplicates(clinical_data: pd.DataFrame, case_id_col: str) -> list:
    """
    Analyzes a clinical DataFrame for duplicate case IDs and identifies
    columns where duplicates differ.

    Parameters:
        clinical_data (pd.DataFrame): The clinical data DataFrame.
        case_id_col (str): The column name representing the case ID.

    Returns:
        list: A list of dicts, one per unique case ID, with:
              - 'case_id': the case ID value
              - 'row_count': number of rows for this case
              - 'status': 'unique' if only one row, else list of columns where rows differ
    """
    results = []

    for case_id, group in clinical_data.groupby(case_id_col):
        entry = {"case_id": case_id, "row_count": len(group)}

        if len(group) == 1:
            entry["status"] = "unique"
        else:
            # Drop the case_id column itself before comparing
            compare_df = group.drop(columns=[case_id_col])

            # Find columns where not all values are the same across rows
            differing_cols = [
                col for col in compare_df.columns
                if compare_df[col].nunique(dropna=False) > 1
            ]

            entry["status"] = differing_cols if differing_cols else "duplicate_identical"

        results.append(entry)

    return results