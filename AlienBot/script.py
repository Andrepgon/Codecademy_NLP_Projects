# importing regex and random libraries
import re
import random

class AlienBot:
    # potential negative responses
    negative_responses = ("no", "nope", "nah", "naw", "not a chance", "sorry", "never", "die", "get off", "disappear", "not")
    # keywords for exiting the conversation
    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later", "leaving", "seeya", "leave")
    # random starter questions
    random_questions = (
        "Why are you here? \n",
        "Are there many humans like you? \n",
        "What do you consume for sustenance? \n",
        "Is there intelligent life on this planet? \n",
        "Does Earth have a leader? \n",
        "What planets have you visited? \n",
        "What technology do you have on this planet? \n",
        "How many humans exist?\n",
        "How long has your species been on this planet?\n",
        "Have you ever entered the sun? \n"
    )

    def __init__(self):
        self.alienbabble = {
            'describe_planet_intent': r'.*\byour planet\b.*',
            'answer_why_intent': r'.*\bwhy are.*',
            'cubed_intent': r'.*\bcube.*?(\d+).*',
            'simple_yes_intent': r'^\s*(yes|sure|of course|yep|yeah)\s*\.?!?$'
        }

    def greet(self):
        self.name = input("Greetings. How should I call you? \n")
        will_help = input(f"Hello {self.name}, I'm Bilu. I'm not from this planet. Will you help me learn about your planet? \n")
        for word in will_help.lower().split():
            if word in self.negative_responses:
                print("I see. We are coming to check for ourselves. \n")
                return
        self.chat()

    def make_exit(self, reply):
        for word in reply.lower().split():
            if word in self.exit_commands:
                print("You said enough, this conversation was very useful.\n")
                return True
        return False

    def chat(self):
        reply = input(random.choice(self.random_questions)).lower()
        while not self.make_exit(reply):
            response = self.match_reply(reply)
            print(response)
            reply = input(random.choice(self.random_questions)).lower()

    def match_reply(self, reply):
        for intent, regex_pattern in self.alienbabble.items():
            found_match = re.match(regex_pattern, reply)
            if found_match:
                if intent == "describe_planet_intent":
                    return self.describe_planet_intent()
                elif intent == "answer_why_intent":
                    return self.answer_why_intent()
                elif intent == "cubed_intent":
                    return self.cubed_intent(found_match.groups()[0])
                elif intent == "simple_yes_intent":
                    return self.simple_yes_intent()
        return self.no_match_intent()

    def describe_planet_intent(self):
        responses = (
            "It's a place where the ground whispers your name before it decides if you may walk or bleed.",
            "The air tastes like iron and sorrow, and the trees remember every scream they've ever heard."
        )
        return random.choice(responses)

    def answer_why_intent(self):
        responses = (
            "We heard the Earth hum and followed the sound through the void.",
            "Your planet called to us in a voice only broken minds can hear.",
            "We came to taste your skies and count the cracks in your minds.",
            "Curiosity... and the hunger that always follows it.",
            "Because extinction is a story we like to hear told up close.",
            "Your dreams leaked into our realm — and now we can't forget the flavor."
        )
        return random.choice(responses)

    def cubed_intent(self, number):
        number = int(number)
        return f"The cube of {number} is {number**3}. You are an unevolved species."

    def simple_yes_intent(self):
        responses = (
            "Excellent. You will remember this moment when your sky turns black.",
            "Good. We need more compliant specimens.",
            "Your cooperation is noted. It will be your only mercy.",
            "Obedience is the first sign of enlightenment."
        )
        return random.choice(responses)

    def no_match_intent(self):
        responses = (
            "I do not understand your primitive language yet. Clarify or perish.",
            "Your words make little sense to us. Try again, flesh unit.",
            "Such noises are not recognized. Try to be more coherent.",
            "We are not amused. Say something of value or be discarded."
        )
        return random.choice(responses)

# Create an instance of AlienBot below:
conv = AlienBot()
conv.greet()
