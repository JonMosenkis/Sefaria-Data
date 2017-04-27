# encoding=utf-8

import codecs
import re
from data_utilities.util import ja_to_xml, multiple_replace, traverse_ja, file_to_ja_g
from data_utilities.util import getGematria, numToHeb

from collections import OrderedDict
import unicodecsv as csv

from sources.functions import post_text, post_index, post_link
from sefaria.model import *
from sefaria.datatype.jagged_array import JaggedArray


def map_semak_day(filename): # alt struct according to days. (not sure how alt struct works
    pass


def parse_semak(filename):

    def cleaner(my_text):
        replace_dict = {u'@11(.*?)@12': ur'<b>\1</b>', u'@33(.*?)@34': ur'<b>\1</b>', u'@33(.*?)@34': ur'<b>\1</b>', u'@66(.*?)@67': ur'\1'}#, u'@55[\u05d0-\u05ea]{1,3}' : u'<i-tags = >'}
        new = []
        for line in my_text:
            line = multiple_replace(line,replace_dict,using_regex=True)
            new.append(line)
        return new


    regs = [ur'@22(?P<gim>[\u05d0-\u05ea]{1,3})'] #, u'@(11|23|33)(?P<gim>)']
    with codecs.open(filename, 'r', 'utf-8') as fp:
        lines = fp.readlines()
    starting = None
    # check if we got to the end of the legend and change to started
    # clean all lines of days start with @00
    cleaned = []
    letter_section = []
    for line_num, line in enumerate(lines):
        if line == u'\n':
            starting = line_num + 1
            break
    for line_num, line in enumerate(lines[starting:]):
        if not re.search(u'@00', line) and not line.isspace():
            if re.search(u'@22', line):
                line = re.split(u'(@22[\u05d0-\u05ea]{1,3})', line)
                if isinstance(line, basestring):
                    cleaned.append(line)
                else:
                    [cleaned.append(st) for st in line if st]
            else:
                cleaned.append(line)
    try:
        smk_ja = file_to_ja_g(2, cleaned, regs, cleaner, gimatria=True,  grab_all=[False, True, True], group_name = 'gim').array() #group_name = 'gim',
    except AttributeError:
        print 'there are more regs then levels...'

    ja_to_xml(smk_ja, ['letter', 'segments'], 'smk.xml')

    return smk_ja


#todo:
# i would want to devide the Raph according to simanim as well and not according to pages,
# once one has the mapping of simanim to dapim this is possible
def parse_Raph(filename):
    def cleaner(my_text):
        replace_dict = {u'@(?:11|77)[\u05d0-\u05ea]{0,3}': u'', u'@(33|22)': u''}#{u'@11(.*?)@12': ur'<b>\1</b>', u'@33(.*?)@34': ur'<b>\1</b>', u'@33(.*?)@34': ur'<b>\1</b>', u'@66(.*?)@67': ur'\1'}
        new = []
        for line in my_text:
            line = multiple_replace(line,replace_dict,using_regex=True)
            new.append(line)
        return new

    regs = [ur'@77(?P<gim>[\u05d0-\u05ea]{0,3})', ur'@11(?P<gim>[\u05d0-\u05ea]{1,3})']  # (?P<gim>[\u05d0-\u05ea]{1,3})
    with codecs.open(filename, 'r', 'utf-8') as fp:
        lines = fp.readlines()
    starting = None
    # check if we got to the end of the legend and change to started
    # clean all lines of days start with @00
    cleaned = []
    letter_section = []
    for line_num, line in enumerate(lines):
        if line == u'\n':
            starting = line_num + 1
            break
    for line_num, line in enumerate(lines[starting:]):
        if not re.search(u'@00', line) and not line.isspace():
            line = re.split(u'(@(?:77|11)[\u05d0-\u05ea]{0,3})', line)
            if isinstance(line, basestring):
                cleaned.append(line)
            else:
                [cleaned.append(st.strip()) for st in line if st]#(st and not re.search(u'@(77)', st))]
            # else:
            #     cleaned.append(line)
    try:
        ja = file_to_ja_g(3, cleaned, regs, cleaner, gimatria=True,  grab_all=[False, False, True], group_name='gim').array()
    except AttributeError:
        print 'there are more regs then levels...'

    ja_to_xml(ja, ['page', 'letter', 'segments'], 'raph.xml')

    return ja


