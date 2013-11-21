/*
-*- coding: utf-8 -*-
 vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number:
 */

CREATE TABLE USERS (
  uid INTEGER AUTO_INCREMENT,
  name VARCHAR(20) NOT NULL,
  password_hash VARCHAR(80),
  description VARCHAR(80),
  CONSTRAINT pk_uid PRIMARY KEY (uid),
  CONSTRAINT uid UNIQUE (uid)
);

CREATE TABLE GROUPS (
  gid INTEGER AUTO_INCREMENT,
  description VARCHAR(80),
  CONSTRAINT pk_gid PRIMARY KEY (gid),
  CONSTRAINT gid UNIQUE (gid)
);

CREATE TABLE RULES_TIME (
  rtid INTEGER AUTO_INCREMENT,
  CONSTRAINT pk_rtid PRIMARY KEY (rtid),
  CONSTRAINT rtid UNIQUE (rtid)
);

CREATE TABLE RULES_URIS (
  ruid INTEGER AUTO_INCREMENT,
  rule_uri VARCHAR(256),
  CONSTRAINT pk_ruid PRIMARY KEY (ruid),
  CONSTRAINT ruid UNIQUE (ruid)
);

CREATE TABLE RULES_WORDS (
  rwid INTEGER AUTO_INCREMENT,
  words VARCHAR(256),
  CONSTRAINT pk_rwid PRIMARY KEY (rwid),
  CONSTRAINT rwid UNIQUE (rwid)
);

CREATE TABLE _M_G2T (
  gid INTEGER NOT NULL,
  rtid INTEGER NOT NULL,
  CONSTRAINT pk_m_g2t PRIMARY KEY (gid,rtid),
  CONSTRAINT time_allowed FOREIGN KEY (rtid)  REFERENCES RULES_TIME (rtid),
  CONSTRAINT allowed_time FOREIGN KEY (gid)   REFERENCES GROUPS (gid)
);

CREATE TABLE _M_G2U (
  gid INTEGER NOT NULL,
  ruid INTEGER NOT NULL,
  CONSTRAINT pk_m_g2u PRIMARY KEY (gid,ruid),
  CONSTRAINT uris_allowed FOREIGN KEY (ruid)  REFERENCES RULES_URIS (ruid),
  CONSTRAINT allowed_uris FOREIGN KEY (gid)   REFERENCES GROUPS (gid)
);

CREATE TABLE _M_G2W (
  gid INTEGER NOT NULL,
  rwid INTEGER NOT NULL,
  CONSTRAINT pk_mg2w PRIMARY KEY (gid,rwid),
  CONSTRAINT words_allowed FOREIGN KEY (rwid) REFERENCES RULES_WORDS (rwid),
  CONSTRAINT allowed_words FOREIGN KEY (gid)  REFERENCES GROUPS (gid)
);


CREATE TABLE _M_U2G (
  uid INTEGER NOT NULL,
  gid INTEGER NOT NULL,
  CONSTRAINT pk_mu2g PRIMARY KEY (uid,gid),
  CONSTRAINT pertenece    FOREIGN KEY (uid) REFERENCES USERS (uid),
  CONSTRAINT contiene     FOREIGN KEY (gid) REFERENCES GROUPS (gid)
);


--- Indexes section
CREATE UNIQUE INDEX idx_uid   ON USERS (uid);
CREATE UNIQUE INDEX idx_name  ON USERS (name);
CREATE UNIQUE INDEX idx_gid   ON GROUPS (gid);
CREATE UNIQUE INDEX idx_rtid  ON RULES_TIME (rtid);
CREATE UNIQUE INDEX idx_ruid  ON RULES_URIS (ruid);
CREATE UNIQUE INDEX idx_rwid  ON RULES_WORDS (rwid);
CREATE UNIQUE INDEX idx_uri   ON RULES_URIS (rule_uri);
CREATE UNIQUE INDEX idx_words ON RULES_WORDS (words);

CREATE INDEX idx_g2ti_rtid    ON _M_G2T (rtid);
CREATE INDEX idx_g2ti_gid     ON _M_G2T (gid);
CREATE INDEX idx_g2ur_ruid    ON _M_G2U (ruid);
CREATE INDEX idx_g2ur_gid     ON _M_G2U (gid);
CREATE INDEX idx_g2wo_rwid    ON _M_G2W (rwid);
CREATE INDEX idx_g2wo_gid     ON _M_G2W (gid);
CREATE INDEX idx_u2g_uid      ON _M_U2G (uid);
CREATE INDEX idx_u2g_gid      ON _M_U2G (gid);







