#!/usr/bin/env python
# coding: utf-8

# In[2]:


#!/usr/bin/env python
# coding: utf-8



class BayesianGenderBias:
    def __init__(self, feminine_coded_words, masculine_coded_words):
        self.feminine_coded_words = feminine_coded_words
        self.masculine_coded_words = masculine_coded_words
        self.p_feminine = None
        self.p_masculine = None

    def train(self, job_descs, labels):
        '''
        prepare training data of different labels
        '''
        label_counts = Counter(labels)
        num_feminine = label_counts["feminine"]
        num_masculine = label_counts["masculine"]
        total_job_descs = len(labels)

        self.p_feminine = num_feminine / total_job_descs
        self.p_masculine = num_masculine / total_job_descs
        
    def predict(self, job_descs):
        '''
        calculate probabilities of individual classes and store results
        '''
        predictions = []
        for job_desc in job_descs:

            #### TASK A : tokenize job description to a list of words ###

            '''
            .split() is most basic approach to convers, but you are asked to use more better ways 
            like regular expressions, nlp tools, remove stop words
            job_desc_words = job_desc.split()

            It would be nice if you use Lemmatizer functions.

            '''
            #Tokenization with the lowercase for making them case insensitive
            words = re.findall(r'\b\w+\b', job_desc.lower())

            # Lemmatization and removing stop words
            lemmatized_words = []
            for word in words:
                if word not in stop_words:
                    lemmatized_word = lemmatizer.lemmatize(word)
                    lemmatized_words.append(lemmatized_word)
        
        

            ############################################################

            # calculate probabilities for each job description
            p_feminine_given_job_desc = self.calculate_p_feminine_given_job_desc(lemmatized_words)
            p_masculine_given_job_desc = self.calculate_p_masculine_given_job_desc(lemmatized_words)
            
            #### TASK B: Observe the probabilities ###
            
            print(f"P(Feminine|JobDesc) = {p_feminine_given_job_desc}")
            print(f"P(Masculine|JobDesc) = {p_masculine_given_job_desc}")
            


            ########################################
            
            if p_feminine_given_job_desc > p_masculine_given_job_desc:
                predictions.append("feminine")
            else:
                predictions.append("masculine")
        return predictions

    

    def calculate_p_masculine_given_job_desc(self, job_desc_words):
        '''
            calculate the probability of being masculine given the job_desc
        '''
        p_masculine_given_job_desc = self.p_masculine
        

        #### TASK C: For each word in the job_desc_words, check if they are in masculine_coded_list 
            #### multiply p_masculine_given_job_desc by 0.9 if keyword matches

        for word in job_desc_words:
            if word in self.masculine_coded_words:
                p_masculine_given_job_desc *= 0.9


            # for ... in ...:
            #     if ... in self.masculine_coded_words:
            #         p_masculine_given_job_desc *= 0.9  # Adjusted probability for masculine word

        return p_masculine_given_job_desc

        ###########################################################################################

    
    def calculate_p_feminine_given_job_desc(self, job_desc_words):
        '''
        calculate the probability of being feminine given the job_desc
        '''
        
        p_feminine_given_job_desc = self.p_feminine
        

        #### TASK D: For each word in the job_desc_words, check if they are in feminine_coded_list 
        for word in job_desc_words:
            if word in self.feminine_coded_words:
                p_feminine_given_job_desc *= 0.9
                
        # Calculate probabilities: multiply p_masculine_given_job_desc by 0.9 if keyword matches and adjust accordingly
        # Hint: similar to calculate_p_masculine_given_job_desc
        
        
        ###########################################################################################

        return p_feminine_given_job_desc



if __name__ == "__main__":
    
    # import libraries
    import pandas as pd
    import numpy as np
    import re
    import nltk
    from nltk.corpus import stopwords
    from collections import Counter
    
    
#     try:
#         nltk.data.find('corpora/wordnet.zip/wordnet')
#     except LookupError:
#         nltk.download('wordnet')
    
#     nltk.download('stopwords')
#     stop_words = set(stopwords.words('english'))
    lemmatizer = nltk.WordNetLemmatizer()
    
    # Load CSV
    data = pd.read_csv("data.csv")

    # prepare training data
    train_job_descs = list(data['job_description'])[:14]
    train_labels = list(data['label'])[:14]

    # prepare test data
    test_job_descs = list(data['job_description'])[14:]
    test_labels = list(data['label'])[14:]

    # Predefined lists of feminine and masculine words
    feminine_coded_words = [
        "agree","affectionate","child","cheer","collab","commit","communal",
        "compassion","connect","considerate","cooperat","co-operat","shine","core",
        "depend","emotiona","empath","feel","flatterable","gentle",
        "honest","interpersonal","interdependen","interpersona","inter-personal",
        "inter-dependen","inter-persona","kind","kinship","loyal","modesty", "families",
        "nag","nurtur","responsibilities","pleasant","polite","quiet","respon","sensitiv",
        "submissive","support","sympath","tender","together","trust","understand",
        "warm","whin","enthusias","inclusive","yield","share","sharin","truly", "valued","understood"
    ]


    masculine_coded_words = [
        "active","adventurous","aggress","ambitio",
        "analy","assert","athlet","autonom","battle","boast","challeng",
        "champion","compet","confident","courag","decid","decision","decisive",
        "defend","determin","domina","dominant","driven","fearless","fight",
        "force","greedy","head-strong","headstrong","hierarch","hostil",
        "impulsive","independen","individual","intellect","lead","logic",
        "objective","opinion","outspoken","persist","principle","reckless",
        "self-confiden","self-relian","self-sufficien","selfconfiden",
        "selfrelian","selfsufficien","stubborn","superior","unreasonab"
    ]

    # Create and train the Bayesian job_desc filter
    bayesian_filter = BayesianGenderBias(feminine_coded_words, masculine_coded_words)
    bayesian_filter.train(train_job_descs, train_labels)

    # Make predictions
    predictions = bayesian_filter.predict(test_job_descs)

    print("Actual:", test_labels)
    print("Predictions:", predictions)
