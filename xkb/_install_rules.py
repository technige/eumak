#!/usr/bin/env python

from xml.etree import ElementTree
from sys import argv


class LayoutList(object):

    languages = ["eng", "deu", "fra", "ita", "spa", "pol", "ron", "nld", "swe"]

    def __init__(self, evdev):
        self.evdev = evdev
        self.tree = ElementTree.parse(self.evdev)
        self.root = self.tree.getroot()
        self.layout_list = self.root.find("./layoutList")

    def install(self):
        layout = ElementTree.SubElement(self.layout_list, "layout")
        config_item = ElementTree.SubElement(layout, "configItem")
        ElementTree.SubElement(config_item, "name").text = "eumak"
        ElementTree.SubElement(config_item, "shortDescription").text = "eumak"
        ElementTree.SubElement(config_item, "description").text = "European (Eumak)"
        language_list = ElementTree.SubElement(config_item, "languageList")
        for lang in self.languages:
            ElementTree.SubElement(language_list, "iso639Id").text = lang
        variant_list = ElementTree.SubElement(layout, "variantList")

    def uninstall(self):
        to_delete = []
        for layout in self.layout_list.iterfind("layout"):
            name = layout.find("configItem/name")
            if name.text == "eumak":
                to_delete.append(layout)
        for layout in to_delete:
            self.layout_list.remove(layout)

    def save(self):
        self.tree.write(self.evdev)


def usage():
    print("Usage: {} install|uninstall evdev.xml".format(argv[0]))
    exit(1)


def main():
    if len(argv) < 3:
        usage()
    mode = argv[1]
    layout_list = LayoutList(argv[2])
    if mode == "install":
        layout_list.uninstall()
        layout_list.install()
    elif mode == "uninstall":
        layout_list.uninstall()
    else:
        usage()
    layout_list.save()


if __name__ == "__main__":
    main()

