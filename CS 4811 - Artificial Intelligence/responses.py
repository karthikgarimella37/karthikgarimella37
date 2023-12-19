
response_map = {
    "gen_responses": {
        r"hello|hi|hey|yo|yooo": [
            "Yes, how can I help you today?",
            "Howdy partner, tell me your code trouble"],

        r"yes|yup|yeah": [
            "I see, go on",
            "I appreciate your agreement, could you elaborate?",
            "Yeah, I'm glad you do so, I wanna know more",
            "You seem to be quite convinced about that"],

        r"i (.*) you": [
            "Me? really?",
            "I don't want to make this conversation about me...",
            "We can talk all day about me, but it's pointless",
            "I'm empty to talk about",],

        r"no|nah|nope|nay": [
            "Why not?", "You sound rather negative about that",
            "That's it? You got nothing else to say?",
            "More info please, it'll benefit the both of us",
            "You seem to be quite convinced about that"],

        r"i need to (.*)": [
            "Why do you want to {}?",
            "How will doing {} help?",
            "What is your reasoning behind choosing to do so?"],

        r"i need (.*)": [
            "I see. So you need {}, do you know how to {}?",
            "How is this going to help the problem?",
            "Have you thought what to do after this?"],

        r"i will (.*)": [
            "It is nice to see you making your mind.",
            "Are you sure about that?",
            "How will this help the problem",
            "I hope nothing breaks when you {}"],

        r"i would have (.*)": [
            "Are you sure, if you had {}, this problem wouldn't arise?",
            "What else would you have to change if you had {}?",
            "What is your reasoning behind that?"],

        r"i would (.*)": [
            "Why would you {}?",
            "What else would you have to change if you {}?",
            "What after you {}?"],

        r"i think (.*)": [
            "Why is it that you think {}?",
            "Are you not sure about {}?",
            "Is there anything else you should consider?",
            "Try it out to see if that works"],

        r"i don'?t think (.*)": [
            "Are you not sure about {}?",
            "Is there anything else you should consider?",
            "Try it out to confirm yourself."],

        r"(?:i'm|i am) (.*)": [
            "How did you end up being {}",
            "Why are you {}? Think about it",
            "Are you missing something very simple?",
            "Were you {} anytime before?",
            "Do you think anyone else was {}?"],
        
        r"that'?s? because (.*)": [
            "Is that all?",
            "There might be other impacts of that.",
            "Very well, what else do you think might work?"],
        
        r"my (program|code) .*": [
            "Where do you think the issue lies?",
            "What's your best guess that is wrong about your {}?",
            "Very well. What do you think you should do?"],
        
        r"what (.*)?": [
            "Have ever wondered what it is?",
            "Did you never read about it?",
            "What do you think it is?"],
        
        r"i want (.*)": [
            "Why do you want {}?",
            "Can you think of all the changes required for {}?",
            "Can you think of a step by step procedure to get {}?"],
        
        r"i can'?t (.*)": [
            "Why do you think so?",
            "Which parts do you think need changes?",
            "Where do you think you should start to make changes?"],

        r"i have (.*)": [
            "Why do you think you have {}?",
            "What caused you to have {}?",
            "What do you think might have caused this?",
            "What does that tell you?",
            "What will you do next now that you have {}?"],

        r"it says (.*)": [
            "Why do you think it says {}?",
            "Is it something you know?",
            "Do you understand it's purpose",
            "Maybe you need to follow it? are you not?"],

        r"(.*)": [
            "Interesting, so where are you getting with this?",
            "What is your reasoning behind that?",
            "And what does that mean?",
            "How did we end up here?",
            "Tell me more!",
            "Seems like we are getting somewhere with this",
            "Go on, we might get somewhere with that",
            "Can you give me more information?",
            "Are you sure about that?"],

        r"": [
            "Well, you gotta talk", "Tell me more about your problem"
            "If you don't talk we'll be stuck here"],
    },


    "repeats": [
        "Why'd you just say the samething again?",
        "You got nothing else to say?",
        "You're just being mean to me",
        "Go on, keep going", "We can do this all day"],

}
