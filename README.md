数据库
======
createuser -P -e hjh (密码: 1234)
createdb -O hjh -E utf8 money

psql -h localhost -U hjh -d money < ./initdata/schema.sql
psql -h localhost -U hjh -d money < ./initdata/func.sql

初始化命令
==========

导入业务数据
flask init-data

建用户表
flask create-db

初始化用户表数据
flask init-user
