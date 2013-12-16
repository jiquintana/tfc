#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

import db_layer
import json
import cgi


class db_handler():
    __db__ = None

    def __init__(self):
        self.__db__ = db_layer.Database()


    def handle_request(self, query, parms):
        print("handle_request: query: %r parms: %r" % (query, parms))
        #function =
        #print(function)
        #answer = function(parms)
        #print(answer)
        hook = self.map_query2db(query)
        if hook:
            answer =  hook(self.map_parms2db(query, parms))
            return answer
        else:
            return ''


    def map_query2db(self, query):
        q2db = {
            'findUser': self.__db__.findUser
        }
        if query in q2db.keys():
            return q2db[query]
        else:
            return None

    def map_parms2db(self, query, parms):
        #print(parms)
        parms_dict = dict(cgi.parse_qsl(parms))
        #print(parms_dict)
        return {
            'findUser': parms_dict.get('username', '%'),
        }[query]

if __name__ == "__main__":

    handler = db_handler()
    answer = handler.handle_request(query="findUser", parms="username=%")
    if answer != None:
        #print(answer.JSONdump())
        #for instance in answer:
        print(answer)
        #print( json.dumps(answer, cls=AlchemyEncoder))

