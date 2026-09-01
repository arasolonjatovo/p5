import pandas as pd
from database import Base, engine


def init_db(csv_fp: str = None):
    print("Réinitialisation des tables")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Tables créées")

    if csv_fp:
        df = pd.read_csv(csv_fp)

        if "Unnamed: 0" in df.columns:
            df = df.drop(columns=["Unnamed: 0"])

        df.to_sql(name="dataset", con=engine, if_exists="append", index=False)
        print("Dataset injecté")


if __name__ == "__main__":
    init_db()