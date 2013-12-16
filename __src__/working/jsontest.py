import db_layer
import json

########################################################################
User = {
    'uid' : 110,
    'username' : 'pep',
    'rol' : 'A',
    'password': 'blah',
    'description' : 'another blah',
    'L_AH' : 2,
    'M_AH' : 3,
    'X_AH' : 4,
    'J_AH' : 5,
    'V_AH' : 6,
    'S_AH' : 7,
    'D_AH' : 8
}


if __name__ == "__main__":
    theS = '{"password": "blah", "D_AH": 8, "uid": 110, "M_AH": 3, "X_AH": 4, "L_AH": 2, "J_AH": 5, "rol": "A", "S_AH": 7, "username": "pep", "V_AH": 6, "description": "another blah"}'

    theU = db_layer.User().fromjson(theS)

    print("%r" % theU)
    print("%s" % theU.toString())