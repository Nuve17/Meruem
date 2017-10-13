import jinja2
from flask import Flask, jsonify, make_response

from pdf_getter import main


app = Flask(__name__)


@app.route('/planning', methods=['GET'])
def get_planning():
    pdf_filename = main()
    if pdf_filename:
        binary_pdf = open("./planning.pdf", "rb")
        binary_pdf = binary_pdf.read()
        response = make_response(binary_pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=planning.pdf'
        return response
    else:
        jsonify("Error: There is an error, please contact the admin")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)