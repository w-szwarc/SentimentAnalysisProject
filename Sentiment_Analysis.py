from colorama import Fore, Back, Style
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import itertools
import re
import json
import io
from PyPDF2 import PdfFileReader
from collections.abc import Iterable


negative_from_input = {}
positive_from_input = {}
positive_bank = []
negative_bank = []
stopword_bank = []
user_input_list = []
processed_words = []
result_reference = []
result_label = []



def greeting():
    greet_message = " \n Welcome! This program will enable you to conduct sentiment analysis. \n"
    print(Fore.BLACK)
    print(Back.CYAN + greet_message)
    print(Style.RESET_ALL)
    print('The text for analysis has to be preprocessed - it can\'t contain newline characters. ' + '\n' +
          'If you have an unprocessed file, you can supply a link to an online pdf '
          + '\n' + 'What would You like to do? Enter write/pdf. ')


def get_positive_words():
    positive_git_link = "https://raw.githubusercontent.com/awikado/words_reupload/main/positive-words.txt"
    positive_git = requests.get(positive_git_link).content
    positive_soup = BeautifulSoup(positive_git, 'html.parser')
    for word in positive_soup.prettify().split():
        if word.isalnum():
            positive_bank.append(word)


def get_negative_words():
    negative_git_link = "https://raw.githubusercontent.com/awikado/words_reupload/main/negative-words.txt"
    negative_git = requests.get(negative_git_link).content
    negative_soup = BeautifulSoup(negative_git, 'html.parser')
    for word in negative_soup.prettify().split():
        if word.isalnum():
            negative_bank.append(word)


def get_stopwords():
    stopwords_git_link = "https://gist.githubusercontent.com/sebleier/554280/raw/7e0e4a1ce04c2bb7bd41089c9821dbcf6d0c786c/NLTK's%2520list%2520of%2520english%2520stopwords"
    stopwords_git = requests.get(stopwords_git_link).content
    stopwords_soup = BeautifulSoup(stopwords_git, 'html.parser')
    for word in stopwords_soup.prettify().split():
        if word.isalnum():
            stopword_bank.append(word)


def get_sentiment():
    result = 0
    for word in user_input_list:
        if word.lower() in positive_bank:
            result += 1
        elif word.lower() in negative_bank:
            result -= 1
    result_reference.append(result)
    if result > 0:
        print('\n')
        print(Back.GREEN + f' The sentiment score is: {result}. The sentiment is positive.')
        print(Style.RESET_ALL)
        result_label.append('positive')
    elif result < 0:
        print('\n')
        print(Back.RED + f' The sentiment score is: {result}. The sentiment is negative.')
        print(Style.RESET_ALL)
        result_label.append('negative')
    else:
        print('\n')
        print(Back.LIGHTBLACK_EX + f'The sentiment score is 0. The sentiment is neutral.')
        print(Style.RESET_ALL)
        result_label.append('neutral')


def get_sentiment_stopwords():
    user_input_list.clear()
    processed_words.clear()
    result_reference.clear()
    for word in text:
        processed_words.append(re.sub('[.,\':\"!?()]', '', word))
    result = 0
    for w in processed_words:
        user_input_list.append(w)
    for word in user_input_list:
        if word in stopword_bank:
            user_input_list.remove(word)
    for word in user_input_list:
        if word.lower() in positive_bank:
            result += 1
        elif word.lower() in negative_bank:
            result -= 1
    if result > 0:
        print('\n')
        print(Back.GREEN + f' The sentiment score is: {result}. The sentiment is positive.')
        print(Style.RESET_ALL)
    elif result < 0:
        print('\n')
        print(Back.RED + f' The sentiment score is: {result}. The sentiment is negative.')
        print(Style.RESET_ALL)
    else:
        print('\n')
        print(Back.LIGHTBLACK_EX + f'The sentiment score is 0. The sentiment is neutral.')
        print(Style.RESET_ALL)
    result_reference.append(result)


def add_pos_to_dict():
    for word in user_input_list:
        if word.lower() in positive_bank:
            counter = user_input_list.count(word)
            positive_from_input[word.lower()] = counter


def add_neg_to_dict():
    for word in user_input_list:
        if word.lower() in negative_bank:
            counter = user_input_list.count(word)
            negative_from_input[word.lower()] = counter


def flatten(pdf_stacked_list):
    for item in pdf_stacked_list:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item


