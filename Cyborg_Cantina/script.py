from collections import Counter
from responses import responses, blank_spot
from user_functions import preprocess, compare_overlap, pos_tag, extract_nouns, compute_similarity
import spacy
word2vec = spacy.load('en')

exit_commands = ("quit", "goodbye", "exit", "no", "later", "seeya", "bye", "adios", "end")

class ChatBot:
  
  #define .make_exit() below:
  def make_exit(self, user_message):
    for word in exit_commands:
      if word in user_message:
        print("Thank you for talking with me! Goodbye and Bon'apeti")
        return True
    
  #define .chat() below:
  def chat(self):
    user_message = input("Hola my friend! Bienvenido to our mexican restaurant! What would you like to know? \n")
    while not self.make_exit(user_message):
      user_message = self.respond(user_message)
  #define .find_intent_match() below:
  def find_intent_match(self, user_message, responses):
    bow_user_message = Counter(preprocess(user_message))
    preprocessed_responses = [Counter(preprocess(response)) for response in responses]

    similarity_list = [compare_overlap(bow_user_message, bow_response) for bow_response in preprocessed_responses]
    response_index = similarity_list.index(max(similarity_list))
    return responses[response_index]
  #define .find_entities() below:
  def find_entities(self, user_message):
    tagged_user_message = pos_tag(preprocess(user_message))
    message_nouns = extract_nouns(tagged_user_message)

    #executing word2vec
    tokens = word2vec(" ".join(message_nouns))
    category = word2vec(blank_spot)

    word2vec_result = compute_similarity(tokens,category)
    word2vec_result.sort(key=lambda x: x[2])
    
    if len(word2vec_result) < 1:
       return blank_spot
    else:
       return word2vec_result[-1][0]

  #define .respond() below:
  def respond(self, user_message):
    best_response = self.find_intent_match(user_message, responses)
    entity = self.find_entities(user_message)
    print(best_response.format(entity))
    input_message = input("Do you have any other questions? \n")           
    return input_message
cantina_bot = ChatBot()
cantina_bot.chat()


