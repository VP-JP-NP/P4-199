import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = "127.0.0.1"
port = 8000
server.bind((ip_address, port))
server.listen()
list_of_clients = []
nicknames = []

questions = [
    "What is the Italian word for PIE? \n a.Mozarella \n b.Pastry \n c.Patty \n d.Pizza",
    "Water boils at 212 Units at which scale? \n a.Fahrenheit \n b.Celsius \n c.Rankine \n d.Kelvin",
    "Who was the character famous in our childhood rhymes associated with a lamb? \n a.Mary \n b.Jack \n c.Johnny \n d.Mukesh",
    "How many bones does an adult human have? \n a.206 \n b.208 \n c.201 \n d.196",
    "What element does not exist? \n a.Xf \n b.Re \n c.Si \n d.Pa"
]
answers = ['d', 'a', 'b', 'a', 'a']
print("Server Has Started!")
def get_random_question_answer(conn):
    random_index = random.randint(0, len(questions) -1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.enode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn, nickname):
    score = 0 
    conn.send("Welcome to this quiz game!!".encode('utf-8'))
    conn.send("You will recieve a question. The answer to that question should be one of a, b, c, d")
    conn.send("Good Luck!!\n\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    while True: 
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better Luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
            else:
                remove(conn)
        except:
            continue
def remove(conn):
    if conn in list_of_clients:
        list_of_clients.remove(conn)
while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print(nickname + "Connected")
    new_thread = Thread(target = clientthread, args= (conn, nickname))
    new_thread.start()


