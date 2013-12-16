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
        answer =  self.map_query2db(query)(self.map_parms2db(query, parms))
        #print("---- answer:\n >%s<" % answer)
        return answer


    def map_query2db(self, query):
        return {
            'findUser': self.__db__.findUser,
        }[query]

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

