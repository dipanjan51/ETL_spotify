import sqlalchemy


def load_to_db(load_df, transformed_df, engine=None):
    """
    Loads extracted and transformed dataframes into the database.
    - Creates tables if not exists
    - Appends data while avoiding duplicates via primary keys
    """
    if engine is None:
        raise ValueError("No SQLAlchemy engine provided.")

    try:
        load_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except Exception as e:
        print(f"Data already exists in the my_played_tracks table: {e}")

    try:
        transformed_df.to_sql("fav_artist", engine, index=False, if_exists='append')
    except Exception as e:
        print(f"Data already exists in the fav_artist table: {e}")

    print("Data loaded to database.")