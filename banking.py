import random
import sqlite3

conn = sqlite3.connect('card.s3db')
c = conn.cursor()

#c.execute('''CREATE TABLE card
 #            (id integer, number text, pin text, balance integer default 0)''')

def Luhn():
    card_number = '400000' + str(random.randint(0,999999999)).zfill(9)
    #print(card_number)
    #card_number = "400000844943340"
    card_list = list(map(int,list(card_number)))
    for i in range(0, len(card_list), 2):
        card_list[i] = card_list[i] * 2
        if card_list[i] > 9:
            card_list[i] = card_list[i] - 9

    Sum = sum(card_list)
    for x in range(10):
        if (Sum + x) % 10 == 0:
            checksum = x
            break
    card_number += str(checksum)
    return card_number
def check_card(card_number):
    card_list = list(map(int,list(card_number[0:-1])))
    for i in range(0, len(card_list), 2):
        card_list[i] = card_list[i] * 2
        if card_list[i] > 9:
            card_list[i] = card_list[i] - 9

    Sum = sum(card_list)
    for x in range(10):
        if (Sum + x) % 10 == 0:
            checksum = x
            break

    if str(checksum) == card_number[-1]:
        return True

counter = 1
exit = 1
while exit:

    print("""1. Create an account
2. Log into account
0. Exit""")
    choice = input()

    if choice == '0':
        print("\nBye!")
        break
    elif choice == '1':
        card_number = Luhn()
        card_pin = str(random.randint(0,9999)).zfill(4)
        c.execute('''insert into card (id, number, pin)values ({}, {}, {})'''.format(counter, card_number, card_pin))
        conn.commit()
        print("\nYour card has been created\nYour card number:\n{}\nYour card PIN:\n{}\n".format(card_number, card_pin))
        counter += 1
    elif choice == '2':
        print("\nEnter your card number:")
        card_number = input()
        print("Enter your PIN:")
        card_pin = input()
        c.execute('''select number, pin from card where number = {}'''.format(card_number))
        record = c.fetchone()
        if not record  or (record[1].zfill(4) != card_pin):
            print("\nWrong card number or PIN!\n")
        else:
            print("\nYou have successfully logged in!\n")
            while True:
                print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")

                choice = input()
                if choice == '0':
                    exit = 0
                    print("\nBye!")
                    break
                elif choice == '1':
                    c.execute('''select balance from card where number = {}'''.format(card_number))
                    balance = c.fetchone()
                    print("\nBalance: {}\n".format(balance[0]))
                elif choice == '2':
                    print("Enter income:")
                    income = eval(input())
                    c.execute('''update card set balance = balance + {}'''.format(income))
                    conn.commit()
                    print('Income was added!')
                elif choice == '3':
                    print("Transfer\nEnter card number:")
                    other_card = input()
                    if other_card != card_number:
                        if check_card(other_card):
                            c.execute('''select number from card where number = {}'''.format(other_card))
                            record = c.fetchone()
                            if record:
                                print("Enter how much money you want to transfer:")
                                money = eval(input())
                                c.execute('''select balance from card where number = {}'''.format(card_number))
                                balance = c.fetchone()
                                if balance[0] < money:
                                    print("Not enough money!")
                                else:
                                    c.execute('''update card set balance = balance - {}'''.format(money))
                                    conn.commit()
                                    print("Success!")
                            else:
                                print("Such a card does not exist.")
                        else:
                            print("Probably you made mistake in the card number. Please try again!")
                    else:
                        print("You can't transfer money to the same account!")
                elif choice == '4':
                    c.execute('''delete from card where number = {}'''.format(card_number))
                    conn.commit()
                    print("The account has been closed!")
                    break
                elif choice == '5':
                    print("\nYou have successfully logged out!\n")
                    break
conn.close()