def parse_Raph_by_letter(filename):
    def cleaner(my_text):
        replace_dict = {u'@(?:11|77)[\u05d0-\u05ea]{0,3}': u'', u'@(33|22)': u''}#{u'@11(.*?)@12': ur'<b>\1</b>', u'@33(.*?)@34': ur'<b>\1</b>', u'@33(.*?)@34': ur'<b>\1</b>', u'@66(.*?)@67': ur'\1'}
        new = []
        for line in my_text:
            line = multiple_replace(line, replace_dict, using_regex=True)
            new.append(line)
        return new

    regs = [ur'@11(?P<gim>[\u05d0-\u05ea]{1,3})']
    with codecs.open(filename, 'r', 'utf-8') as fp:
        lines = fp.readlines()
    starting = None
    # check if we got to the end of the legend and change to started
    # clean all lines of days start with @00
    cleaned = []
    for line_num, line in enumerate(lines):
        if line == u'\n':
            starting = line_num + 1
            break
    for line_num, line in enumerate(lines[starting:]):
        if not re.search(u'@00', line) and not line.isspace():
            line = re.split(u'(@11[\u05d0-\u05ea]{0,3})', line)
            if isinstance(line, basestring):
                cleaned.append(line)
            else:
                [cleaned.append(st.strip()) for st in line if st]
    new_ja = regs_devide(cleaned, regs)
    try:
        ja = file_to_ja_g(2, cleaned, regs, cleaner, gimatria=True,  grab_all=[True, True], group_name='gim').array()
    except AttributeError:
        print 'there are more regs then levels...'

    ja_to_xml(new_ja, ['Alef', 'letter', 'segments'], 'raph_letters.xml')

    return new_ja


def parse_Raph_simanim(filename, raph_smk_alignment):
    def cleaner(my_text):
        replace_dict = {u'@(?:11|77)[\u05d0-\u05ea]{0,3}': u'', u'@(33|22)': u''}#{u'@11(.*?)@12': ur'<b>\1</b>', u'@33(.*?)@34': ur'<b>\1</b>', u'@33(.*?)@34': ur'<b>\1</b>', u'@66(.*?)@67': ur'\1'}
        new = []
        for line in my_text:
            line = multiple_replace(line, replace_dict, using_regex=True)
            new.append(line)
        return new

    regs = [ur'@11(?P<gim>[\u05d0-\u05ea]{1,3})']
    with codecs.open(filename, 'r', 'utf-8') as fp:
        lines = fp.readlines()
    starting = None
    # check if we got to the end of the legend and change to started
    # clean all lines of days start with @00
    cleaned = []
    for line_num, line in enumerate(lines):
        if line == u'\n':
            starting = line_num + 1
            break
    for line_num, line in enumerate(lines[starting:]):
        if not re.search(u'@00', line) and not line.isspace():
            line = re.split(u'@11[\u05d0-\u05ea]{0,3}', line)
            if isinstance(line, basestring):
                cleaned.append(line)
            else:
                [cleaned.append(st.strip()) for st in line if st]
    for ln in cleaned:
        pass
    ja = []
    ja_to_xml(ja, ['siman', 'letter', 'segments'], 'raph_simanim.xml')

    return ja



