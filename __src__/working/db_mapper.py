#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

import db_layer
import json
import cgi

DEBUGCALL = False
DEBUGANSWER = False
DEBUG = False


class db_handler():
    __db__ = None

    def __init__(self):
        self.__db__ = db_layer.Database()

    def answer_wrapper(self, to_type, answer):
        if DEBUGCALL: print("answer_wrapper.call: (to_type %r, parms: %r)" % (to_type, answer))

        wrapped_answer = { 'typeinfo': '',
                           'answer': '',
                           'size': 0,
                           'code': 0}

        wrapped_answer['typeinfo'] = to_type

        if to_type == 'json':
            wrapped_answer['answer'] = answer
        elif to_type == 'html':
            wrapped_answer['answer'] = '<HTML><BODY><PRE>%r</PRE><a href="javascript: self.close()">Close Window</a></BODY></HTML>' % answer

        wrapped_answer['size'] = len(str(wrapped_answer['answer']))

        if DEBUGANSWER: print("answer_wrapper.return: (%r)" % wrapped_answer)

        return wrapped_answer


    def map_db2answer(self, query, answer):
        if DEBUGCALL: print("map_db2answer.call (query: %r, type %r, answer: %r)" % (query, type(answer), answer))


        printed_answer = {
            'findUser': self.answer_wrapper('json', answer),
            'addUser': self.answer_wrapper('html', answer),
            'modUser': self.answer_wrapper('html', answer),
            'delUser': self.answer_wrapper('html', answer),
            'findGroup': self.answer_wrapper('json', answer),
            'addGroup':self.answer_wrapper('html', answer),
            'modGroup': self.answer_wrapper('html', answer),
            'delGroup': self.answer_wrapper('html', answer),
            'groupsuserISmember': self.answer_wrapper('json', answer),
            'groupsuserNOTmember': self.answer_wrapper('json', answer),
            'addUserToGroup': self.answer_wrapper('html', answer),
            'delUserFromGroup': self.answer_wrapper('html', answer),
            
        }[query]


        '''
        if query == 'findUser':
            printed_answer =  self.answer_wrapper('json', answer)
        elif query == 'addUser':
            printed_answer =   self.answer_wrapper('html', answer)
        elif query == 'modUser':
            printed_answer =   self.answer_wrapper('html', answer)
        elif query == 'delUser':
            printed_answer =   self.answer_wrapper('html', answer)
        elif query == 'findGroup':
            printed_answer =   self.answer_wrapper('json', answer)
        elif query == 'addGroup':
            printed_answer =   self.answer_wrapper('html', answer)
        elif query == 'modGroup':
            printed_answer =   self.answer_wrapper('html', answer)
         '''

        if DEBUGANSWER: print("map_db2answer.return: (%r)" %  printed_answer)
        return printed_answer



    def handle_request(self, query, parms):
        if DEBUGCALL: print("handle_request.call: (query: %r parms: %r)" % (query, parms))
        #function =
        #print(function)
        #answer = function(parms)
        #print(answer)

        hook = self.map_query2db(query)
        #print("->>>> %r" % str(self.map_parms2db(query, parms)))
        if hook:
            answer =  self.map_db2answer(query, hook(self.map_parms2db(query, parms)))
        else:
            answer = None

        if DEBUGANSWER: print("handle_request.return: (%r)" % answer )

        return answer


    def map_query2db(self, query):
        if DEBUGCALL: print("map_query2db.call (query: %r)" % (query))

        q2db = {
            'findUser': self.__db__.findUser,
            'addUser': self.__db__.addUser,
            'modUser': self.__db__.changeUser,
            'delUser': self.__db__.delUser,
            'findGroup': self.__db__.findGroup,
            'addGroup': self.__db__.addGroup,
            'modGroup': self.__db__.changeGroup,
            'delGroup': self.__db__.delGroup,
            'groupsuserISmember': self.__db__.findGroupsByUser,
            'groupsuserNOTmember': self.__db__.findNotGroupsByUser,
            'addUserToGroup': self.__db__.wr_addRelation,
            'delUserFromGroup': self.__db__.wr_delRelation,
        }

        if query in q2db.keys():
            answer = q2db[query]
        else:
            answer = None

        if DEBUGANSWER: print("map_query2db.return (%r)" % answer)
        return answer

    def map_parms2db(self, query, parms):
        if DEBUGCALL: print("map_parms2db.call: (query: %r parms: %r)" % (query, parms))
        parms_dict = dict(cgi.parse_qsl(parms))

        # print(">..... %r" %parms_dict)
        if DEBUG: print("MMMMMMMMMMMMMMMMMM %s" % self.map_dict2User(parms_dict).toString())
        answer = {
            'findUser': parms_dict.get('username', '%'),
            'addUser': self.map_dict2User(parms_dict),
            'modUser': self.map_dict2User(parms_dict),
            'delUser': self.map_dict2User(parms_dict),
            'findGroup': parms_dict.get('groupname', '%'),
            'addGroup': self.map_dict2Group(parms_dict),
            'modGroup': self.map_dict2Group(parms_dict),
            'delGroup': self.map_dict2Group(parms_dict),
            'groupsuserISmember': parms_dict.get('username', '%'),
            'groupsuserNOTmember': parms_dict.get('username', '%'),
            'addUserToGroup': parms_dict, 
            'delUserFromGroup': parms_dict,
            
        }[query]

        if DEBUGANSWER: print("map_parms2db.return (%r)" % answer)
        return answer

    def map_dict2User(self, parms):
        if DEBUGCALL: print("map_dict2User.call: (type %s parms: %r)" % (type(parms), parms))
        if parms == None:
            answer = None
        elif(type(parms) == dict):
            # print(type(parms))

            newUser = db_layer.User()
            for k in parms:
                if k in newUser.intColumns():
                    #print("..... iterate %r, %r" % (k, parms[k]))
                    try:
                        parms[k] = int(parms[k])
                    except:
                        pass
                    #print("..... iterate %r, %r" % (k, parms[k]))


            newUser.fromdict(parms)

            answer = newUser

        if DEBUGANSWER: print("map_dict2User.return (%r)" % answer)
        return answer

    def map_dict2Group(self, parms):
        if DEBUGCALL: print("map_dict2Group.call: (type %s parms: %r)" % (type(parms), parms))
        if parms == None:
            answer = None
        elif(type(parms) == dict):
            # print(type(parms))

            newGroup = db_layer.Group()
            for k in parms:
                if k in newGroup.intColumns():
                    #print("..... iterate %r, %r" % (k, parms[k]))
                    try:
                        parms[k] = int(parms[k])
                    except:
                        pass
                    #print("..... iterate %r, %r" % (k, parms[k]))


            newGroup.fromdict(parms)

            answer = newGroup

        if DEBUGANSWER: print("map_dict2Group.return (%r)" % answer)
        return answer

if __name__ == "__main__":

    handler = db_handler()
    answer = handler.handle_request(query="findUser", parms="username=%")
    if answer != None:
        #print(answer.JSONdump())
        #for instance in answer:
        print(answer)
        #print( json.dumps(answer, cls=AlchemyEncoder))

