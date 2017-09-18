# encoding=utf-8

from sources.Shulchan_Arukh.ShulchanArukh import *

root = Root('../../Orach_Chaim.xml')
base = root.get_base_text()
filename = u'../../txt_files/Orach_Chaim/part_3/מחבר שולחן ערוך אורח חיים חלק ג.txt'

base.remove_volume(3)
with codecs.open(filename, 'r', 'utf-8') as infile:
    volume = base.add_volume(infile.read(), 3)
assert isinstance(volume, Volume)

volume.mark_simanim(u'@22([\u05d0-\u05ea]{1,4})', specials={u'@00': {'name': u'topic'}})
print "Validating Simanim"
volume.validate_simanim()

bad = volume.mark_seifim(u'@11([\u05d0-\u05ea]{1,3})', specials={u'@23': {'name': u'title'}})
print 'Validating Seifim'
for i in bad:
    print i
volume.validate_seifim()
'''
אשל אברהם:
ur'@99([\u05d0-\u05ea]{1,2})\]'
'''

codes = [ur'@77', ur'@66', ur'@14', ur'@55']
patterns = [ur'@77\(({})\)', ur'@66\(({})\)', ur'@14\[({})\]', ur'@55({})']
patterns = [i.format(ur'[\u05d0-\u05ea]{1,3}') for i in patterns]

# for pattern in patterns:
#     correct_marks_in_file(filename, u'@22', pattern)
# correct_marks_in_file(filename, u'@22', ur'@44([\u05d0-\u05ea])', error_finder=out_of_order_he_letters)

volume.validate_references(ur'@44([\u05d0-\u05ea])', ur'@44', key_callback=he_ord)
for pattern, code in zip(patterns, codes):
    volume.validate_references(pattern, code)

root.export()
