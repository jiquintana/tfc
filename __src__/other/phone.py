#!/usr/bin/env python
 
numbers = {"2" : ["A", "B", "C"],
           "3" : ["D", "E", "F"],
           "4" : ["G", "H", "I"],
           "5" : ["J", "K", "L"],
           "6" : ["M", "N", "O"],
           "7" : ["P", "Q", "R"],
           "8" : ["S", "T", "U"],
           "9" : ["V", "W", "X"],
           "0" : ["Y", "Z"]}
 
def generate(input_list):
	return gen(input_list, 0, "")
 
def gen(input_list, index, n):
	if index > len(input_list)-1: return [n]
	output_list = []
	for i in input_list[index]:
		index += 1
		for x in numbers[i]:
			tmp = gen(input_list, index, x)
           		for t in tmp:
		        	output_list.append(n + t)
	return output_list
     
if __name__ == "__main__":
	for i in generate(["6", "7", "2", "0","6","4","2"]): print i
