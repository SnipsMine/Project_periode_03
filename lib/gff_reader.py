#!/usr/bin/env python3

"""
This Program will get a GFF file and extracts the data from is to create graphs
"""

__author__ = "Micha Beens"
__version__ = "1.0.0"

from lxml import html
from io import BytesIO
import matplotlib.pyplot as plt
from re import findall
from requests import get
from json import dump, load
from base64 import b64encode


class GffReader(object):
    """
    This class gets a gff file. With the file it can create different graphs
    """

    def __init__(self, gff_file):
        """
        def __init__(self, gff_file)

        Arguments:
        - (string) gff_file: a string with the data of a gff file

        Return:
        - (None): will return a None object

        Usage:
        Will be called when the object is created.

        """
        self.data = self.read_file(gff_file)

    @staticmethod
    def read_file(file):
        """
        def read_file(self, file)

        Arguments:
        -(string) file: a string with the data of a gff file

        Return:
        - (list): the processed file data. This list is 2d nested

        Usage:
        This method will split the file argument based on \n and then wil proceed to split every line based on spaces
        """
        file = file.split("\n")
        data = [line.strip().split() for line in file if not line.startswith("#") and line.strip().split() != []]
        return data

    @staticmethod
    def encode_figure():
        """
        def encode_figure()

        Arguments:
        There are no arguments

        Return:
        - (base64 string): The base64 encoded string of the currend plot

        Usage:
        This method will encode a plot to a base64 string
        """
        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)  # rewind to beginning of file
        website_png = b64encode(figfile.getvalue()).decode('ascii')

        return website_png

    # ---------------------------------------------------------------------------------------------

    def create_freq_line_graph(self, accuratie="", min_length="", max_length=""):
        """
        def crate_freq_line_graph(self, [accuratie, min_length, max_length])

        Arguments:
        - (string) accuratie: This is a optional argument with a default value of 100. This argument affects the step
                              size in the graph
        - (string) min_length: This is a optional argument with a default value of 0. This argument affects the minimal
                               length shown in the graph
        - (string) max_length: This is a optional argument with a default value of the highest feature length. This
                               argument affects the maximal lenth shown in the graph

        Returns:
        - (base64 string): The base64 encoded string of the figure
        - (list): A 2d nested list containing the raw data used in the creation of the graph

        Usage:
        This method will create a length frequency line graph
        """
        # Clear the previous figure data
        plt.clf()

        # Set the figure size and pixel density
        plt.figure(figsize=(8, 6), dpi=100)

        # Get the raw data from the file data
        feature_data = self.isolate_lengths()

        # A list with all the lengths of the features
        min_max_check = [y for x in feature_data for y in feature_data[x]]

        # Check if argument was given or valid
        if min_length == "" or not min_length.isnumeric():
            min_length = 0

        # Check if argument was given or valid
        if max_length == "" or not max_length.isnumeric():
            max_length = max(min_max_check)

        # Check if argument was given or valid
        if accuratie == "" or not accuratie.isnumeric():
            accuratie = 100

        raw_data = []
        # Create the line plots
        for data in feature_data:
            raw_data.append(self.calculate_freq_line_axel_pos(feature_data, data, int(accuratie), int(min_length), int(max_length)))

        # Set the graph variables
        plt.title("Lengte Frequentie (Stap groote: {})".format(accuratie))
        plt.xlabel("lengte")
        plt.ylabel("frequenties")

        plt.legend()

        # Encode the graph
        website_png = self.encode_figure()

        return website_png, raw_data

    def isolate_lengths(self):
        """
        def isolate_lengths(self)

        Arguments:
        There are no arguments

        Return:
        - (dict): The raw data required for the creation of the graph

        Usage:
        This method will filter the total data to the essentials for the creation of the graph
        """

        features = {self.data[index][2] for index in range(len(self.data))}
        data = {feat: [int(self.data[index][4]) - int(self.data[index][3])
                       for index in range(len(self.data))
                       if self.data[index][2] == feat]
                for feat in features}
        return data

    @staticmethod
    def calculate_freq_line_axel_pos(features, data, accuratie, min_length, max_length):
        """
        def calculate_freq_line_axel_pos(features, data, accuratie, min_length, max_length):

        Arguments:
        - (dict) features: Contains the raw data for the graph
        - (string) data: contains the key for the features dict
        - (int) accuratie: contains the value for the step size of the graph
        - (int) min_length: contains the value for the minimal length to be shown on the graph
        - (int) max_length: contains the value for the maximal length to be shown on the graph

        Return:
        - (string) data: name of the feature
        - (list) ten_lengths: the lengths used to create the graph
        - (list) freq: the amount every length is used
        """
        freq = []
        count = 0
        ten_lenghts = [number for number in range(min_length, max_length + accuratie, accuratie)]
        for length in range(min_length, max_length + accuratie):
            count += features[data].count(length)
            if length % accuratie == 0:
                freq.append(count)
                count = 0
        plt.plot(ten_lenghts, freq, label=data)
        return data, ten_lenghts, freq

    # ---------------------------------------------------------------------------------------------

    def create_gem_length_barplot(self):
        """
        def create_gem_length_barplot(self):

        Arguments:
        There are no arguments

        Returns:
        - (base64 string): The base64 encoded string of the figure
        - (list): A 2d nested list containing the raw data used in the creation of the graph

        Usage:
        This method will create a mean length bar graph
        """
        # Clear the previous figure data
        plt.clf()

        # Set the figure size and pixel density
        plt.figure(figsize=(8, 6), dpi=100)

        # Get the raw data from the file data
        feature_data = self.isolate_lengths()

        # Plot the graph for each feature
        raw_data = []
        for data in feature_data:
            raw_data.append(self.calculate_gem_length_axel_pos(feature_data[data], data))

        # Set the graph variables
        plt.title("Gemiddelde lengte features")
        plt.xlabel("feature")
        plt.ylabel("gem. length")

        # Encode the graph
        website_png = self.encode_figure()

        return website_png, raw_data

    @staticmethod
    def calculate_gem_length_axel_pos(data, feature):
        """
        def calculate_gem_length_axel_pos(data, feature):

        Arguments:
        - (dict) data: contains the data to create the graph
        - (string) feature: contains the name of the feature

        Return:
        - (string) feature: The name of the feature
        - (float) gem_length: The mean length of the feature
        """
        gem_length = sum(data) / len(data)
        plt.bar(feature, [gem_length])
        return feature, gem_length

    # ---------------------------------------------------------------------------------------------

    def create_length_perc_barplot(self):
        """
        def create_gem_length_barplot(self):

        Arguments:
        There are no arguments

        Returns:
        - (base64 string): The base64 encoded string of the figure
        - (list): A 2d nested list containing the raw data used in the creation of the graph

        Usage:
        This method will create a intron, exon percentage bar graph
        """
        plt.clf()
        plt.figure(figsize=(12, 8), dpi=100)

        # Get the data required to create the graph
        feature_data = self.isolate_build_data()[::-1]

        # calculate all the values for the graph
        collection = []
        cal_data = []
        for info in feature_data:
            collection.append(info)
            if info[0] == "mRNA":
                cal_data.append(self.calculate_length_perc_bar(collection))
                collection = []

        # Create the graph
        exon = [dat[1] for dat in cal_data]
        intron = [dat[2] for dat in cal_data]
        ids = ["".join(findall(r"^ID=\w+;", dat[0])).strip(";").strip("ID=") for dat in cal_data]
        names = self.website_scrap_names(ids)
        p1 = plt.bar(names, exon, bottom=intron)
        p2 = plt.bar(names, intron)

        # Make the raw data
        raw_data = (names, exon, intron)

        # Set the graph variables
        plt.title("Verdeling van de intronen en exonen per mRNA")
        plt.xlabel("mRNA")
        plt.xticks(rotation=90, fontsize=6)
        plt.ylabel("length%")

        plt.legend((p1[0], p2[0]), ("exon", "intron"))

        # Encode the graph
        website_png = self.encode_figure()

        return website_png, raw_data

    def isolate_build_data(self):
        """
        def isolate_build_data(self)

        Arguemnts:
        There are no arguemnts

        Return:
        - (list): The raw data required for the creation of the graph

        Usage:
        This method will filter the total data to the essentials for the creation of the graph
        """
        data = [[line[2], int(line[3]), int(line[4]), line[8]] for line in self.data]
        return data

    @staticmethod
    def calculate_length_perc_bar(data):
        """
        def calculate_length_perc_bar(data):

        Arguments:
        - (list) data: contains the data to create the graph

        return:
        - (string) name_mrna: The name of the mrna
        - (float) percentage_exon: the percentage that is exon from total
        - (float) percentage_intron: the percentage that is intron from total
        """
        features = {data[index][0] for index in range(len(data))}
        feature_dict = {feat: [feature[2] - feature[1] for feature in data if feature[0] == feat] for feat in features}

        name_mrna = data[-1][-1]

        # Calculate the percentage
        percentages_exon = (sum(feature_dict["exon"]) / sum(feature_dict["mRNA"]) * 100)
        percentages_intron = 100 - percentages_exon

        return name_mrna, percentages_exon, percentages_intron

    @staticmethod
    def website_scrap_names(ids):
        """
        def website_scrap_names(ids):

        Arguments:
        - (list) ids: Contains all the ids of the mRNA's

        Returns:
        - (list) names: Contains all the names of the mRNA's

        Usage:
        This method will go to the website of the data base and will get the name of the mRNA
        """

        # Open the json file with then names
        with open('../lib/static/mRNA_names.json') as json_file:
            data = load(json_file)

        names = []
        for mrna_id in ids:
            # Check if the id is in the json file
            if mrna_id in data.keys():
                names.append(data[mrna_id])
            else:
                # If the id is not in the json file go to the website and get the mrna name
                page = get("http://flybase.org/reports/{}".format(mrna_id))
                tree = html.fromstring(page.content)
                name_mrna = tree.xpath('//div[@class="col-sm-3 col-sm-height"]/text()')
                if not name_mrna == []:
                    names.append(name_mrna[1])
                    data[mrna_id] = name_mrna[1]
                else:
                    names.append(mrna_id)
                    data[mrna_id] = mrna_id

        # Write the updated dict terug naar de json fiel
        with open('../lib/static/mRNA_names.json', 'w') as outfile:
            dump(data, outfile, indent=4)

        return names
