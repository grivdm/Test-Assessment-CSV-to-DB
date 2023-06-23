from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configurations for the DB connection
engine = create_engine('*DATABASE_URL*')
Session = sessionmaker(bind=engine)



class DBSession:

    def __enter__(self):
        self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()