def save_stats():
    while True:
        print('Would you like to save the statistical analysis into a file? Please enter yes/no.')
        save_answer_stats = input()
        if save_answer_stats.lower() == 'yes':
            print('Please enter the name of the file you would like to create.')
            save_file_name = input()
            save_file = open(save_file_name, 'w')
            save_file.write(f'Sentiment Score: {result_reference}. \n The sentiment is {result_label}.')
            save_file.close()
            break
        elif save_answer_stats.lower() == 'no':
            break
        else:
            print('I did not understand.')
        continue


def get_graphs():
    sorted_pos_input = dict(sorted(positive_from_input.items(), key=lambda item: item[1], reverse=True))
    sorted_neg_input = dict(sorted(negative_from_input.items(), key=lambda item: item[1], reverse=True))

    if len(text) < 5:
        end = len(user_input_list)
        graph_pos_value = []
        graph_pos_key = []
        graph_neg_value = []
        graph_neg_key = []
        pos_values_range = itertools.islice(sorted_pos_input.items(), 0, end)
        neg_values_range = itertools.islice(sorted_neg_input.items(), 0, end)

        for key, value in pos_values_range:
            graph_pos_key.append(key)
            graph_pos_value.append(value)

        for key, value in neg_values_range:
            graph_neg_key.append(key)
            graph_neg_value.append(value)
    else:
        end = 5
        graph_pos_value = []
        graph_pos_key = []
        graph_neg_value = []
        graph_neg_key = []
        pos_values_range = itertools.islice(sorted_pos_input.items(), 0, end)
        neg_values_range = itertools.islice(sorted_neg_input.items(), 0, end)

        for key, value in pos_values_range:
            graph_pos_key.append(key)
            graph_pos_value.append(value)

        for key, value in neg_values_range:
            graph_neg_key.append(key)
            graph_neg_value.append(value)

    if len(graph_neg_value) >= 1:
        plt.subplot(212)
        plt.barh(graph_neg_key, graph_neg_value)
        plt.tick_params(axis='both', which='major', labelsize=8)
        plt.title('Negative word occurrences', size=10)
        plt.xlim(xmin=0, xmax=graph_neg_value[0] + 2)
        for i, v in enumerate(graph_neg_value):
            plt.text(v, i, str(v), size=8)
    else:
        plt.subplot(212)
        plt.barh(graph_neg_key, graph_neg_value)
        plt.tick_params(axis='both', which='major', labelsize=8)
        plt.title('Negative word occurrences', size=10)
        plt.xlim(xmin=0, xmax=1)

    if len(graph_pos_value) >= 1:
        plt.subplot(211)
        plt.barh(graph_pos_key, graph_pos_value)
        plt.tick_params(axis='both', which='major', labelsize=8)
        plt.title('Positive word occurrences', size=10)
        plt.xlim(xmin=0, xmax=graph_pos_value[0]+2)
        for i, v in enumerate(graph_pos_value):
            plt.text(v, i, str(v), size=8)
    else:
        plt.subplot(221)
        plt.barh(graph_pos_key, graph_pos_value)
        plt.tick_params(axis='both', which='major', labelsize=8)
        plt.title('Positive word occurrences', size=10)
        plt.xlim(xmin=0, xmax=1)
    plt.suptitle(f'The sentiment score is {result_reference}')
    plt.show()
    plt.close()
    while True:
        print('Would you like to save the graph? Please enter yes/no. ')
        save_graph_answer = input()
        if save_graph_answer.lower() == 'yes':
            print('Please enter the name of the file you would like to save the graph to')
            save_graph_name = input()
            if len(graph_neg_value) >= 1:
                plt.subplot(212)
                plt.barh(graph_neg_key, graph_neg_value)
                plt.tick_params(axis='both', which='major', labelsize=8)
                plt.title('Negative word occurrences', size=10)
                plt.xlim(xmin=0, xmax=graph_neg_value[0] + 2)
                for i, v in enumerate(graph_neg_value):
                    plt.text(v, i, str(v), size=8)
            else:
                plt.subplot(212)
                plt.barh(graph_neg_key, graph_neg_value)
                plt.tick_params(axis='both', which='major', labelsize=8)
                plt.title('Negative word occurrences', size=10)
                plt.xlim(xmin=0, xmax=1)

            if len(graph_pos_value) >= 1:
                plt.subplot(211)
                plt.barh(graph_pos_key, graph_pos_value)
                plt.tick_params(axis='both', which='major', labelsize=8)
                plt.title('Positive word occurrences', size=10)
                plt.xlim(xmin=0, xmax=graph_pos_value[0] + 2)
                for i, v in enumerate(graph_pos_value):
                    plt.text(v, i, str(v), size=8)
            else:
                plt.subplot(221)
                plt.barh(graph_pos_key, graph_pos_value)
                plt.tick_params(axis='both', which='major', labelsize=8)
                plt.title('Positive word occurrences', size=10)
                plt.xlim(xmin=0, xmax=1)
            plt.suptitle(f'The sentiment score is {result_reference}')
            plt.savefig(save_graph_name)
            plt.close()
            break
        elif save_graph_answer.lower() == 'no':
            break
        else:
            print('I did not understand.')
        continue


