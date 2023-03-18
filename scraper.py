from lxml import html
import requests
import sys

page = requests.get('https://www.wheresthematch.com/live-football-on-tv/')
tree = html.fromstring(page.content)

#This will create a list of buyers:
fixture_details = tree.xpath('//span[@class="fixture"]/a/em/text()')
fixture_comp = tree.xpath('//tr/td[@class="competition-name"]//span[not (@class)]/text()')
fixture_channel = tree.xpath('//tr/td[@class="channel-details"]/span[1]/text()')
fixture_time = tree.xpath('//span[@class="time"]/em/text()')
#//tr/td[@class='channel-details']/span[1]/text()

fixture = []
for i in range(0, len(fixture_details), 2):
	output_text = fixture_details[i].strip() + ' vs ' + fixture_details[i+1].strip()
#	print(i)
#	print(output_text)
	fixture.append(output_text)

#print('Buyers: ', fixture_details)
# print('We\'ve found ' + str(len(fixture)) + ' fixtures')
# print('We\'ve found ' + str(len(fixture_comp)) + ' comps')
# print('We\'ve found ' + str(len(fixture_channel)) + ' channels')
#print(fixture_comp)

#print ('{} {} {}'.format(len(fixture), len(fixture_comp), len(fixture_channel)))

json_fix_list = []
for i in range(0, len(fixture_channel)):
# 	print("{} / {} / {}".format(fixture[i], fixture_comp[i], fixture_channel[i]))
	json_fix = '{' + '"title":"{} - {}",'.format(fixture[i], fixture_comp[i], fixture_channel[i])
	json_fix += '"subtitle":"{} on {}"'.format(fixture_time[i].strip(), fixture_channel[i]) + '},'
	json_fix_list.append(json_fix)

#print(sys.argv[1].upper())
filtered_list = []
if len(sys.argv) > 1:
	for i in range(0, len(fixture_channel)):
		if (sys.argv[1].upper() in json_fix_list[i].upper()):
			filtered_list.append(json_fix_list[i])
else:
	filtered_list = json_fix_list

print('{"items":[')
for i in range(0, min(5, len(filtered_list))):
	print(filtered_list[i])
print(']}')

# for i in range(0, 10):
# 	print("{} / {} / {}".format(fixture[i], fixture_comp[i], fixture_channel[i]))
