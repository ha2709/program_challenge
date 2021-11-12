import random
import string
import os
import re
from flask import Flask, jsonify
from flask import send_file
from flask_cors import CORS

file_name = 'output.txt'
app = Flask(__name__)
CORS(app)

@app.route('/generate')
def generate():
    """
    generate file contain random 4 objects:
    alphabetical strings, real numbers, integers, alphanumerics
    return url is the file name for download
    """

    max_size = 2097152
    open(file_name, 'w')
    file_size = os.stat(file_name).st_size

    def random_alphanumerics(length):
        key = ''
        for i in range(length):
            key += random.choice(string.digits + string.ascii_lowercase)
        return key

    with open(file_name, 'a') as my_file:
        while file_size < max_size:
            length_numeric = random.randint(15, 17)
            length_alpha = random.randint(11, 15)
            length_real = random.randint(1, 5)
            my_alphabets = ''.join(random.choice(string.ascii_lowercase)\
                 for x in range(length_alpha))
            my_int = random.randint(0, 100000000000)
            my_real = round(random.uniform(0.0, 10000.0), length_real)
            my_alphanumerics = random_alphanumerics(length_numeric)
            my_file.write(my_alphabets + ', {}'.format(my_int) + \
                ', {}'.format(my_real) + ', ' + my_alphanumerics + ', ')
            file_size = os.stat(file_name).st_size

            if file_size == max_size:
                break
        print('Done')
        my_file.close()

        return jsonify({
            "url": str(file_name)
        })

@app.route('/download')
def download():
    """
    download file generated from random.
    """

    return send_file(file_name, as_attachment=True)

@app.route('/report')
def report():
    """
    Do calculation each of objects, then return the count value for each objects
    """

    list_obj = []
    with open(file_name, "r") as file_stream:
        for line in file_stream:
            list_obj = line.split(",")

    count_int = 0
    count_real = 0
    count_alpha_numeric = 0
    count_alphabet = 0
    for  word in list_obj:
        word = word.strip()
        if re.fullmatch(re.compile(r'^[0-9]+$'), word):
            count_int += 1
        else:
            try:
                if word.index("."):
                    count_real += 1
            except:
                if re.match(r"(?=.*[a-zA-Z])(?=.*[0-9])^[\w\d ]+$", word):
                    count_alpha_numeric += 1
                else:
                    count_alphabet += 1

    data = {
        "Alphabet":count_alphabet,
        "real": count_real,
        "integer": count_int,
        "alphanumeric":count_alpha_numeric,
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
