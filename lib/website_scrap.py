import requests
from lxml import html

page = requests.get("http://flybase.org/reports/FBtr0078116")
tree = html.fromstring(page.content)

value = tree.xpath('//div[@class="col-sm-3 col-sm-height"]/text()')

print(value[1])


mRNAs = ['FBtr0078135', 'FBtr0078136', 'FBtr0078137', 'FBtr0078129', 'FBtr0078138', 'FBtr0078128', 'FBtr0078139', 'FBtr0078127',
        'FBtr0078142', 'FBtr0078141', 'FBtr0078140', 'FBtr0078143', 'FBtr0078126', 'FBtr0299837', 'FBtr0078144',
        'FBtr0078145', 'FBtr0078125', 'FBtr0078146', 'FBtr0078124', 'FBtr0078123', 'FBtr0078122', 'FBtr0078121', 'FBtr0091612',
        'FBtr0078119', 'FBtr0078120', 'FBtr0078118', 'FBtr0078117', 'FBtr0078147', 'FBtr0300107', 'FBtr0078116',
        'FBtr0078150', 'FBtr0078151', 'FBtr0078152', 'FBtr0078115', 'FBtr0078114', 'FBtr0078155', 'FBtr0078153', 'FBtr0100379',
        'FBtr0078154', 'FBtr0078159', 'FBtr0078156', 'FBtr0100310', 'FBtr0100309', 'FBtr0100308', 'FBtr0100307',
        'FBtr0078158', 'FBtr0078157', 'FBtr0078160', 'FBtr0089436', 'FBtr0089435', 'FBtr0089434', 'FBtr0089433', 'FBtr0089432',
        'FBtr0089431', 'FBtr0089430', 'FBtr0089429', 'FBtr0089428', 'FBtr0089437', 'FBtr0078161', 'FBtr0078104',
        'FBtr0078103', 'FBtr0290323', 'FBtr0114507', 'FBtr0078101', 'FBtr0078100', 'FBtr0113416', 'FBtr0113415', 'FBtr0078164',
        'FBtr0078163', 'FBtr0113008', 'FBtr0078169', 'FBtr0078168', 'FBtr0078167', 'FBtr0078166', 'FBtr0078171',
        'FBtr0078170', 'FBtr0089256']

for mRNA in mRNAs:
    page = requests.get("http://flybase.org/reports/{}".format(mRNA))
    tree = html.fromstring(page.content)
    name_mRNA = tree.xpath('//div[@class="col-sm-3 col-sm-height"]/text()')
    if not name_mRNA == []:
        print(name_mRNA[1])
    else:
        print(mRNA)
