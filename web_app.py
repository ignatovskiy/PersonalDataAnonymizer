from flask import Flask, render_template, request, send_file, abort
from pdanonymizer import pipelines, images

app = Flask(__name__, template_folder='html')


@app.route('/', methods=['POST'])
def render_anonymized_page():
    input_text = request.form['input_text']
    transformed_text = pipelines.web_handling(input_text.split("\n"))
    return render_template('text_index.html',
                           inputed_text=input_text,
                           transformed_text=transformed_text)


@app.route('/', methods=['GET'])
def render_main_page():
    return render_template('text_index.html',
                           transformed_text="")


@app.route('/docs', methods=['GET'])
def render_file_page():
    return render_template('file_index.html')


@app.route('/docs', methods=['POST'])
def render_uploaded_file():
    uploaded_file = request.files['file']
    uploaded_ext = uploaded_file.filename.split('.')[-1]
    if uploaded_file.filename != '':
        if uploaded_ext in ("txt", "csv"):
            uploaded_file.save(uploaded_file.filename)
            new_file = "new_file." + uploaded_ext
            pipelines.file_handling('models/model_10000', uploaded_file.filename, new_file, "replace")
            return send_file(new_file)
        elif uploaded_ext in ("png", "jpg", "jpeg", "bmp"):
            uploaded_file.save(uploaded_file.filename)
            new_file = images.hide_data_image(uploaded_file.filename)
            return send_file(new_file)
    else:
        abort(404)


def main():
    app.run(host='0.0.0.0',
            port=4444,
            debug=False,
            use_reloader=False)


if __name__ == "__main__":
    main()
