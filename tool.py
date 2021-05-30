from sys import exit

from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.ext.declarative

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')

Base = sqlalchemy.ext.declarative.declarative_base()


class Flashcard(Base):
    __tablename__ = 'flashcard'
    question = Column(String)
    answer = Column(String)
    stage = Column(Integer)
    ID = Column(Integer, primary_key=True, autoincrement=True)

    def add_flashcards(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        print('1. Add a new flashcard')
        print('2. Exit')
        user_input = input()
        if user_input == '1':
            print('Question:')
            qst = input().strip()
            while qst == '':
                print('Question:')
                qst = input().strip()
            print('Answer:')
            ans = input().strip()
            while ans == '':
                print('Answer:')
                ans = input().strip()
            query_input = Flashcard(question=qst, answer=ans, stage=1)
            session.add(query_input)
            session.commit()
            self.add_flashcards()
        elif user_input == '2':
            print('Bye!')
            exit()
        else:
            print('{} is not an option'.format(user_input))
            self.add_flashcards()

    @staticmethod
    def card_sort(result, session):
        print('press "y" if your answer is correct:')
        print('press "n" if your answer is wrong:')
        u_input = input()
        if u_input == 'y':
            result.stage = result.stage + 1
            session.commit()
            if result.stage >= 4:
                session.delete(result)
                session.commit()
        elif u_input == 'n':
            result.stage = 1
        else:
            print('{} is not an option'.format(u_input))

    def practice_flashcards(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        result_list = session.query(Flashcard).all()
        if not result_list:
            print('There is no flashcard to practice!')
        else:
            for result in result_list:
                print('Question: '+result.question)
                print('press "y" to see the answer:')
                print('press "n" to skip:')
                print('press "u" to update:')
                user_input = input()
                if user_input == 'y':
                    print('Answer: '+result.answer)
                    self.card_sort(result, session)
                elif user_input == 'n':
                    self.card_sort(result, session)
                elif user_input == "u":
                    print('press "d" to delete the flashcard:')
                    print('press "e" to edit the flashcard:')

                    user_input = input()
                    if user_input == "d":
                        session.delete(result)
                        session.commit()
                    elif user_input == "e":
                        print("current question: ", result.question)
                        print("please write a new question:")
                        edit_q = input()
                        if edit_q == "":
                            result.question = result.question
                        else:
                            result.question = edit_q
                        print("current answer: ", result.answer)
                        print("please write a new answer:")
                        edit_a = input()
                        if edit_a == "":
                            result.answer = result.answer
                        else:
                            result.answer = edit_a
                        session.commit()
                    else:
                        print("{} is not an option".format(user_input))
                else:
                    print("{} is not an option".format(user_input))


Base.metadata.create_all(engine)


def main():
    f = Flashcard()
    while True:
        print('1. Add flashcards')
        print('2. Practice flashcards')
        print('3. Exit')
        a = input()
        if a in ['1', '2', '3']:
            if a == '1':
                f.add_flashcards()
            elif a == '2':
                f.practice_flashcards()
            else:
                print('Bye!')
                exit()

        else:
            print('{} is not an option'.format(a))


main()
