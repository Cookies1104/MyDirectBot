from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, ForeignKey, create_engine
from datetime import datetime

from sqlalchemy.orm import Session

metadata = MetaData()


engine = create_engine('postgresql+psycopg2://postgres:Zx12357810@localhost/telebot_bd', echo=True)
Session.configure(bind=engine)

# user = Table('user', metadata,
#              Column('id', Integer(), primary_key=True),
#              Column('telegram_id', Integer(), nullable=False)
#              )
#
# chapter = Table('chapter', metadata,
#                 Column('id', Integer(), autoincrement=True),
#                 Column('user_id', ForeignKey('user.id'), nullable=False),
#                 Column('chapter_name', String(255), nullable=False, index=True, primary_key=True),
#                 Column('create_date', DateTime(), default=datetime.now)
#                 )
#
element = Table('chapter', metadata,
                Column('element_id', Integer(), autoincrement=True),
                Column('name', String(20), nullable=False, index=True),
                Column('description', Text, nullable=False),
                Column('link', String(255), nullable=True),
                Column('user_id', Integer(), ForeignKey('user.id'), nullable=False, index=True),
                Column('chapter_name', String(255), ForeignKey('chapter.name'), nullable=False, index=True),
                Column('create_date', DateTime(), default=datetime.now),
                Column('update_date', DateTime(), default=datetime.now, onupdate=datetime.now)
                )

MetaData.create_all(engine)

