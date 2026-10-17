# Name: Ivan Chan
# Roster: XKCD
# This is an optional assignment.

from flask import Flask, render_template, request
import random
import os
app = Flask(__name__)

def generateLorem(w, cw):
	nums = list(range(1, 16))
	weights = [41, 55, 68, 79, 87, 90, 87, 79, 68, 55, 41, 29, 19, 12, 7]
	senLength = random.choices(nums, weights=weights, k=1)[0]
    
	sentence_words = []
	last_word = None
	hasComma = False
    
	for _ in range(senLength):
		if (random.random() < 0.15):
			word = random.choice(cw)
		else:
			word = random.choice(w)

		while word == last_word:
			word = random.choice(w)

		if (random.random() < 0.0616) and not hasComma:
			word += ","
			hasComma = True
		else:
			hasComma = False

		sentence_words.append(word)
		last_word = word
    
	sen = "Lorem ipsum dolor sit amet, " + " ".join(sentence_words)

	if (random.random() < 0.08):
		sen += "?"
	elif (random.random() < 0.04):
		sen += "!"
	else:
		sen += "."
	
	sen = sen[:-2] + "?" if sen.endswith(',?') else sen
	sen = sen[:-2] + "!" if sen.endswith(',!') else sen
	sen = sen[:-2] + "." if sen.endswith(',.') else sen
	return sen

def generateSentence(w, cw):
	nums = list(range(2, 21))
	weights = [29, 41, 55, 68, 79, 87, 90, 87, 79, 68, 55, 41, 29, 19, 12, 7, 4, 2, 1]
	senLength = random.choices(nums, weights=weights, k=1)[0]

	sentence_words = []
	last_word = None
	hasComma = False

	for _ in range(senLength):
		if (random.random() < 0.15):
			word = random.choice(cw)
		else:
			word = random.choice(w)

		while word == last_word:
			word = random.choice(w)
			
		if (random.random() < 0.0616) and not hasComma:
			word += ","
			hasComma = True
		else:
			hasComma = False

		sentence_words.append(word)
		last_word = word

	sen = " ".join(sentence_words).capitalize()

	if (random.random() < 0.08):
		sen += "?"
	elif (random.random() < 0.04):
		sen += "!"
	else:
		sen += "."
	
	sen = sen[:-2] + "?" if sen.endswith(',?') else sen
	sen = sen[:-2] + "!" if sen.endswith(',!') else sen
	sen = sen[:-2] + "." if sen.endswith(',.') else sen
	return sen
	
def generateNSentence(w, cw, num):
	sentence_words = []
	last_word = None
	hasComma = False

	for _ in range(num):
		if (random.random() < 0.15):
			word = random.choice(cw)
		else:
			word = random.choice(w)

		while word == last_word:
			word = random.choice(w)
			
		if (random.random() < 0.0616) and not hasComma:
			word += ","
			hasComma = True
		else:
			hasComma = False

		sentence_words.append(word)
		last_word = word

	sen = " ".join(sentence_words).capitalize() + "."
	sen = sen[:-2] + "." if sen.endswith(',.') else sen
	return sen
    
@app.route("/", methods=['GET'])
def main():
    return render_template('main.html')

@app.route("/result", methods=['POST'])
def result():
	unit = request.values.get('unit')
	amount = int(request.values.get('amount'))
	text = ""
	words = []
	commonwords = ["an", "sed", "et", "atque", "ac", "aut", "vel", "si", "quia", "quod", "dum", "in", "ad", "ab", "a", "ex", "e", "cum", "sine", "per", "pro", "ego", "tu", "nos", "vos", "is", "hic", "haec", "ea", "qui", "quae", "sum", "esse", "etiam", "non", "tamen", "quoque", "saepe", "suus", "sua"]
	
	with open('text/words.txt', 'r') as file:
		words = file.read().splitlines()
	
	print(unit, amount)
	# Rules: 1. Capitalize the first letter of each sentence.
		# 2. Do not place two of the same words next to one another.
		# 3. Sentences ideally should be from 4 to 15 words, though make it possible for 1 to 20 word sentences to be possible.
		# 4. Commas should sometimes, but not often appear in a sentence. They must not appear in the first or before the last word.
	text = "Sorry, something went wrong. Please try again later."
	if unit == "paragraph":
		text = ""
		for i in range(amount):
			rand = random.randint(4, 9)
			for j in range(rand):
				if j == 0:
					text += "	"
					if i == 0:
						text += generateLorem(words, commonwords) + " "
					else:
						text += generateSentence(words, commonwords) + " "
				else:
					text += generateSentence(words, commonwords) + " "
			text += "\n"
			
	elif unit == "sentence":
		text = "	"
		for i in range(amount):
			if i == 0: 
				text += generateLorem(words, commonwords) + " "
			else:
				text += generateSentence(words, commonwords) + " "
	elif unit == "word":
		if amount == 1: 
			text = "	Lorem."
		elif amount == 2: 
			text = "	Lorem ipsum."
		elif amount == 3: 
			text = "	Lorem ipsum dolor."
		elif amount == 4: 
			text = "	Lorem ipsum dolor sit."
		elif amount == 5: 
			text = "	Lorem ipsum dolor sit amet."
		else:
			text = "	Lorem ipsum dolor sit amet."
			remaining = amount - 5
			while remaining > 0:
				if remaining > 15:
					nums = list(range(1, 16))
					weights = [41, 55, 68, 79, 87, 90, 87, 79, 68, 55, 41, 29, 19, 12, 7]
					senLength = random.choices(nums, weights=weights, k=1)[0]
				else:
					senLength = remaining
				
				text += " " + generateNSentence(words, commonwords, senLength)
				remaining -= senLength
		
	else:
		text = "Sorry, something went wrong. Please try again later."
	
	return render_template('result.html', text=text, unit=unit, amount=amount)

if __name__ == "__main__": # I used Artificial Intelligence (AI) to host a website,  but only for this part.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
