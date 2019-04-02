
def make_output_line_freq(data):
    with open("../lib/static/output/freq_length.txt", "w") as output:
        for feature in data:
            output.write("{}\n".format(feature[0]))
            output.write("Length\t\t\t\tFrequentie\n")
            for index in range(len(feature[1])):
                output.write("{}\t\t\t\t{}\n".format(feature[1][index], feature[2][index]))
                if feature[1][index] == feature[1][-1] and not feature == data[-1]:
                    output.write("\n")


def make_output_gem_length(data):
    with open("../lib/static/output/gem_length.txt", "w") as output:
        output.write("Feature\t\t\t\tGemiddelde lengte\n")
        for feature in data:
            output.write("{}\t\t\t\t{}\n".format(feature[0], feature[1]))


def make_output_exon_intron(data):
    with open("../lib/static/output/exon_intron.txt", "w") as output:
        output.write("Name of mRNA\t\tExon percentage\t\tIntron percentage\n")
        for index in range(len(data[0])):
            output.write("{}\t\t{}%\t\t\t{}%\n".format(data[0][index],
                                                       round(data[1][index], 2), round(data[2][index], 2)))