def get_pie():
    if len(user_input_list)-sum(positive_from_input.values())-sum(negative_from_input.values()) > 0:
        neutral_graph = len(user_input_list) - sum(positive_from_input.values()) - sum(negative_from_input.values())
    else:
        neutral_graph = 0

    graph_slices = [sum(positive_from_input.values()), sum(negative_from_input.values()), neutral_graph]
    slice_labels = ['Positive words', 'Negative words', 'Neutral words']
    colors = ("limegreen", "red", "gray")
    plt.pie(graph_slices, autopct=lambda p: f'{p:.1f}%', shadow=True, colors=colors)
    plt.legend(slice_labels, loc='best')
    plt.show()
    while True:
        print('Would you like to save the pie chart? Please enter yes/no. ')
        save_pie_answer = input()
        if save_pie_answer.lower() == 'yes':
            print('Please enter the name of the file you would like to save the pie chart to')
            save_pie_name = input()
            if len(user_input_list) - sum(positive_from_input.values()) - sum(negative_from_input.values()) > 0:
                neutral_graph = len(user_input_list) - sum(positive_from_input.values()) - sum(negative_from_input.values())
            else:
                neutral_graph = 0

            graph_slices = [sum(positive_from_input.values()), sum(negative_from_input.values()), neutral_graph]
            slice_labels = ['Positive words', 'Negative words', 'Neutral words']
            colors = ("limegreen", "red", "gray")
            plt.pie(graph_slices, autopct=lambda p: f'{p:.1f}%', shadow=True, colors=colors)
            plt.legend(slice_labels, loc='best')
            plt.savefig(save_pie_name)
            break
        elif save_pie_answer == 'no':
            break
        else:
            print('I did not understand.')
        continue


get_negative_words()
get_positive_words()
greeting()

while True:
    text_format_answer = input()
    if text_format_answer.lower() == 'write':
        text = input('\n Please, enter the text for analysis. The text can\'t contain newline characters. ').split()

        for word in text:
            processed_words.append(re.sub('[.,\':\"!?()]', '', word))
        for w in processed_words:
            user_input_list.append(w)
        break
    elif text_format_answer.lower() == 'pdf':
        while True:
            try:
                pdf_link = input('Please enter the link to the pdf: ')
                break
            except:
                print('The link is invalid.')
                continue
        while True:
            try:
                pdf_pages = int(input('Please enter the number of pages you want to analyze: '))
                break
            except:
                print('This is not a valid number.')
                continue
        pdf_request = requests.get(pdf_link)
        io_file = io.BytesIO(pdf_request.content)
        pdf_reader = PdfFileReader(io_file)
        pdf_stacked_list = []
        for i in range(pdf_pages):
            pdf_stacked_list.append(pdf_reader.getPage(i).extractText().split())
        text = list(flatten(pdf_stacked_list))
        for word in text:
            processed_words.append(re.sub('[.,\':\"!?()]', '', word))
        for w in processed_words:
            user_input_list.append(w)
        break
    else:
        print('I did not understand. Please enter: write/pdf.')
    continue

get_sentiment()

add_neg_to_dict()
add_pos_to_dict()
negative_for_json = [negative_from_input]
positive_for_json = [positive_from_input]
negative_json = json.dumps(negative_for_json)
positive_json = json.dumps(positive_for_json)

save_stats()
get_graphs()
get_pie()

