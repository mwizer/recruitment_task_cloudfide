import pandas as pd
import re

def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    """
    Function for creating new DataFrame with old data and new columns

    Input:
    df - pd.DataFrame - old data
    role - str - string representation of math expression
    new_column - str - name of new column

    Return:
    new_df - pd.DataFrame
    """

    def _addition(df_temp, col1, col2, new_col, idx):
        if idx == 0:
            df_temp[new_col] = df_temp[col1] + df_temp[col2]
        else:
            df_temp[new_col] += df_temp[col2]
        return df_temp.copy(deep=True)

    def _subtraction(df_temp, col1, col2, new_col, idx):
        if idx == 0:
            df_temp[new_col] = df_temp[col1] - df_temp[col2]
        else:
            df_temp[new_col] -= df_temp[col2]
        return df_temp.copy(deep=True)

    def _multiplication(df_temp, col1, col2, new_col, idx):
        if idx == 0:
            df_temp[new_col] = df_temp[col1] * df_temp[col2]
        else:
            df_temp[new_col] *= df_temp[col2]
        return df_temp.copy(deep=True)

    # ~~~~~~ validation and extraction of data from "role"

    # ~~ first i want to validate columns cause this will be the fastest
    validate_columns = [
        True if re.search("^[A-Za-z_]+$", col) is not None else False
        for col in df.columns
    ]
    if not all(validate_columns) or (re.search("^[A-Za-z_]+$", new_column) is None):
        print("Wrong column names")
        return pd.DataFrame([])

    # ~~ now i want to extract data from role and then continue validation based on it
    allowed_operations = ["+", "-", "*"]
    pattern_operations = f"[{re.escape(''.join(allowed_operations))}]"

    if re.search(
        f"^[{re.escape(''.join(allowed_operations))}]", role.strip()
    ) or re.search(f"[{re.escape(''.join(allowed_operations))}]$", role.strip()):
        print("Role starts or ends with an operator")
        return pd.DataFrame([])

    role_data = {
        "operations": re.findall(pattern_operations, role),
        "cols": [
            col.strip() for col in re.split(pattern_operations, role) if col.strip()
        ],
    }

    # i could look if there is simple operation, but I didnt find in task that there cant be multiple columns. So it may take a bit more time to check it all, but i prefer to be ready for "what if it is in second validation" situation.
    if len(role_data["operations"]) < 1:
        print("didnt find acceptable math func")
        return pd.DataFrame([])

    validate_role_cols = [
        True if re.search("^[A-Za-z_]+$", col) is not None else False
        for col in role_data["cols"]
    ]
    validate_role_cols_exists = [
        True if col in df.columns else False for col in role_data["cols"]
    ]
    if not all(validate_role_cols) or not all(validate_role_cols_exists):
        print("Wrong column names in roles")
        return pd.DataFrame([])

    # ~~~~~~ processing operations

    df_new = df.copy(deep=True)
    
    # ok never mind. I dont want to lose points bcs of it. But rip performance
    for col in role_data["cols"]:
        if not pd.api.types.is_numeric_dtype(df_new[col]):
            try:
                df_new[col] = pd.to_numeric(df_new[col])
            except Exception as e:
                print('Data is not numeric and cant be converted')
                return pd.DataFrame([])

    for idx, operator in enumerate(role_data["operations"]):
        col1 = role_data["cols"][idx]
        col2 = role_data["cols"][idx + 1]
        if operator == "+":
            df_new = _addition(df_new, col1, col2, new_column, idx)
        elif operator == "-":
            df_new = _subtraction(df_new, col1, col2, new_column, idx)
        elif operator == "*":
            df_new = _multiplication(df_new, col1, col2, new_column, idx)
    return df_new.copy(deep=True)

if __name__ == "__main__":
    # simple test
    df_exmpl = pd.DataFrame(
        {
            "xyz": ['1.4', '2', '3'],
            "x_z": [1, 2, 3],
            # "x5z": [1, 2, 3],
            # "x.z": [1, 2, 3],
            # 'x z': [1, 2,3]
        }
    )
    print(add_virtual_column(df_exmpl, "xyz + x_z - xyz * x_z", "new_col"))
    print(add_virtual_column(df_exmpl, "xyz +x_z", "new_col"))
    # print(add_virtual_column(df_exmpl, "xyz /xyza", "new_col"))
