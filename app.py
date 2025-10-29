from flask import Flask, render_template, request
import os


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/myworks')
def myworks():
    return render_template('myworks.html')

@app.route('/works', methods=['GET', 'POST'])
def works():
    result = None
    if request.method == 'POST':
        input_string = request.form.get('inputString', '')
        result = input_string.upper()
    return render_template('touppercase.html', result=result)

@app.route('/circle', methods=['GET', 'POST'])
def circle():
    result = None
    if request.method == "POST":
        try:
            radius = float(request.form.get("radius", 0))
            result = 3.14159 * radius * radius
        except ValueError:
            result = "Invalid input"
    return render_template("circle.html", result=result)

@app.route('/triangle', methods=['GET', 'POST'])
def triangle():
    result = None
    if request.method == "POST":
        try:
            base = float(request.form.get("base", 0))
            height = float(request.form.get("height", 0))
            result = 0.5 * base * height
        except ValueError:
            result = "Invalid input"
    return render_template("triangle.html", result=result)

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route("/library")
def library():
    import os
    library_path = os.path.join(app.root_path, "library")
    notebooks = [f for f in os.listdir(library_path) if f.endswith(".ipynb")]
    return render_template("library.html", notebooks=notebooks)

@app.route("/view/<path:filename>")
def view_notebook(filename):
    from flask import send_from_directory
    library_path = os.path.join(app.root_path, "library")
    return send_from_directory(library_path, filename)


@app.route('/converter', methods=['GET', 'POST'])
def converter():
    postfix = None
    if request.method == "POST":
        infix_expr = request.form.get("infix", "")

        tokens = []
        current = ''
        for char in infix_expr:
            if char.isalnum():
                current += char
            else:
                if current:
                    tokens.append(current)
                    current = ''
                if char.strip():
                    tokens.append(char)
        if current:
            tokens.append(current)

        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        stack = []
        output = []

        for token in tokens:
            if token.isalnum():
                output.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack:
                    stack.pop()  
            else:  
                while (stack and stack[-1] != '(' and
                       precedence.get(token, 0) <= precedence.get(stack[-1], 0)):
                    output.append(stack.pop())
                stack.append(token)

        while stack:
            output.append(stack.pop())

        postfix = ' '.join(output)

    return render_template("converter.html", postfix=postfix)

if __name__ == "__main__":
    app.run(debug=True)
