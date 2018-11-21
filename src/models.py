from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date
)

meta = MetaData()

# Describe 'question' table
question = Table(
    'question', meta,

    Column('id', Integer, primary_key=True),
    Column('question_text', String(200), nullable=False),
    Column('pub_date', Date, nullable=False),
)

# Describe 'choice' table
choice = Table(
    'choice', meta,

    Column('id', Integer, primary_key=True),
    Column('choice_text', String(200), nullable=False),
    Column('votes', Integer, server_default='0', nullable=False),
    Column(
        'question_id',
        Integer,
        ForeignKey('question.id', ondelete='CASCADE')
    )
)
