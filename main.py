import openai
import os
from random import randint

openai.api_key = os.getenv("OPENAI_API_KEY")

def getText(promptRequest):

    something = openai.Completion.create(
        model="text-davinci-003",
        prompt=promptRequest,
        max_tokens=2048,
        temperature=0.8
    )
    newtext = something['choices'][0]['text']

    return newtext

file = open("flashcards.txt","r")
text = file.read().splitlines()
file.close()

def getLines(start):
    list = []
    while start<len(text):
        list.append(text[start])
        start+=4
    return list

question_list = getLines(0)
answer_list = getLines(1)
record_list = getLines(2)

def getQuestion():
    success_rate_list = []
    attempts_total = []
    for i in range(len(record_list)):
        attempts = list(record_list[i])
        if len(attempts) != 0:
            attempts_total.append(len(attempts))
            yes_count = attempts.count("Y")
            no_count = attempts.count("N")
            success_rate = yes_count/(yes_count+no_count)
            success_rate_list.append(success_rate)
        else:
            return i
    if attempts_total.count(record_attempts) == len(attempts_total):
        if success_rate_list.count(1) == len(success_rate_list):
            return randint(0,len(success_rate_list)-1)
        else:
            cur_list = success_rate_list
    else:
        cur_list = attempts_total
    lowest_score = min(cur_list)
    position = cur_list.index(lowest_score)
    return position

def compareAnswers(q,a,u_i):
    prompt = "Here is a question: '"+q+"' The correct answer to this question is: '"+a+"' A student answered: '"+u_i+"' Is the student's answer equivolent to the other answer? In other words, did the student get the correct answer? Respond with one character, either 'Y' meaning yes, or 'N' meaning no."

    response = getText(prompt).strip()
    return response


record_attempts = 5

while True:

    position = getQuestion()
    question = question_list[position]
    answer = answer_list[position]

    user_input = input(question)
    if user_input == "quit":
        break
    status = compareAnswers(question,answer,user_input)

    if status == 'Y':
        print(status)
    else:
        print(status+", the correct answer was: "+answer)
    
    record = list(record_list[position])

    record.append(status)

    while len(record) > record_attempts:
        record.pop(0)
    record = ''.join(record)

    record_list[position] = record
    text[(position*4)+2] = record

file = open("flashcards.txt","r+")
text = map(lambda x: x + '\n', text)
file.writelines(text)
file.close()
