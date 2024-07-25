from core.config import settings
from sqlmodel import Field, SQLModel, create_engine, Session, Column, String, Relationship

# database setup
engine = create_engine(str(settings.SQL_DATABASE_URI))


def start_engine():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session


def get_or_create_entity(db: Session, model, **kwargs):
    """
    Function to get an entity from the database based on the provided filter criteria, or create a new entity if it does not exist.

    Parameters:
    - db (Session): The database session to use for querying and creating entities.
    - model (SQLModel): The SQLModel class representing the entity to work with.
    - **kwargs: Arbitrary keyword arguments representing the filter criteria for querying the entity.

    Returns:
    - The retrieved or newly created entity based on the provided filter criteria.
    """
    entity = db.query(model).filter_by(**kwargs).first()
    if not entity:
        entity = model(**kwargs)
        db.add(entity)
        db.commit()
        db.refresh(entity)
    return entity

def update_instance(instance, data):
    for field, value in data.dict(exclude_unset=True).items():
        setattr(instance, field, value)
    db.commit()