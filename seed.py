from app import app
from models import db, User, Review, Comment


db.drop_all()
db.create_all()


user = User(
    username="Test",
    email="testing@gmail.com",
    password="$2b$12$Q1PUFjhN/AWRQ21LbGYvjeLpZZB6lfZ1BPwifHALGO6oIbyC3CmJe"
)

review = Review(
    title="Test Movie Title",
    rating=10,
    text="This is a test review",
    timestamp="2017-01-21 11:04:53.522807",
    user_id=1
)

comment = Comment(
    comment="This is a test comment",
    timestamp="2018-01-21 11:04:53.522807",
    user_id=1,
    review_id=1
)

db.session.commit()