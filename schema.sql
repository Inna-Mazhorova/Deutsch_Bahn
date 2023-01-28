DROP DATABASE IF EXISTS 'deutsche_bahn';
CREATE DATABASE 'deutsche_bahn';
USE 'deutsche_bahn';

DROP TABLE IF EXISTS 'Orders';
CREATE TABLE 'Orders' (
  'OrderTime' datetime,
  'Item' varchar(100) NOT NULL
);