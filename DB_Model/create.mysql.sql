CREATE USER 'proxy' IDENTIFIED BY 'proxypass'; 
CREATE DATABASE proxy;
GRANT ALL PRIVILEGES ON proxy.* to 'proxy'@'%' identified by 'proxypass';
-- CREATE USER root WITH PASSWORD 'password'; 
-- GRANT ALL PRIVILEGES ON DATABASE proxy to root;
