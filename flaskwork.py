import os
import click
from app import create_app, db
from app.models import User

from app.dbwork import sqldb
from app import utils

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)

@app.cli.command()
def create_db():
    """创建数据表"""
    db.create_all()

@app.cli.command()
def drop_db():
    """删除数据表"""
    db.drop_all()

@app.cli.command()
def init_user():
    """创建用户"""
    u = User(username='admin', password='admin')
    db.session.add(u)
    db.session.commit()

@app.cli.command()
def init_data():
    """倒入原始数据"""

    d = utils.get_data('./initdata/data.csv')
    sdb = sqldb.SQLDB()
    results = []
    for r in d:
        x = r[0].split(',')
        results.append([x[0], x[1], x[2], x[3], x[4], x[5]])

    sdb.write_data(results)
