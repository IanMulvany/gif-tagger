from finances import app, render_template, request, redirect, url_for, session, jsonify, escape
import os
import json
import glob
from uuid import uuid4


@app.route('/')
def index():
    return render_template("index.html")

def parse_qif(file):
    contents = file.read()
    print(contents)

@app.route("/upload", methods=["POST"])
def upload():
    """Handle the upload of qif files, else ignore the file."""
    form = request.form

    # Create a unique "session ID" for this particular batch of uploads.
    upload_key = str(uuid4())

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.
    target = "finances/static/uploads/{}".format(upload_key)
    try:
        os.mkdir(target)
    except:
        if is_ajax:
            return ajax_response(False, "Couldn't create upload directory: {}".format(target))
        else:
            return "Couldn't create upload directory: {}".format(target)

    print("=== Form Data ===")
    for key, value in form.items():
        print(key, "=>", value)

    for upload in request.files.getlist("file"):
        print("about to print upload")
        print(upload)
        filename = upload.filename.rsplit("/")[0]
        print(filename)
        extension = filename.split(".")[1].lower()
        print(extension)
        if extension == "qif":
            destination = "/".join([target, filename])
            file_contents = upload.stream.read().decode("utf-8")
            # print(file_contents)
            upload.save(destination)
            session['display_value'] = file_contents
            return redirect(url_for("show_qif"))

    if is_ajax:
        return redirect(url_for("show_qif"))
        # return ajax_response(True, upload_key)
    else:
        return redirect(url_for("show_qif"))

@app.route("/qif_by_date", methods=['GET'])
def qif_by_date():
    return(jsonify("date ordered"))

@app.route("/qif_by_payee", methods=['GET'])
def qif_by_payee():
    return(jsonify("payee ordered"))

@app.route("/qif_by_value", methods=['GET'])
def qif_by_value():
    return(jsonify("value ordered"))

@app.route("/test_entries", methods=['GET'])
def test_entries():
    row_one = ["a", "b", "c"]
    row_two = ["1", "2", "3"]
    row_three = ["x", "y", "z"]
    return render_template('entries.html', row=row_one)

@app.route("/show_qif", methods=['GET'])
def show_qif():
    print("in show qif")
    split_transactions = []
    contents = session['display_value']
    transactions = contents.split("^")
    for x in transactions:
        print(x)
        print("next: ")
        try:
            transaction = x.split("\n")
            print(transaction)
            transactions.append(transactions)
        except:
            continue 
    return render_template('entries.html', transactions=transactions)

@app.route("/one", methods=['GET'])
def one():
    session['variable'] = "I'm shared"
    message = "this is page one"
    return(message)

@app.route("/two", methods=['GET'])
def two():

    if 'variable' in session:
        message = "this is page two " +  session['variable'] + session['display_value']
    else:
        message = "this is page two"
    session.pop('display_value', None)
    session.pop('variable', None)
    return(message)

@app.route("/files/<uuid>")
def upload_complete(uuid):
    """The location we send them to at the end of the upload."""

    # Get their files.
    root = "finances/static/uploads/{}".format(uuid)
    if not os.path.isdir(root):
        return "Error: UUID not found!"

    files = []
    for file in glob.glob("{}/*.*".format(root)):
        fname = file.split(os.sep)[-1]
        files.append(fname)

    return render_template("files.html",
        uuid=uuid,
        files=files,
    )


def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))
