#!/usr/bin/env python3

"""
This program creates a flask app that functions as the controller for the web page
"""

__author__ = "Micha Beens"
__version__ = "1.0.0"

from flask import Flask, request, render_template, make_response
from lib.gff_reader import GffReader as Reader
from lib.make_output_files import make_output_line_freq, make_output_gem_length, make_output_exon_intron

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"gff"}

app = Flask(__name__)
SECRET_KEY = "jhdsfkdjsha"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def home():
    """The code that is called with the url route /"""
    # Set the jinja kwargs
    kwargs = {
        "title": "Home",
        "home": "active",
    }

    # returns/shows the html page index.html with the jinja kwargs
    rendered_page = render_template('index.html', **kwargs)
    return rendered_page


@app.route("/gff_reader", methods=['POST', 'GET'])
def gff_reader():
    """The code that is called with the url route /gff_reader"""
    if request.method == 'GET':
        # Set the jinja kwargs
        kwargs = {
            "title": "GFF Reader",
            "gff_reader": "active",
        }

        # Returns/shows the html page gff_reader_get.html with the jinja kwargs
        rendered_page = render_template("gff_reader_get.html", **kwargs)
        return rendered_page

    elif request.method == "POST":
        # Get the file that was given
        file = request.files["file"]
        file_data = file.read().decode("UTF-8")

        # Check if there was a file given.
        if not file_data:
            # If no file is given return the error page with the corresponding error
            error = "Er was geen document gevonden. Zorg ervoor dat er een document is mee gegeven"

            # Set the jinja kwargs
            kwargs = {
                "title": "GFF Reader",
                "gff_reader": "active",
                "error": error,
            }
            return render_template("gff_reader_error.html", **kwargs)

        elif file.filename.split(".")[1] in ALLOWED_EXTENSIONS:
            # if the file has the allowed extension try to create the graphs
            try:
                # Create the class
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

                # Create the graphs
                freq_line, freq_line_data = gff_import.create_freq_line_graph(accuratie_length_freq,
                                                                              min_length_length_freq,
                                                                              max_length_length_freq)

                gem_lenght, gem_length_data = gff_import.create_gem_length_barplot()
                length_perc, length_perc_data = gff_import.create_length_perc_barplot()

                # Make the raw data file's fro the graphs
                make_output_line_freq(freq_line_data)
                make_output_gem_length(gem_length_data)
                make_output_exon_intron(length_perc_data)

                # Set the kwargs for jinja
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

                # return je the html page gff_reader_post.html with the jinja kwargs
                rendered_page = make_response(
                    render_template("gff_reader_post.html", **kwargs))
                rendered_page.set_cookie('sessionID', '', expires=0)
                return rendered_page

            except:
                # if there occurs when creating the graphs return je error page with te corresponding error
                error = "Iets ging mis tijdens lezen tijdens het document. Zorg ervoor dat je het juiste document hebt meegegeven."

                # Set the jinja kwargs
                kwargs = {
                    "title": "GFF Reader",
                    "gff_reader": "active",
                    "error": error,
                }
                return render_template("gff_reader_error.html", **kwargs)

        else:
            # if the file  extension was not allowed return the error page with the corresponding error
            error = "Het document dat is meegegeven was geen gff document"

            # Set the jinja kwargs
            kwargs = {
                "title": "GFF Reader",
                "gff_reader": "active",
                "error": error
            }
            return render_template("gff_reader_error.html", **kwargs)


@app.route("/info_gff_file_format")
def gff_info():
    """The code that is called with the url route /info_gff_file_format"""
    # Set the jinja kwargs
    kwargs = {
        "title": "GFF info",
        "gff_info": "active",
    }

    # Return the html page info_gff_file_format.html with the jinja kwargs
    rendered_page = render_template("info_gff_file_format.html", **kwargs)
    return rendered_page


@app.route("/contact")
def contact():
    """The code that is called with the url route /contact"""
    # Set the jinja kwargs
    kwargs = {
        "title": "contact",
        "contact": "active",
    }

    # Return the html page contact.html with the jinja kwargs
    rendered_page = render_template("contact.html", **kwargs)
    return rendered_page
