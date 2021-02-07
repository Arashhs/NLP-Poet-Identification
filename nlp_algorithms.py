

START_SYMBOL = None
END_SYMBOL = None
WORDS_THRESHOLD = None

L1 = None
L2 = None
L3 = None
E = None

def set_parameters(start_sym, end_sym, threshold, l1_val, l2_val, l3_val, e_val):
    global START_SYMBOL, END_SYMBOL, WORDS_THRESHOLD, L1, L2, L3, E
    START_SYMBOL = start_sym
    END_SYMBOL = end_sym
    WORDS_THRESHOLD = threshold
    L1 = l1_val
    L2 = l2_val
    L3 = l3_val
    E = e_val


# for each poet, we create an object from this class
class Language:
    def __init__(self, file_name):
        self.file_name = file_name
        self.words_dict = self.init_dict(file_name)
        self.unigram_model = None
        self.bigram_model = None

    
    # initializing words dictionary (# each word occurrences) for the given file
    def init_dict(self, file_name):
        my_dict = {}
        with open(file_name, encoding="utf-8", mode="rt") as reader:
            num_lines = 0
            for line in reader:
                num_lines +=1
                words = line.split()
                for word in words:
                    if not word in my_dict:
                        my_dict[word] = 1
                    else:
                        my_dict[word] += 1
        my_dict[START_SYMBOL] = num_lines
        my_dict[END_SYMBOL] = num_lines
        my_dict = {i:my_dict[i] for i in my_dict if my_dict[i] > WORDS_THRESHOLD}
        return my_dict



    # calculating the unigram probabilities for our dictionary
    def build_unigram_model(self):
        words_dict = self.words_dict
        words_dict = {i:words_dict[i] for i in words_dict if i != START_SYMBOL and i != END_SYMBOL}
        sum_count = sum(words_dict.values())
        unigram_model = {i:words_dict[i]/sum_count for i in words_dict}
        self.unigram_model = unigram_model


    # getting the unigram probability for the given word
    def unigram_prob(self, word):
        if word in self.unigram_model:
            return self.unigram_model[word]
        else:
            return 0

    # getting the word count in our dictionary for the given word
    def word_count(self, word):
        if word in self.words_dict:
            return self.words_dict[word]
        else:
            return 0

    # checking if the given word exists in our dictionary
    def word_exists(self, word):
        if word in self.words_dict:
            return True
        else:
            return False


    # calculating the bigram probabilities for our dictionary
    def build_bigram_model(self):
        bigram_model = {}
        with open(self.file_name, encoding="utf-8", mode="rt") as reader:
            for sentence in reader:
                words = sentence.split()
                words = [START_SYMBOL] + words + [END_SYMBOL]
                bigram_tokens = []
                for i in range(len(words)-1):
                    bigram_tokens.append([words[i], words[i+1]])
                for bigram_token in bigram_tokens:
                    if self.word_exists(bigram_token[0]) and self.word_exists(bigram_token[1]):
                        token = bigram_token_str(bigram_token)
                        if not token in bigram_model:
                            bigram_model[token] = 1/self.word_count(bigram_token[0])
                        else:
                            bigram_model[token] += 1/self.word_count(bigram_token[0])
                
                '''for bigram_token in bigram_tokens:
                    token = bigram_token_str(bigram_token)
                    if bigram_token[1] in unigram_model:
                        unigram_prob = unigram_model[bigram_token[1]]
                    else:
                        unigram_prob = 0
                    bigram_model[token] = l3*bigram_model[token] + l2*unigram_prob + l1*E'''
        self.bigram_model = bigram_model

    
    # getting the raw bigram probability
    def raw_bigram_prob(self, word1, word2):
        token = bigram_token_str([word1, word2])
        if token in self.bigram_model:
            return self.bigram_model[token]
        else:
            return 0


    # getting the bigram probability using the back-off model
    def bigram_prob(self, word1, word2):
        bi_prob = self.raw_bigram_prob(word1, word2)
        uni_prob = self.uni_prob(word1)
        prob = L3*bi_prob + L2*uni_prob + L1*E
        return prob



# converting bigram token to string
def bigram_token_str(bigram_token):
    return bigram_token[0] + "-" + bigram_token[1]
