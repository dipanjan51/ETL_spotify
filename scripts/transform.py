import pandas as pd

def Data_Quality(load_df):
    if load_df.empty:
        print('No Songs Extracted. Skipping Transformation')
        return False
    
    if not pd.Series(load_df['played_at']).is_unique:
        raise Exception("Primary Key Exception: 'played_at' column contains duplicate entries.")
    
    if load_df.isnull().values.any():
        raise Exception("Null values found in dataset.")
    
    return True  # If all checks passed


def Transform_df(load_df):

    Transformed_df=load_df.groupby(['timestamp','artist_name'],as_index = False).count()
    Transformed_df.rename(columns ={'played_at':'count'}, inplace=True)

    Transformed_df["id"] = Transformed_df['timestamp'].astype(str) +"-"+ Transformed_df["artist_name"]

    return Transformed_df[['id','timestamp','artist_name','count']]


if __name__ == "__main__":
    import extract
    load_df = extract.return_dataframe()

    if Data_Quality(load_df):
        Transformed_df=Transform_df(load_df) 
        print(Transformed_df)   
    else:
        print("Data Quality failed. No transformation performed.")
