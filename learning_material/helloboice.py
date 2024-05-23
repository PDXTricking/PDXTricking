print("hello world")
print("hello boice")


# This is a comment
print("hello boice")
#if <condition> : "colon"
#   then you tab for what to do if its true.
# == means  "is this equal"
# < less
# < greater
# <= less than or equal
# >= greater than or equal 
# != Not equal


if 1 == 2: #is the number 1 the same as the number 2 -> False
    #Goes here if its true
    print("it is true1")
elif 2 == 4: #else if
    print("it is true2") #Stops when it hits true
elif 3 == 3: #else if
    print("it is true3")
else: #else only happens if all ifs and elifs are false
    #goes here if its false
    print("this is false")

#Variables
#<name> = <value>
# = sign means "set"

#datatypes
#int
this_integer = 4
#strings
this_is_a_string = "me string yay 1234"
#boolean
this_boolean = True

#This is a list
#do make a list
# nameOfList = [<things>,<thing2>,<thing4>]

rcgData = ["boice", 4, 4, "adam"]
player_names = ["Alice", 3, "Charlie", False, True, 4, "Frank", "Boice", rcgData]

list_of_nums = [2,3434,4,69,6,7]
list_of_nums.sort()
print(list_of_nums)
print(player_names[4],  player_names[4])
print("end of program")



#Dictionary
#key value pair
#to make one:
this_dict = {
            "tyson": "value1",
            "ray": "community manager",
            "adam": False,
            "boice": [4,5],
            "names": {"boice": 2}
            }

print(this_dict["tyson"])
print(this_dict["adam"])
print("Hello world")
print(this_dict["ray"])
print(this_dict["tyson"])   