print('Would you like to analyze this text with the exclusion of stopwords?')
while True:
    reanalyze_stopwords_answer = input()
    if reanalyze_stopwords_answer.lower() == 'yes':
        negative_from_input.clear()
        positive_from_input.clear()
        result_reference.clear()
        get_stopwords()
        get_sentiment_stopwords()
        add_pos_to_dict()
        add_neg_to_dict()
        get_graphs()
        get_pie()
        break
    elif reanalyze_stopwords_answer.lower() == 'no':
        break
    else:
        print('I did not understand. Please enter yes/no.')
    continue


while True:
    print("Would you like to conduct the analysis once more ? Please enter yes/no. ")
    reanalyse_answer = input()
    if reanalyse_answer.lower() == 'yes':
        print('Would you like to conduct the analysis with the exclusion of stopwords? Please enter yes/no. ')
        stopwords_answer = input()
        if stopwords_answer.lower() == 'yes':
            negative_from_input.clear()
            positive_from_input.clear()
            result_reference.clear()
            get_stopwords()
            while True:
                print('Would you like to write in a preprocessed text, or use an online pdf ? Please enter write/pdf.')
                text_format_answer = input()
                if text_format_answer.lower() == 'write':
                    print('Please enter text for analysis: ')
                    text = input().split()
                    get_sentiment_stopwords()
                    add_pos_to_dict()
                    add_neg_to_dict()
                    get_graphs()
                    get_pie()
                    break
                elif text_format_answer.lower() == 'pdf':
                    while True:
                        try:
                            pdf_link = input('Please enter the link to the pdf: ')
                            break
                        except:
                            print('The link is invalid.')
                            continue
                    while True:
                        try:
                            pdf_pages = int(input('Please enter the number of pages you want to analyze: '))
                            break
                        except ValueError:
                            print('This is not a valid number.')
                            continue
                    pdf_request = requests.get(pdf_link)
                    io_file = io.BytesIO(pdf_request.content)
                    pdf_reader = PdfFileReader(io_file)
                    pdf_stacked_list = []
                    for i in range(pdf_pages):
                        pdf_stacked_list.append(pdf_reader.getPage(i).extractText().split())
                    text = list(flatten(pdf_stacked_list))
                    get_sentiment_stopwords()
                    add_pos_to_dict()
                    add_neg_to_dict()
                    get_graphs()
                    get_pie()
                    break
                else:
                    print('I did not understand.')
                continue
            continue
        elif stopwords_answer == 'no':
            negative_from_input.clear()
            positive_from_input.clear()
            result_reference.clear()
            user_input_list.clear()
            processed_words.clear()
            while True:
                print('Would you like to write in a preprocessed text or use an online pdf? Please enter write/pdf')
                text_format_answer = input()
                if text_format_answer.lower() == 'write':
                    print('Please enter text for analysis: ')
                    text = input().split()
                    for word in text:
                        processed_words.append(re.sub('[.,\':\"!?()]', '', word))
                    result = 0
                    for w in processed_words:
                        user_input_list.append(w)
                    get_sentiment()
                    add_pos_to_dict()
                    add_neg_to_dict()
                    get_graphs()
                    get_pie()
                    break
                elif text_format_answer.lower() == 'pdf':
                    while True:
                        try:
                            pdf_link = input('Please enter the link to the pdf: ')
                            break
                        except:
                            print('The link is invalid.')
                            continue
                    while True:
                        try:
                            pdf_pages = int(input('Please enter the number of pages you want to analyze: '))
                            break
                        except ValueError:
                            print('This is not a valid number.')
                            continue
                    pdf_request = requests.get(pdf_link)
                    io_file = io.BytesIO(pdf_request.content)
                    pdf_reader = PdfFileReader(io_file)
                    pdf_stacked_list = []
                    for i in range(pdf_pages):
                        pdf_stacked_list.append(pdf_reader.getPage(i).extractText().split())
                    text = list(flatten(pdf_stacked_list))
                    for word in text:
                        processed_words.append(re.sub('[.,\':\"!?()]', '', word))
                    result = 0
                    for w in processed_words:
                        user_input_list.append(w)
                    get_sentiment()
                    add_pos_to_dict()
                    add_neg_to_dict()
                    get_graphs()
                    get_pie()
                    break
                else:
                    print('I did not understand.')
                continue
            continue
        else:
            print('I did not understand you. Please enter yes/no. ')
        continue
    elif reanalyse_answer.lower() == 'no':
        print(Fore.BLACK)
        print(Back.CYAN + 'Bye Bye!')
        break
    else:
        print(f'I did not understand. Please enter yes/no. ')
    continue
