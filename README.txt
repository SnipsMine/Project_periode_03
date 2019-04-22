Author: Micha Beens
Versie: 1.0.0
Datum: 7-4-2019

--------------------------------------------

Doel:
Inleveren project periode 3

--------------------------------------------

Files:
>lib
    > static
        >images
            - hanze_logo.png
            - logo.png
        >java_script
            - options.js
        > output
            - exon_intron.txt
            - freq_length.txt
            - gem_length.txt
        - mRNA_names.json
        - stylesheet.cxx
    > templates
        - base.html
        - contact.html
        - gff_reader_error.html
        - gff_reader_get.html
        - gff_reader_post.html
        - index.html
        - info_gff_file_format.html
    - app_setup.py
    - gff_reader.py
    - make_output_files.py
    - temp_file_test
> venv
    -run_app

--------------------------------------------

Needed packages:
- flask
- json
- lxml
- io
- matplotlib
- re
- request
- base64

*and all the packages that are required to use these packages

--------------------------------------------

Usage:
To execute this program run the run_app.py file. This will create a server with a link that connects to the website.
The page with the funcionality is gff reader there you can give a gff file to the website.

The pdf files can load slowly this is because the large size of them.
