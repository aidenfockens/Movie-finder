from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

# Replace this URL with your actual RDS database URI
DATABASE_URI = 'mysql+pymysql://afockens:DAfense101!!@users-db.cl0ukeemwuxg.us-east-2.rds.amazonaws.com:3306/accounts'
engine = create_engine(DATABASE_URI)
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

# Create tables (if they don't exist already)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Test user details
username = 'testuser'
email = 'testuser@example.com'
password = 'securepassword'

# Check if the user already exists
existing_user = session.query(User).filter_by(username=username).first()
if existing_user:
    print('User already exists')
else:
    # Create a new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    session.add(new_user)
    session.commit()
    print('User added successfully')

# Close the session
session.close()