def parse_hagahot_by_letter(filename):
    def cleaner(my_text):
        replace_dict = {u'@11\([\u05d0-\u05ea]{0,3}\)': u''}
        new = []
        for line in my_text:
            line = multiple_replace(line, replace_dict, using_regex=True)
            new.append(line)
        return new

    regs = [ur'@11\((?P<gim>[\u05d0-\u05ea]{1,3})\)']
    with codecs.open(filename, 'r', 'utf-8') as fp:
        lines = fp.readlines()
    starting = None
    # check if we got to the end of the legend and change to started
    # clean all lines of days start with @00
    cleaned = []
    for line_num, line in enumerate(lines):
        if line == u'\n':
            starting = line_num + 1
            break
    for line_num, line in enumerate(lines[starting:]):
        if not re.search(u'\$', line) and not line.isspace():
            line = re.split(u'(@11\([\u05d0-\u05ea]{0,3}\))', line)
            if isinstance(line, basestring):
                cleaned.append(line)
            else:
                [cleaned.append(st.strip()) for st in line if st]
    try:
        ja = file_to_ja_g(2, cleaned, regs, cleaner, gimatria=True,  grab_all=[True, True], group_name='gim').array()
    except AttributeError:
        print 'there are more regs then levels...'
    new_ja = regs_devide(cleaned, regs, u'(נשלם מלאכת שבעת הימים)')
    ja_to_xml(new_ja, ['siman', 'letter', 'segments'], 'hagahot_letters.xml')

    return new_ja


def map_semak_page_siman(smk_ja, to_print = True):
    '''
    create a dictionary from key: siman value: page(s) that the siman is on
    :param smk_ja: smk ja parsed according to simanim @22
    :return: dictionary. keys: siman (he letter), value: list of pages the siman spans over. (pages according to scan -
    starts on p. 21)
    '''
    siman_page = OrderedDict()
    page_count = 21
    start_page = False
    lst_seg = {'data': '', 'indices': []}
    for seg in traverse_ja(smk_ja):
        for i, page in enumerate(re.finditer(u'@77', seg['data'])):
            page_count += 1
            try:
                siman_page[numToHeb(seg['indices'][0]+1)].append(page_count)
            except KeyError:
                if not start_page:
                    siman_page[numToHeb(seg['indices'][0] + 1)] = [page_count - 1, page_count]
                    start_page = False
                else:
                    siman_page[numToHeb(seg['indices'][0]+1)] = [page_count]
            if re.search(u'@77 ?$', lst_seg['data']):
                start_page = True
                siman_page[numToHeb(lst_seg['indices'][0] + 1)].remove(page_count)
        if not list(re.finditer(u'@77', seg['data'])):
            try:
                siman_page[numToHeb(seg['indices'][0]+1)]
            except KeyError:
                siman_page[numToHeb(seg['indices'][0] + 1)] = [page_count]
            if re.search(u'@77 ?$', lst_seg['data']):
                start_page = True
                try:
                    siman_page[numToHeb(lst_seg['indices'][0] + 1)].remove(page_count)
                except ValueError:
                    pass
        lst_seg = seg
    if to_print:
        for k in siman_page.keys():
            print k, siman_page[k]
    return siman_page


def link_semak_raph(smk_ja, raph_ja):
    #if segment in smak_ja has a @55[\u05d0-\u05ea]{0,3} extract the letter and match it to the segment in the ja_raph
    #by running on the ja_raph segments
    smk_raph = []
    raph_letter = []
    for seg in traverse_ja(smk_ja):
        if re.search(u'@55[\u05d0-\u05ea]{0,3}', seg['data']):
            for letter in re.findall(u'@55([\u05d0-\u05ea]{0,3})', seg['data']):
                # smk_raph.append([seg['indices'][:], letter])
                smk_raph.append([letter, seg['indices']])
    last = [-1, -1]
    for seg in traverse_ja(raph_ja):
        if seg['indices'][0:2] == last[0:2]:
            continue
        else:
            raph_letter.append(seg)
        last = seg['indices']

    problem_count = 0
    for smk, raph in zip(smk_raph, raph_letter):
        if getGematria(smk[0]) == (raph['indices'][1]+1):
            print getGematria(smk[0]), raph['indices'][1]+1, \
                [item+1 for item in smk[1]], [item +1 for item in raph['indices']]
        else:
            problem_count +=1
            print 'problem:', getGematria(smk[0]), raph['indices'][1]+1,\
                [item+1 for item in smk[1]], [item +1 for item in raph['indices']]
    print problem_count


