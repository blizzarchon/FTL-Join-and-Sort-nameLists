
from xml.etree import ElementTree

def ftl_names_v2(node, names, short_names):
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

    :param wf: a file to write to
    :param short_male: list with the <name="short"> tags for male nameList
    :param reg_male: list with the <name> tags for male nameList
    :param short_female: list with the <name="short"> tags for female nameList
    :param reg_female: list with the <name> tags for female nameList
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
                 "".format(name_tuple[0], name_tuple[1]))
    for name_string in sorted(reg_female):
        wf.write("\t<name>{}</name>\n"
                 "".format(name_string))
    wf.write("</nameList>\n")


def xmlize(event_root, writer):
    """ Does XML stuff using event_root as a tree representing a read-only file
        and writer as as a write-only file.

    :param event_root: the head node of a tree containing XML data
    :param writer: a file open for writing
    :rtype: None
    """
    naming = False
    # male_names_list, male_short_names_list = [], []
    # female_names_list, female_short_names_list = [], []
    names_list, short_names_list = [], []
    for child in event_root:
        if ((child.tag == 'weaponBlueprint') and
                ("DRONE" not in child.attrib['name'])):
            tooltips(child, writer)
        if child.tag == 'nameList':
            # ftl_names(child, writer)
            if not naming:
                naming = True
            if child.attrib['sex'] == 'male':
                # names_list was male_names_list
                ftl_names_v2(child, names_list, short_names_list)
            elif child.attrib['sex'] == 'female':
                # names_list was female_names_list
                ftl_names_v2(child, names_list, short_names_list)
            else:
                raise ValueError("nameList's 'sex' attribute must "
                                 "either be male or female!\n")
    if naming:
        # write_names(writer, male_short_names_list, male_names_list,
        #             female_short_names_list, female_names_list)
        write_names(writer, short_names_list, names_list,
                    short_names_list, names_list)


if __name__ == '__main__':

    reading = input("\nEnter name of file in this directory to read from:\n")

    with open(reading, 'r') as reading_file:
        tree = ElementTree.parse(reading_file)
        root = tree.getroot()

        writing = input("Enter name of new file name to write to.\n")
        with open(writing, 'w') as writing_file:
            xmlize(root, writing_file)
