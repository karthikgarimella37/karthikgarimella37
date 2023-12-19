from re import match
from random import choice
from responses import response_map
# import transformers

reflections = {'i am': 'you are', 'i was': 'you were', 'i': 'you',
               "i'm": 'you are', "i'd": 'you would', "i've": 'you have',
               "i'll": 'you will', 'my': 'your', 'you are': 'I am',
               'you were': 'I was', "you've": 'I have', "you'll": 'I will',
               'your': 'my', 'yours': 'mine', 'you': 'me', 'me': 'you', 'my': 'your'}


user_characteristics = {"ducky_say": [], "user_say": [],
                        "user_problem": {"repeat": False}}


def input_processing(count):
    global user_characteristics
    if user_characteristics["user_say"][count] ==  \
            user_characteristics["user_say"][count-1] and count != 0:
        user_characteristics["user_problem"]["repeat"] = True


def main():

    global user_characteristics
    ducky_say = ""
    count = 0
    print("Ducky: Hello! How can I help you today? Quack")
    user_characteristics["ducky_say"].append(
        "Hello! How can I help you today? Quack")

    while True:

        user_input = input("You:   ")
        user_characteristics["user_say"].append(user_input.lower())
        input_processing(count)

        if user_input.lower() in ["bye", "goodbye", "exit"]:
            print("Ducky: Thanks for talking to me, byee")
            break

        elif user_characteristics["user_problem"]["repeat"]:
            ducky_say = choice(response_map["repeats"])
            user_characteristics["user_problem"]["repeat"] = False

        else:
            for pattern, response in response_map["gen_responses"].items():
                matcher = match(pattern, user_input.lower())

                if matcher:
                    group_list = ""
                    if matcher.groups():
                        group_list = [*matcher.groups()][0].split()

                        for key, value in reflections.items():

                            if key in group_list:
                                group_list = [
                                    l if l != key else value for l in group_list]

                    ducky_say = choice(response)
                    ducky_say = ducky_say.format(" ".join(group_list))
                    break

        quack = ""

        if choice([False, False, True, False]):
            quack = " Quack"

        print("Ducky: " + ducky_say + quack)
        user_characteristics["ducky_say"].append(ducky_say)
        count += 1


if __name__ == '__main__':
    main()
