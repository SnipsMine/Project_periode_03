from flask import Flask, request, render_template, make_response
from lib.class_p3 import GffReader as Reader
from lib.make_output_files import make_output_line_freq, make_output_gem_length, make_output_exon_intron

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"gff", "py"}

app = Flask(__name__)
SECRET_KEY = "jhdsfkdjsha"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def home():
    kwargs = {
        "title": "Home",
        "home": "active",
    }

    rendered_page = render_template('index.html', **kwargs)
    return rendered_page


@app.route("/gff_reader", methods=['POST', 'GET'])
def gff_reader():
    if request.method == 'GET':
        kwargs = {
            "title": "GFF Reader",
            "gff_reader": "active",
        }

        rendered_page = render_template("gff_reader_get.html", **kwargs)

        return rendered_page

    elif request.method == "POST":
        try:
            file = request.files["file"]
            file_data = file.read().decode("UTF-8")

        except FileNotFoundError:
            print("No file found")
            kwargs = {
                "title": "GFF Reader",
                "gff_reader": "active",
            }

            return render_template("gff_reader_get.html", **kwargs)
        if file != "" and file.filename.split(".")[1] in ALLOWED_EXTENSIONS:

            gff_import = Reader(file_data)

            # Get options length freq graph
            accuratie_length_freq = request.form["step"]
            max_length_length_freq = request.form["max_length"]
            min_length_length_freq = request.form["min_length"]
            show_graph_length_freq = "show_graph_length_freq" in request.form


            # Get options gem. length
            show_graph_gem_length = "show_graph_gem_length" in request.form

            # Get options exon & intron division
            show_graph_intron_exon = "show_graph_intron_exon" in request.form

            freq_line, freq_line_data = gff_import.create_freq_line_graph(accuratie_length_freq, min_length_length_freq, max_length_length_freq)
            gem_lenght, gem_length_data = gff_import.create_gem_length_barplot()
            length_perc, length_perc_data = gff_import.create_length_perc_barplot()

            make_output_line_freq(freq_line_data)
            make_output_gem_length(gem_length_data)
            make_output_exon_intron(length_perc_data)

            kwargs = {
                "title": "GFF Reader",
                "gff_reader": "active",

                "graph1": freq_line,
                "graph2": gem_lenght,
                "graph3": length_perc,

                "length_freq_data": freq_line_data,
                "gem_length_data": gem_length_data,
                "prec_intron_exon_data": length_perc_data,

                "show_graph_length_freq": show_graph_length_freq,
                "show_graph_gem_length": show_graph_gem_length,
                "show_graph_intron_exon": show_graph_intron_exon,
            }

            rendered_page = make_response(
                render_template("gff_reader_post.html", **kwargs))
            rendered_page.set_cookie('sessionID', '', expires=0)

        else:
            kwargs = {
                "title": "GFF Reader",
                "gff_reader": "active",
            }

            rendered_page = render_template("gff_reader_get.html", **kwargs)
        return rendered_page


@app.route("/info_gff_file_format")
def gff_info():
    kwargs = {
        "title": "GFF info",
        "gff_info": "active",
    }

    rendered_page = render_template("info_gff_file_format.html", **kwargs)
    return rendered_page


@app.route("/contact")
def contact():
    kwargs = {
        "title": "contact",
        "contact": "active",
    }

    rendered_page = render_template("contact.html", **kwargs)
    return rendered_page
