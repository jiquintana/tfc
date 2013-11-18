/*
Created: 16/11/2013
Modified: 16/11/2013
Model: Universal
Database: SQLite 3.7
*/



-- Create tables section -------------------------------------------------

-- Table Proxy_Users

CREATE TABLE Proxy_Users
(
  uid INTEGER NOT NULL,
  user TEXT NOT NULL,
  password_hash TEXT,
  description TEXT,
  CONSTRAINT pk_uid PRIMARY KEY (uid),
  CONSTRAINT uid UNIQUE (uid)
);

CREATE UNIQUE INDEX idx_uid ON Proxy_Users (uid);

CREATE UNIQUE INDEX idx_user ON Proxy_Users (user);

-- Table Proxy_Groups

CREATE TABLE Proxy_Groups
(
  gid INTEGER NOT NULL,
  description TEXT,
  CONSTRAINT pk_gid PRIMARY KEY (gid),
  CONSTRAINT gid UNIQUE (gid)
);

CREATE UNIQUE INDEX idx_gid ON Proxy_Groups (gid);

-- Table Proxy_rules_TIME

CREATE TABLE Proxy_rules_TIME
(
  trid INTEGER NOT NULL,
  rule_time_start NONE NOT NULL,
  rule_time_end NONE NOT NULL,
  CONSTRAINT pk_trid PRIMARY KEY (trid),
  CONSTRAINT trid UNIQUE (trid)
);

CREATE UNIQUE INDEX idx_trid ON Proxy_rules_TIME (trid);

CREATE INDEX idx_time_start ON Proxy_rules_TIME (rule_time_start);

CREATE INDEX idx_time_end ON Proxy_rules_TIME (rule_time_end);

-- Table Proxy_rules_URIS

CREATE TABLE Proxy_rules_URIS
(
  urid INTEGER NOT NULL,
  rule_uri TEXT,
  CONSTRAINT pk_urid PRIMARY KEY (urid),
  CONSTRAINT urid UNIQUE (urid)
);

CREATE UNIQUE INDEX idx_urid ON Proxy_rules_URIS (urid);

CREATE UNIQUE INDEX idx_uri ON Proxy_rules_URIS (rule_uri);

-- Table Proxy_rules_WORDS

CREATE TABLE Proxy_rules_WORDS
(
  wrid INTEGER NOT NULL,
  words TEXT,
  CONSTRAINT pk_wrid PRIMARY KEY (wrid),
  CONSTRAINT wrid UNIQUE (wrid)
);

CREATE UNIQUE INDEX idx_wrid ON Proxy_rules_WORDS (wrid);

CREATE UNIQUE INDEX idx_words ON Proxy_rules_WORDS (words);

-- Table _map_group2time

CREATE TABLE _map_group2time
(
  gid INTEGER NOT NULL,
  trid INTEGER NOT NULL,
  CONSTRAINT pk_map_group2time PRIMARY KEY (gid,trid),
  CONSTRAINT time_allowed FOREIGN KEY (trid) REFERENCES Proxy_rules_TIME (trid),
  CONSTRAINT allowed_times FOREIGN KEY (gid) REFERENCES Proxy_Groups (gid)
);

CREATE INDEX idx_group2time_trid ON _map_group2time (trid);

CREATE INDEX idx_group2time_gid ON _map_group2time (gid);

-- Table _map_group2uri

CREATE TABLE _map_group2uri
(
  gid INTEGER NOT NULL,
  urid INTEGER NOT NULL,
  CONSTRAINT pk_map_group2uri PRIMARY KEY (gid,urid),
  CONSTRAINT allowed_uris FOREIGN KEY (gid) REFERENCES Proxy_Groups (gid),
  CONSTRAINT uris_allowed FOREIGN KEY (urid) REFERENCES Proxy_rules_URIS (urid)
);

CREATE INDEX idx_group2uri_urid ON _map_group2uri (urid);

CREATE INDEX idx_group2uri_gid ON _map_group2uri (gid);

-- Table _map_group2word

CREATE TABLE _map_group2word
(
  gid INTEGER NOT NULL,
  wrid INTEGER NOT NULL,
  CONSTRAINT pk_map_group2word PRIMARY KEY (gid,wrid),
  CONSTRAINT words_allowed FOREIGN KEY (wrid) REFERENCES Proxy_rules_WORDS (wrid),
  CONSTRAINT allowed_words FOREIGN KEY (gid) REFERENCES Proxy_Groups (gid)
);

CREATE INDEX idx_group2word_wrid ON _map_group2word (wrid);

CREATE INDEX idx_group2word_gid ON _map_group2word (gid);

-- Table _map_user2group

CREATE TABLE _map_user2group
(
  uid INTEGER NOT NULL,
  gid INTEGER NOT NULL,
  CONSTRAINT pk_map_user2group PRIMARY KEY (uid,gid),
  CONSTRAINT Pertenece FOREIGN KEY (uid) REFERENCES Proxy_Users (uid),
  CONSTRAINT Contiene FOREIGN KEY (gid) REFERENCES Proxy_Groups (gid)
);

CREATE INDEX idx_user2group_uid ON _map_user2group (uid);

CREATE INDEX idx_user2group_gid ON _map_user2group (gid);




