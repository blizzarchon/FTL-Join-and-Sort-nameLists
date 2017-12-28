
from xml.etree import ElementTree

def sort_names(node, names, short_names):
    """ Sorts the <name /> tags in node into short_names if the tag contains
        a "short" attribute, or names if the tag is just plain.

    :param node: tree representing a nameList
    :param names: list
    :param short_names: list
    :rtype: None
    """
    for name in node:
        if name.tag != 'name':
            raise AttributeError("Bad tag in nameList!\n")
        elif len(name.attrib) > 0:
            if (name.attrib['short'], name.text) not in short_names:
                short_names.append((name.attrib['short'], name.text))
        else:
            if name.text not in names:
                names.append(name.text)


def write_names(wf, short_male, reg_male, short_female, reg_female):
    """ Writes the names of two nameLists in "alphabetical" order into wf.
    Adds zero-width spaces to names in the female nameList to make them unique.

    :param wf: a file to write to
    :param short_male:   list with the <name="short"> tags for male nameList
    :param reg_male:     list with the <name> tags for male nameList
    :param short_female: list with the <name="short"> tags for female nameList
    :param reg_female:   list with the <name> tags for female nameList
    :rtype: None
    """
    wf.write("<nameList race=\"human\" sex=\"male\">\n")
    for name_tuple in sorted(short_male):
        wf.write("\t<name short=\"{}\">{}</name>\n"
                 "".format(name_tuple[0], name_tuple[1]))
    for name_string in sorted(reg_male):
        wf.write("\t<name>{}</name>\n"
                 "".format(name_string))
    wf.write("</nameList>\n\n"
             "<nameList race=\"human\" sex=\"female\">\n")
    for name_tuple in sorted(short_female):
        wf.write("\t<name short=\"{}\">{}</name>\n"
                 "".format(name_tuple[0], 
                           name_tuple[1] + '\u200b'))
    for name_string in sorted(reg_female):
        wf.write("\t<name>{}</name>\n"
                 "".format(name_string + '\u200b'))
    wf.write("</nameList>\n")


def xmlize(event_root, writer, join_truth):
    """ Does XML stuff using event_root as a tree representing a read-only file
        and writer as a write-only file.

    :param event_root: the head node of a tree containing XML data
    :param writer: a file open for writing
    :param join_truth: True if all nameLists should be joined,
                       regardless of gender. 
    :rtype: None
    """
    if join_truth:
        names_list, short_names_list = [], []
        for child in event_root:
            if child.tag == 'nameList':
                if child.attrib['sex'] == 'male' or \
                        child.attrib['sex'] == 'female':
                    sort_names(child, names_list, short_names_list)
                else:
                    raise ValueError("nameList's 'sex' attribute must "
                                     "either be male or female!\n")
        # if both empty, don't write
        if names_list or short_names_list:
            write_names(writer, short_names_list, names_list,
                        short_names_list, names_list)
    else:
        m_names_list, m_short_names_list = [], []
        f_names_list, f_short_names_list = [], []
        for child in event_root:
            if child.tag == 'nameList':
                if child.attrib['sex'] == 'male':
                    sort_names(child, m_names_list, m_short_names_list)
                elif child.attrib['sex'] == 'female':
                    sort_names(child, f_names_list, f_short_names_list)
                else:
                    raise ValueError("nameList's 'sex' attribute must "
                                     "either be male or female!\n")
        # if both male nameList and female nameList empty, don't write
        if (m_names_list or m_short_names_list) and \
                (f_names_list or f_short_names_list):
            write_names(writer, m_short_names_list, m_names_list,
                        f_short_names_list, f_names_list)


if __name__ == '__main__':

    reading = input("Enter name of file in this directory to read from:\n")

    with open(reading, 'r') as reading_file:
        tree = ElementTree.parse(reading_file)
        root = tree.getroot()

        writing = input("Enter name of new file name to write to.\n")
        # utf-8 encoding needed in order to write zero-width space to file
        with open(writing, 'w', encoding='utf-8') as writing_file:
            join_all = input("Join all nameLists regardless of gender? "
                             "(enter y or n)\n")
            # default is to keep separate -- entered n
            join_regardless = False
            if join_all == 'y':
                join_regardless = True
            
            xmlize(root, writing_file, join_regardless)