def regs_devide(lines, regs, eof=None):
    reg = regs[0]
    ja = []
    letter = []
    siman = []
    for line in lines:
        comb_letter = ' '.join(letter)
        if re.search(reg, line) or (eof and re.search(eof, line)):
            siman.append(comb_letter)
            letter = []
            if re.search(reg, line):
                gim = getGematria(re.search(reg, line).group(1))
            if gim == 1 or (eof and re.search(eof, line)):
                ja.append(siman)
                if siman == ['']:
                    ja.pop()
                siman = []
        letter.append(line)
    return ja


def raph_alignment_report(ja_smk, letter_ja):
    csv_lst = []
    lst_raph = []
    smk_siman = 0
    smk_pages = map_semak_page_siman(ja_smk, to_print=False)
    for seg in traverse_ja(ja_smk):
        for raph_l_in_smk in re.finditer(u'@55([\u05d0-\u05ea]{1,3})', seg['data']):
            lst_raph.append((raph_l_in_smk.group(1),
                             seg['data'][raph_l_in_smk.span()[0] - 20: raph_l_in_smk.span()[1] + 20],
                             (seg['indices'][0] + 1)))
    raph_11 = []
    for raph in traverse_ja(letter_ja):
        raph_11.append(raph)  # re.search(u'@11([\u05d0-\u05ea]{1,3})', raph['data']).group(1))
    page = 21
    prob = 0
    for raph, smk_l in zip(raph_11, lst_raph):

        print re.search(u'@11([\u05d0-\u05ea]{1,3})', raph['data']).group(1), smk_l[0], numToHeb(smk_l[2])
        csv_dict = {u'smk letter': smk_l[0], u'raph letter': re.search(u'@11([\u05d0-\u05ea]{1,3})', raph['data']).group(1),
                    u'smk words': smk_l[1], u'raph line': raph['data'], u'siman': numToHeb(smk_l[2]), u'aprx page in scan': smk_pages[numToHeb(smk_l[2])]}
        if re.search(u'@77', smk_l[1]):
            page += 1
        if re.search(u'@11([\u05d0-\u05ea]{1,3})', raph['data']).group(1) != smk_l[0]:
            prob += 1
            print "*"
            csv_dict['problem'] = True
            # break
        csv_lst.append(csv_dict)
    print 'prob', prob
    print 'done'
    toCSV(u'testcsvreport', csv_lst, [u'smk letter', u'raph letter', u'smk words',
                                u'raph line', u'siman', u'aprx page in scan', u'problem'])
    return csv_lst


def toCSV(filename, list_rows, column_names):
    with open(u'{}.csv'.format(filename), 'w') as csv_file:
        writer = csv.DictWriter(csv_file, column_names)
        writer.writeheader()
        writer.writerows(list_rows)


def hagahot_alignment(ja_smk, ja_raph, ja_hagahot):
    for seg in traverse_ja(ja_smk):
        re.search(seg['data'])

if __name__ == "__main__":
    ja_smk = parse_semak('Semak.txt')
    siman_page = map_semak_page_siman(ja_smk, to_print=False)
    # ja_raph = parse_Raph('Raph_on_Semak.txt')
    # link_semak_raph(ja_smk, ja_raph)
    letter_ja = parse_Raph_by_letter(u'Raph_on_Semak.txt')
    raph_smk_alignment = raph_alignment_report(ja_smk, letter_ja)
    ja_hagahot = parse_hagahot_by_letter(u'Semak_hagahot_chadashot.txt')
    parse_Raph_simanim(u'Raph_on_Semak.txt', raph_smk_alignment)
# use ja functions and not travers ja. or through them first into a list instead of getting them live. classic...
