from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace with your actual database URI
DATABASE_URI = 'mysql+pymysql://afockens:DAfense101!!@users-db.cl0ukeemwuxg.us-east-2.rds.amazonaws.com:3306/accounts'

# Set up the SQLAlchemy engine and session
engine = create_engine(DATABASE_URI)
Base = declarative_base()

# Define the User model (make sure it matches your database schema)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

# Create a session
Session = sessionmaker(bind=engine)
engine.dispose()  # Dispose of the connection pool to refresh
session = Session()

try:
    # Query all users
    users = session.query(User).all()

    if not users:
        print("No users found in the database.")
    else:
        print("Current users and their data:")
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Password Hash: {user.password_hash}")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the session
    session.close()