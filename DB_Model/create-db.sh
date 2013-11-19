#!/bin/bash
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

help () {
    echo -e "Sintaxis: $0 <database_type>"
    echo -e ""
    echo -e "siendo <database_type> una de las siguientes:"
    echo -e "\tmysql"
    echo -e "\tsqlite3"
    echo -e "\tpostgres"
    echo -e ""
}
if [ $# -lt 1 ]; then
    echo -e "Error:: No he recibido parametros"
    help
    exit -1
fi

DATABASE=`echo $1 | tr '[:upper:]' '[:lower:]'`
case $DATABASE in
    mysql)
        MYDATABASE=`cat SQL.DB`
        MYUSER=`cat SQL.USER`
        MYPASS=`cat SQL.PASSWD`
        export MYDATABASE MYUSER
        cat drop.mysql.template | sed "s/@USER/$MYUSER/g;s/@DATABASE/$MYDATABASE/g" > drop.mysql.sql
        mysql -t -vvv -e "source drop.mysql.sql"
        cat create.mysql.template | sed "s/@USER/$MYUSER/g;s/@DATABASE/$MYDATABASE/gi;s/@PASSWD/`cat SQL.PASSWD`/g;" > create.mysql.sql
        mysql -t -vvv -e "source create.mysql.sql"
        #cat mysql -u proxy --password=proxypass proxy
        mysql -t -vvv -u proxy --password=proxypass proxy -e "source DDL.sql"
        ;;
    sqlite3)
        SQLITEDATABASE=`cat SQL.DB`.db
        rm -rf $SQLITEDATABASE
        sqlite3 $SQLITEDATABASE -init DDL.sql
        ;;
    postgres)
        PGDATABASE=`cat SQL.DB`
        PGUSER=`cat SQL.USER`
        PGPASSFILE=`pwd`/.pgpass
        export PGDATABASE PGUSER PGPASSFILE
        #su - postgres -c "dropdb $PGDATABASE; dropuser $PGUSER ; createuser $PGUSER ; createdb -O $PGUSER $PGDATABASE"
        cat drop.postgres.template | sed "s/@USER/$PGUSER/g;s/@DATABASE/$PGDATABASE/g" > drop.postgres.sql
        su - postgres -c "psql -f `pwd`/drop.postgres.sql"
        cat create.postgres.template | sed "s/@USER/$PGUSER/g;s/@DATABASE/$PGDATABASE/g;s/@PASSWD/`cat SQL.PASSWD`/g;" > create.postgres.sql
        su - postgres -c "psql -f `pwd`/create.postgres.sql"
        echo "*:*:$PGDATABASE:$PGUSER:`cat SQL.PASSWD`" > ./.pgpass
        chmod 600 ./.pgpass
        psql -f DDL.postgres.sql

        ;;
    *)
        echo -e "Error:: paramertro no soportado"
        help
        exit -1
        ;;
esac
