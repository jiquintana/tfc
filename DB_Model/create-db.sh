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
        
        ;;
    sqlite3)
        ;;
    postgres)
        cat drop.postgres.template | sed "s/@USER/`cat SQL.USER`/g;s/@DATABASE/`cat SQL.DB`/g" > drop.postgres.sql
        su - postgres -c "psql -f `pwd`/drop.postgres.sql"
        cat create.postgres.template | sed "s/@USER/`cat SQL.USER`/g;s/@DATABASE/`cat SQL.DB`/g;s/@PASSWD/`cat SQL.PASSWD`/g;" > create.postgres.sql
        su - postgres -c "psql -f `pwd`/create.postgres.sql"
        echo "*:*:`cat SQL.DB`:`cat SQL.USER`:`cat SQL.PASSWD`" > ./.pgpass
        chmod 600 ./.pgpass
        PGDATABASE=`cat SQL.DB`
        PGUSER=`cat SQL.USER`
        export PGDATABASE PGUSER
        psql -f DDL.sql

        ;;
    *)
        echo -e "Error:: paramertro no soportado"
        help
        exit -1
        ;;
esac
