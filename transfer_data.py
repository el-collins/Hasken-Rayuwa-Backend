from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.links import Link
from models.users import User
from models.states import StateData
# from models.blogs import Blog


# SQLite database URL
sqlite_url = "sqlite:///./dev.sqlite"
sqlite_engine = create_engine(sqlite_url)

# PostgreSQL database URL
postgres_url = "postgresql://hasken_rayuwa_w562_user:MJWlTS2psJcrlijKzoCwOl3CaXatNTuX@dpg-cqlbio3qf0us7398uqi0-a.oregon-postgres.render.com/hasken_rayuwa_w562"
postgres_engine = create_engine(postgres_url)

# Create sessions
SQLiteSession = sessionmaker(bind=sqlite_engine)
sqlite_session = SQLiteSession()

PostgresSession = sessionmaker(bind=postgres_engine)
postgres_session = PostgresSession()

# Reflect tables from SQLite
StateData.metadata.create_all(postgres_engine)  # Create tables in PostgreSQL

# Define the transfer function
def transfer_table_data(model):
    records = sqlite_session.query(model).all()
    for record in records:
        postgres_session.merge(record)  # merge will insert or update the record
    postgres_session.commit()

# Transfer data for each table
transfer_table_data(Link)
transfer_table_data(User)
# transfer_table_data(Blog)
transfer_table_data(StateData)

# Close sessions
sqlite_session.close()
postgres_session.close()