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

    def map_db2answer(self, answer):
        return {
               'findUser': answer,
               'addUser': self.map_dict2User(parms_dict),
               'modUser': self.map_dict2User(parms_dict),
           }[answer]


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
        print("db_mapper.map_query2db query: %r" % (query))

        q2db = {
            'findUser': self.__db__.findUser,
            'addUser': self.__db__.addUser,
            'modUser': self.__db__.addUser,
        }
        if query in q2db.keys():
            return q2db[query]
        else:
            return None

    def map_parms2db(self, query, parms):
        print("db_mapper.map_parms2db query: %r, parms: %r" % (query, parms))
        parms_dict = dict(cgi.parse_qsl(parms))

        print(">..... %r" %parms_dict)
        print("MMMMMMMMMMMMMMMMMM %s" % self.map_dict2User(parms_dict).toString())
        return {
            'findUser': parms_dict.get('username', '%'),
            'addUser': self.map_dict2User(parms_dict),
            'modUser': self.map_dict2User(parms_dict),
        }[query]

    def map_dict2User(self, parms):
        for k in parms.keys():
            print("..... iterate %r, %r" % (k, parms[k]))
            try:
                parms[k] = int(parms[k])
            except:
                pass
            print("..... iterate %r, %r" % (k, parms[k]))

        newUser = db_layer.User()
        return newUser.fromdict(parms)

if __name__ == "__main__":

    handler = db_handler()
    answer = handler.handle_request(query="findUser", parms="username=%")
    if answer != None:
        #print(answer.JSONdump())
        #for instance in answer:
        print(answer)
        #print( json.dumps(answer, cls=AlchemyEncoder))

