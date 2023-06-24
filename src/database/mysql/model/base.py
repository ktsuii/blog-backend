from sqlalchemy.orm import declarative_base

Base = declarative_base()


def to_dict(self: Base):
    return {col.name: getattr(self, col.name) for col in all_columns(self)}


Base.to_dict = to_dict


def all_columns(_model):
    return list(_model.__table__.columns)


if __name__ == '__main__':
    pass
