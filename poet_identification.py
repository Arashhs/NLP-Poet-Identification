import nlp_algorithms as nlp

START_SYMBOL = "$"
END_SYMBOL = "$$"
WORDS_THRESHOLD = 2

TEST_OPTION = "bigram" # must be either unigram or bigram (this is for predicting labels for test data)

L1 = 0.05
L2 = 0.25
L3 = 0.7
E = 0.0001


# predicting the label for one sentence in test data
def predict(poets, sentence, option):
    all_probs = []
    for poet in poets:
        sentence_prob = 1
        if option == "unigram":
            words = sentence.split()
            for word in words:
                prob = poet.unigram_prob(word)
                sentence_prob *= prob
        elif option == "bigram":
            words = sentence.split()
            words = [START_SYMBOL] + words + [END_SYMBOL]
            bigram_tokens = []
            for i in range(len(words)-1):
                prob = poet.bigram_prob(words[i+1], words[i])
                sentence_prob *= prob
        all_probs.append(sentence_prob)
    max_prob = 0
    max_index = 0
    for i in range(len(all_probs)):
        if all_probs[i] > max_prob:
            max_prob = all_probs[i]
            max_index = i
    predicted_label = max_index + 1
    return predicted_label
            
            



# predicting all the labels for every sentence in test data
def predict_labels(poets, file_name, option):
    orig_labels = []
    predicted_labels = []
    with open(file_name, encoding="utf-8", mode="rt") as reader:
            for line in reader:
                orig_label, sentence = line.split("\t")
                orig_label = int(orig_label)
                orig_labels.append(orig_label)
                sentence = sentence.replace("\n", "")
                predicted_label = predict(poets, sentence, option)
                predicted_labels.append(predicted_label)
    return predicted_labels, orig_labels


# calculating the accuracy of the predicted model
def calculate_accuracy(predicted_labels, orig_labels):
    corrects = 0
    all_labels = len(orig_labels)
    for i in range(all_labels):
        if predicted_labels[i] == orig_labels[i]:
            corrects += 1
    accuracy = corrects / all_labels
    return accuracy, corrects



def main():
    nlp.set_parameters(START_SYMBOL, END_SYMBOL, WORDS_THRESHOLD, L1, L2, L3, E)
    # test = nlp.Language("train_set\\test.txt")
    ferdowsi = nlp.Language("train_set\\ferdowsi_train.txt")
    hafez = nlp.Language("train_set\\hafez_train.txt")
    molavi = nlp.Language("train_set\\molavi_train.txt")
    poets = [ferdowsi, hafez, molavi]
    for poet in poets:
        poet.build_unigram_model()
        poet.build_bigram_model()
    predicted_labels, orig_labels = predict_labels(poets, "test_set\\test_file.txt", TEST_OPTION)
    # predicted_labels, orig_labels = predict_labels(poets, "test_set\\test.txt", TEST_OPTION)
    accuracy, corrects = calculate_accuracy(predicted_labels, orig_labels)
    print("\nFinished!\n")
    print("Parameters: λ3: {}, λ2: {}, λ1: {}, ε: {}\n".format(L3, L2, L1, E))
    print("Accuracy of the predicted model: {}\n\nAll predictions: {}\nCorrect predictions: {}\n\n".format(accuracy, len(orig_labels), corrects))




if __name__ == '__main__':
    main()