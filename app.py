from flask import Flask, render_template, request

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

app.config['DEBUG'] = True

@app.route('/')
def input():
    rows = ['Row 1', 'Row 2', 'Row 3']
    return render_template('input.html', rows=rows)

@app.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        rows = input_text.splitlines()
    else:
        rows = ['Row 1', 'Row 2', 'Row 3']
    return render_template('table.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
