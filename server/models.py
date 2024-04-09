from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self, key, name):
            if not name:
                raise ValueError('Name cannot be empty.')

            existing_author = Author.query.filter(Author.name == name).first()
            if existing_author:
                raise ValueError('An author with this name already exists.')

            else:
                return name


    
        
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError('Phone number must be exactly ten digits.')
        return phone_number
        
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        if not len(content) >= 250:
            raise ValueError('Content must be at least 250 characters long.')
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if not len(summary) <= 250:
            raise ValueError('Summary must be less than or equal to 250 characters.')
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category not in ('Fiction', 'Non-Fiction'):
            raise ValueError('Category must be Fiction or Non-Fiction.')
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        if not any(keyword in title for keyword in ["Won't Believe", "Secret", "Top", "Guess"]):
            raise ValueError("Title must contain at least one of: Won't Believe, Secret, Top, or Guess.")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
