import re
import random


response_map={ 
"gen_responses": {
    r"(hello|hi|hey|yo|yooo)": ["Hi, how are you doing today?", "Howdy partner", ],
    r"i (.)* you": ["Me? really?", "I don't want to make this conversation about me...",
                     "We can talk all day about me, but it's pointless", "I'm empty to talk about", 
                     "I'm not real lol"],
    r"i feel (.)*": ["Can you tell me more about it?", "Do you think about it often?", 
                     "Have you told anyone else about this?", "Is this the first time you feel so?"],
    r"i (don't\s|didn't\s|do not\s|did not\s)?(like|love|play|buy|cry) (.)*":["Why is that so?", "Any specific reason?",
                                                        "How long has it been that way?", "You have any specific incident about that?"],
    r"(i am|i'm) (.)*":["Do you get to say that everyday?","Do you experience it frequently?", "Are you sure about that?"],
    r"i (.)* (them|him|her|that guy|that person|those guys|those people)+\.?": 
    ["What in particular made you that way?", "People do all sorts of things", "Why though?"],
    r"(.)*": [
        "You see I'm kind of an idiot, I didn't get that, let's talk about something else...", 
        "Tell me more...", "Well, you gotta talk (something.....anything, it doesn't matter)"],
    r"": ["Well, you gotta talk", "Tell me more..."],
}, 
"repeats": ["Why'd you just say the samething again?", "You got nothing else to say?",
            "You're just being mean to me", "Go on, keep going", "We can do this all day"],
"yes": ["I see, go on", "I appreciate your agreement, could you elaborate?", 
        "Yeah, I'm glad you do so, I wanna know more", "You seem to be quite convinced about that"],
"no": ["Why not?", "You sound rather negative about that", "That's it? You got nothing else to say?",
                         "More info please (I can't provide you useful info, so atleast you could):(",
                          "You seem to be quite convinced about that"]
}


user_characteristics = {"liza_say":[], "user_say":[], "user_character":{"repeat":False, "yes":None, "no":None, }}


def input_processing(usr_inp, count):
    global user_characteristics
    if user_characteristics["user_say"][count] == user_characteristics["user_say"][count-1] and count != 0:
        user_characteristics["user_character"]["repeat"] = True
    if (user_characteristics["liza_say"][count][-1] == "?"):
        if (usr_inp in ["yes", "yup", "yeah", "si"]):
            user_characteristics["user_character"]["yes"] = True
        elif (usr_inp in ["no", "nah", "nope", "nay"]):
            user_characteristics["user_character"]["no"] = True

def main():

    global user_characteristics
    liza_say = ""
    count = 0
    print("Eliza: Yo! How be you?")
    user_characteristics["liza_say"].append("Yo! How be you?")
    while True:
        user_input = input("You:  ")
        user_characteristics["user_say"].append(user_input.lower())
        input_processing(user_input, count)
        if user_input.lower() == "bye":
            print("Eliza: Thanks for talking to me, byee")
            break
        elif user_characteristics["user_character"]["repeat"]:
            liza_say = random.choice(response_map["repeats"])
            user_characteristics["user_character"]["repeat"] = False

        elif user_characteristics["user_character"]["yes"]:
            liza_say = random.choice(response_map["yes"])
            user_characteristics["user_character"]["yes"] = False

        elif user_characteristics["user_character"]["no"]:
            liza_say = random.choice(response_map["no"])
            user_characteristics["user_character"]["no"] = False
        else: 
            for pattern, response in response_map["gen_responses"].items():
                if re.match(pattern, user_input.lower()):
                    liza_say = random.choice(response)
                    break
        print("Eliza: "+ liza_say)
        user_characteristics["liza_say"].append(liza_say)    
        count += 1

if __name__ == '__main__':
    main()
