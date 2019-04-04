#!/usr/bin/env python3

"""
This Program will get a GFF file and extracts the data from is to create graphs
"""

__author__ = "Micha Beens"

# Imports
from lxml import html
from io import BytesIO
import sys
import matplotlib.pyplot as plt
import re
import requests
import json
import base64


# Constants


# Functions
class GffReader(object):
    """
    init with gff_file
    """

    def __init__(self, gff_file):
        self.read_file(gff_file)

    def read_file(self, file):
        file = file.split("\n")
        data = [line.strip().split() for line in file if not line.startswith("#") and line.strip().split() != []]
        self.data = data

    @staticmethod
    def encode_figure():
        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)  # rewind to beginning of file
        website_png = base64.b64encode(figfile.getvalue()).decode('ascii')

        return website_png

    # ---------------------------------------------------------------------------------------------

    def create_freq_line_graph(self, accuratie="", min_length="", max_length=""):
        """
        Needed Data Frequentie and Lenght
        """
        plt.clf()

        plt.figure(figsize=(8, 6), dpi=100)
        feature_data = self.isolate_lengths()

        min_max_check = [y for x in feature_data for y in feature_data[x]]

        if min_length == "" or not min_length.isnumeric():
            min_length = 0

        if max_length == "" or not max_length.isnumeric():
            max_length = max(min_max_check)

        if accuratie == "" or not accuratie.isnumeric():
            accuratie = 100

        raw_data = []
        for data in feature_data:
            raw_data.append(self.calculate_freq_line_axel_pos(feature_data, data, int(accuratie), int(min_length), int(max_length)))

        plt.title("Length Frequentie (Step groote: {})".format(accuratie))
        plt.xlabel("length")
        plt.ylabel("frequenties")

        plt.legend()

        website_png = self.encode_figure()

        return website_png, raw_data

    def isolate_lengths(self):
        """
        Get the lenghts of every feature in the file
        """

        features = {self.data[index][2] for index in range(len(self.data))}
        data = {feat: [int(self.data[index][4]) - int(self.data[index][3])
                       for index in range(len(self.data))
                       if self.data[index][2] == feat]
                for feat in features}
        return data

    @staticmethod
    def calculate_freq_line_axel_pos(features, data, accuratie, min_length, max_length):
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
        Needed data: Gem length and feature
        """
        plt.clf()

        plt.figure(figsize=(8, 6), dpi=100)
        feature_data = self.isolate_lengths()

        raw_data = []
        for data in feature_data:
            raw_data.append(self.calculate_gem_length_axel_pos(feature_data[data], data))

        plt.title("Gemiddelde lengte features")
        plt.xlabel("feature")
        plt.ylabel("gem. length")

        website_png = self.encode_figure()

        return website_png, raw_data

    @staticmethod
    def calculate_gem_length_axel_pos(data, feature):
        """Calculate the average length of the feature"""
        gem_length = sum(data) / len(data)
        plt.bar(feature, [gem_length])
        return feature, gem_length

    # ---------------------------------------------------------------------------------------------

    def create_length_perc_barplot(self):
        """
        Needed data: lenght mRNA, Length Exon and Length Intron
        """
        plt.clf()
        plt.figure(figsize=(12, 8), dpi=100)

        feature_data = self.isolate_length_perc_data()[::-1]

        collection = []
        cal_data = []
        for info in feature_data:
            collection.append(info)
            if info[0] == "mRNA":
                cal_data.append(self.calculate_length_perc_bar(collection))
                collection = []

        exon = [dat[1] for dat in cal_data]
        intron = [dat[2] for dat in cal_data]
        ids = ["".join(re.findall("^ID=\w+;", dat[0])).strip(";").strip("ID=") for dat in cal_data]
        names = self.website_scrap_names(ids)
        p1 = plt.bar(names, exon, bottom=intron)
        p2 = plt.bar(names, intron)

        raw_data = (names, exon, intron)

        plt.title("Verdeling van de intronen en exonen per mRNA")
        plt.xlabel("mRNA")
        plt.xticks(rotation=90, fontsize=6)
        plt.ylabel("length%")

        plt.legend((p1[0], p2[0]), ("exon", "intron"))

        website_png = self.encode_figure()

        return website_png, raw_data

    def isolate_length_perc_data(self):
        """
        -get the start and end of mRNA, Exon and introns.
        """
        data = [[line[2], int(line[3]), int(line[4]), line[8]] for line in self.data]
        return data

    @staticmethod
    def calculate_length_perc_bar(data):
        """
        -groep al the lengths of the exons and introns that fit in the mRNA in a groep
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
        with open('../lib/static/mRNA_names.json') as json_file:
            data = json.load(json_file)

        names = []
        for mrna_id in ids:
            if mrna_id in data.keys():
                names.append(data[mrna_id])
            else:
                page = requests.get("http://flybase.org/reports/{}".format(mrna_id))
                tree = html.fromstring(page.content)
                name_mrna = tree.xpath('//div[@class="col-sm-3 col-sm-height"]/text()')
                if not name_mrna == []:
                    names.append(name_mrna[1])
                    data[mrna_id] = name_mrna[1]
                else:
                    names.append(mrna_id)
                    data[mrna_id] = mrna_id

        with open('../lib/static/mRNA_names.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

        return names

# -------------------------------------------------------------------------------------------------


# Main
def main():
    gff = GffReader("/homes/mbeens/Downloads/Data/test.gff")
    gff.create_freq_line_graph()
    return 0


if __name__ == "__main__":
    exitcode = main()
    sys.exit(exitcode)
