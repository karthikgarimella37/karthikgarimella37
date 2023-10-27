import pandas as pd
import re


sh = pd.read_csv('SMSSpamCollection.txt', sep='\t', header=None, names=['spam/ham', 'SMS'])

sms_num = len(sh)

spam_df = sh.loc[sh['spam/ham'] == 'spam']['SMS']
spam_df.reset_index(inplace=True, drop=True)
ham_df = sh.loc[sh['spam/ham'] == 'ham']['SMS']
ham_df.reset_index(inplace=True, drop=True)
ham_sms = len(ham_df)
spam_sms = len(spam_df)

ham_df = ham_df.apply(lambda x:re.split(r'''([!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ ])''',x))
spam_df = spam_df.apply(lambda x:re.split(r'''([!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ ])''',x))

ham_df=ham_df.apply(lambda l: [w.lower() for w in l if w != ' '])
spam_df=spam_df.apply(lambda l: [w.lower() for w in l if w != ' '])

hamlis = []
sms = 1
def ham_words(l):
    global sms
    for w in l:
        hamlis.append((w,sms))
    sms += 1

ham_df.apply(ham_words)

ham = pd.DataFrame(hamlis, columns=['words','sms'])

spamlis = []
smss = 1
def spam_words(l):
    global smss
    for w in l:
        spamlis.append((w,smss))
    smss += 1

spam_df.apply(spam_words)

spam = pd.DataFrame(spamlis, columns=['words', 'sms'])

prob_spam = spam.groupby('words').count()
prob_ham = ham.groupby('words').count()

prob_spam['p(w|s)'] = prob_spam.apply(lambda x: (x+1)/(spam_sms+2))
prob_ham['p(w|h)'] = prob_ham.apply(lambda x: (x+1)/(ham_sms+2))

prob_ham['normal_p'] =  (prob_ham['p(w|h)'] - min(prob_ham['p(w|h)']))/(max(prob_ham['p(w|h)']) - min(prob_ham['p(w|h)']))

prob_spam['normal_p'] =  (prob_spam['p(w|s)'] - min(prob_spam['p(w|s)']))/(max(prob_spam['p(w|s)']) - min(prob_spam['p(w|s)']))

ham_prob = ham_sms/sms_num
spam_prob = spam_sms/sms_num
#print(ham_prob, spam_prob)

exit_statement = 'exit'

while True:
    str_input = input("Give your Input here: ")
    if str_input == 'exit':
        break
    inp_sms = set(filter(None, re.split(r'''([!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ ])''',str_input)))

    inp_sms.discard(" ")

    new_sms = []
    s_count = 0
    h_count = 0

    for i in inp_sms:
        i = i.lower()
        word_prop = []
    
        if (i not in list(spam['words'])) and (i not in list(ham['words'])):
            word_prop.append(spam_prob)
            word_prop.append(ham_prob)
        else:
            if i not in list(spam['words']):
                word_prop.append(0)
            else:
                word_prop.append(prob_spam.loc[i,'p(w|s)'])
                s_count += 1
            if i not in list(ham['words']):
                word_prop.append(0)
            else:
                word_prop.append(prob_ham.loc[i,'p(w|h)'])
                h_count += 1
    
        new_sms.append(tuple(word_prop))

    new_spam_p = 1
    new_ham_p = 1
    for prop in new_sms:
        if (prop[0] != 0):
            new_spam_p *= prop[0]
        if (prop[1] != 0):
            new_ham_p *= prop[1]

    if s_count == 0:
        new_spam_p = spam_prob
    if h_count == 0:
        new_ham_p = ham_prob
    

    p_inp_sms = (spam_prob * new_spam_p)/((spam_prob * new_spam_p)+(ham_prob*new_ham_p))

    if p_inp_sms >= 0.5:
        print(f" It's SPAM\nspam : 'spam_prob':{p_inp_sms} 'ham_prob':{ 1-p_inp_sms}")
    else:
        print(f"It's HAM\nham : 'spam_prob':{p_inp_sms} 'ham_prob':{ 1-p_inp_sms}")