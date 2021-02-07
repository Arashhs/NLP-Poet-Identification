import nlp_algorithms as nlp

START_SYMBOL = "$"
END_SYMBOL = "$$"
WORDS_THRESHOLD = 0

L1 = 0.6
L2 = 0.3
L3 = 0.1
E = 0.1


def main():
    nlp.set_parameters(START_SYMBOL, END_SYMBOL, WORDS_THRESHOLD, L1, L2, L3, E)
    test = nlp.Language("train_set\\test.txt")
    test.build_unigram_model()
    test.build_bigram_model()
    print(test.unigram_model)



if __name__ == '__main__':
    main()