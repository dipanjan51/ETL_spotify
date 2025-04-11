from extract import return_dataframe
from transform import Data_Quality, Transform_df
from load import load_to_db

def spotify_etl(engine):
    df = return_dataframe()

    if not Data_Quality(df):
        print("ETL terminated due to failed data quality.")
        return
    
    transformed_df = Transform_df(df)
    load_to_db(df, transformed_df, engine=engine)
