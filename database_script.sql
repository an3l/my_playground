CREATE DATABASE ekoforumdb CHARACTER SET UTF8;
use ekoforumdb;
# Air Quality Index:
# http://www.fhmzbih.gov.ba/latinica/ZRAK/AQI-satne.php
create table table_so2 (id int,city varchar, _location varchar, _value int, _date datetime);
create table table_h2s (id int,city varchar, _location varchar, _value int, _date datetime);
create table table_no2 (id int,city varchar, _location varchar, _value int, _date datetime);
create table table_nox (id int,city varchar, _location varchar, _value int, _date datetime);
create table table_no (id int,city varchar, _location varchar, _value int, _date datetime);
create table table_co (id int,city varchar, _location varchar, _value int, _date datetime);
create table table_o3 (id int,city varchar, _location varchar, _value int, _date datetime);
create table table_pm10 (id int,city varchar, _location varchar, _value int, _date datetime);
create table table_pm25 (id int,city varchar, _location varchar, _value int, _date datetime);
