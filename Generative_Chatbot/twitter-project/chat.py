import numpy as np
import re
from test_model import encoder_model, decoder_model, num_decoder_tokens, num_encoder_tokens, input_features_dict, target_features_dict, reverse_target_features_dict, max_decoder_seq_length, max_encoder_seq_length

class ChatBot:
    negative_responses = ("no", "nope", "nah", "naw", "not a chance", "sorry")

    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later", "stop")

    def start_chat(self):
        answer = input("Hi friend, let´s talk about the weather! \n")
        if answer in self.negative_responses:
            print("Okay buddy, see you later! \n")
            return
        else:
            self.chat(answer)

    def chat(self, reply):
        while not self.make_exit(reply):
            reply = input(self.generate_response(reply))

    def string_to_matrix(self, user_input):
        tokens = re.findall(r"[\w']+|[^\s\w]", user_input)
        user_input_matrix = np.zeros(
            (1, max_encoder_seq_length, num_encoder_tokens),
            dtype='float32')
        for timestep, token in enumerate(tokens):
            if token in input_features_dict:
                user_input_matrix[0, timestep, input_features_dict[token]] = 1.
        return user_input_matrix

    def generate_response(self, user_input):
        # Convert the user's input string into the appropriate input matrix for the encoder model.
        # This matrix will have the shape expected by the encoder: (1, max_encoder_seq_length, num_encoder_tokens)
        input_matrix = self.string_to_matrix(user_input)

        # Use the encoder model to predict the internal state vectors (h and c) from the input sequence.
        # These states will be passed to the decoder to start generating the output sequence.
        states_value = encoder_model.predict(input_matrix)

        # Create an initial target sequence for the decoder with shape (1, 1, num_decoder_tokens)
        # This represents a single timestep input, and it's initialized with the <START> token.
        target_seq = np.zeros((1, 1, num_decoder_tokens))
        target_seq[0, 0, target_features_dict['<START>']] = 1.

        # Initialize an empty string to accumulate the chatbot's response.
        chatbot_response = ''

        # Set a condition to control the decoding loop.
        stop_condition = False

        # Begin the decoding loop: this will generate one token at a time.
        while not stop_condition:
            # Feed the decoder with the previous target token and the latest states from the encoder/decoder.
            # It returns the probabilities for the next token and the updated hidden and cell states.
            output_tokens, hidden_state, cell_state = decoder_model.predict([target_seq] + states_value)

            # Select the token with the highest probability in the current timestep's output.
            sampled_token_index = np.argmax(output_tokens[0, -1, :])
            sampled_token = reverse_target_features_dict[sampled_token_index]  # Convert index back to token

            # Append the generated token to the chatbot's response string.
            chatbot_response += " " + sampled_token

            # Check for end-of-sequence condition:
            # Either the decoder predicts the <END> token or the response grows too long.
            if (sampled_token == '<END>' or len(chatbot_response) > max_decoder_seq_length):
                stop_condition = True

            # Update the target sequence with the token just generated (as one-hot vector).
            # This token will be fed into the decoder at the next timestep.
            target_seq = np.zeros((1, 1, num_decoder_tokens))
            target_seq[0, 0, sampled_token_index] = 1.

            # Update the decoder states to use in the next iteration of the loop.
            states_value = [hidden_state, cell_state]

        # Clean the final chatbot response by removing <START> and <END> tokens, if present.
        chatbot_response = chatbot_response.replace("<END>", "")
        chatbot_response = chatbot_response.replace("<START>", "")

        # Return the chatbot's final decoded string response.
        return chatbot_response

    def make_exit(self, reply):
        for exit_command in self.exit_commands:
            if exit_command in reply:
                print("Ok, have a great day!")
                return True

        return False

weather_chat = ChatBot()
weather_chat.start_chat()