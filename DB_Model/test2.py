#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////proxy.db'
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'USERS'
    uid = db.Column(db.Integer),
    name = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(80))
    description = db.Column(db.String(80))

    def __init__(self, name, password_hash, description):
        self.name = name
        self.password_hash = password_hash
        self.description = description
        
        
    def __repr__(self):
        return '<User %r>' % self.name

users = Users.query.all()