#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2019, Nigel Small
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function

from argparse import ArgumentParser
from base64 import b64decode
from os import path, remove
from os.path import isdir
from xml.etree import ElementTree


REF = u"""\
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│ EUMAK European Keyboard Layout                                                           │
└──────────────────────────────────────────────────────────────────────────────────────────┘
┌─────┐┌───────────────────────────────────┐┌──────────────────────────────────────────────┐
│ 2 4 ││  2 = Shift    │  4 = Shift+AltGr  ││ [Mod]+[~],[X] -> àèìǹòùẁỳǜ ὰὲὴὶὸὺὼ           │
│ 1 3 ││  1 = Normal   │  3 = AltGr        ││ [Mod]+[1],[X] -> áćéǵíḱĺḿńóṕŕśúẃýźḯǘ άέήίόύώ │
└─────┘└───────────────────────────────────┘│ [Mod]+[2],[X] -> ǎčďěǧȟǐǰǩľňǒřšťǔžǚ          │
┌──────────────────────────────────────────┐│ [Mod]+[3],[X] -> âĉêĝĥîĵôŝûŵŷẑ               │
│ [Mod]+[X] -> áćéǵíḱĺḿńóṕŕśúẃýźőű άέήίόύώ ││ [Mod]+[4],[X] -> āēḡīōūȳǟȫǖ                  │
│ [Mod]+[6] -> Toggle Latin/Greek          ││ [Mod]+[5],[X] -> ȧḃċḋėḟġḣıȷŀṁṅȯṗṙṡṫẇẋẏż      │
└──────────────────────────────────────────┘└──────────────────────────────────────────────┘
"""
LATIN = u"""\
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬────────────┐
│ @ ° │ ! ¡ │ " ½ │ £ # │ $ € │ % § │ & ¶ │ | † │ ( « │ ) » │ = ≠ │ / \ │ * · │ Backspace  │
│ ~ ` │ 1 ´ │ 2 ˇ │ 3 ^ │ 4 ¯ │ 5 ˙ │ 6 µ │ 7 { │ 8 [ │ 9 ] │ 0 } │ - ÷ │ + × │            │
├─────┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬──────────┤
│       │ Q Ă │ W Ł │ E Ę │ R Ŧ │ T Ț │ Y Ů │ U Ų │ I Į │ O Ø │ P Õ │ Ü Å │ Ï Ÿ │ Enter    │
│ Tab   │ q ă │ w ł │ e ę │ r ŧ │ t ț │ y ů │ u ų │ i į │ o ø │ p õ │ ü å │ ï ÿ │          │
├───────┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┐        │
│         │ A Ą │ S Ș │ D Đ │ F Þ │ G Ģ │ H Ħ │ J Ñ │ K Ķ │ L Ļ │ Ö Œ │ Ä Æ │ Ë Ẅ │        │
│ Caps    │ a ą │ s ș │ d đ │ f þ │ g ģ │ h ħ │ j ñ │ k ķ │ l ļ │ ö œ │ ä æ │ ë ẅ │        │
├───────┬─┴───┬─┴───┬─┴───┬─┴───┬─┴───┬─┴───┬─┴───┬─┴───┬─┴───┬─┴───┬─┴───┬─┴─────┴────────┤
│       │     │ Z ẞ │ X Ŭ │ C Ç │ V Ð │ B Ã │ N Ņ │ M Ŋ │ ; ≤ │ : ≥ │ ? ¿ │                │
│ Shift │ Mod │ z ß │ x ŭ │ c ç │ v ð │ b ã │ n ņ │ m ŋ │ , < │ . > │ ' _ │ Shift          │
├───────┼─────┴─┬───┴───┬─┴─────┴─────┴─────┴─────┴─────┴──┬──┴────┬┴─────┴┬───────┬───────┤
│       │       │       │                                  │       │       │       │       │
│ Ctrl  │ Meta  │ Alt   │             Space                │ AltGr │ Meta  │ Menu  │ Ctrl  │
└───────┴───────┴───────┴──────────────────────────────────┴───────┴───────┴───────┴───────┘
"""
GREEK = u"""\
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬────────────┐
│ @ ° │ ! ¡ │ " ½ │ £ # │ $ € │ % § │ & ¶ │ | † │ ( « │ ) » │ = ≠ │ / \ │ * · │ Backspace  │
│ ~ ` │ 1 ´ │ 2 ˇ │ 3 ^ │ 4 ¯ │ 5 ˙ │ 6 µ │ 7 { │ 8 [ │ 9 ] │ 0 } │ - ÷ │ + × │            │
├─────┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬──────────┤
│       │ :   │     │ Ε   │ Ρ   │ Τ   │ Υ   │ Θ   │ Ι   │ Ο   │ Π   │ Ϋ   │ Ϊ   │ Enter    │
│ Tab   │ ;   │ ς   │ ε   │ ρ   │ τ   │ υ   │ θ   │ ι   │ ο   │ π   │ ϋ   │ ϊ   │          │
├───────┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┐        │
│         │ Α   │ Σ   │ Δ   │ Φ   │ Γ   │ Η   │ Ξ   │ Κ   │ Λ   │     │     │     │        │
│ Caps    │ α   │ σ   │ δ   │ φ   │ γ   │ η   │ ξ   │ κ   │ λ   │     │     │     │        │
├───────┬─┴───┬─┴───┬─┴───┬─┴───┬─┴───┬─┴───┬─┴───┬─┴───┬─┴───┬─┴───┬─┴───┬─┴─────┴────────┤
│       │     │ Ζ   │ Χ   │ Ψ   │ Ω   │ Β   │ Ν   │ Μ   │ ; « │ : » │ ? ¿ │                │
│ Shift │ Mod │ ζ   │ χ   │ ψ   │ ω   │ β   │ ν   │ μ   │ , < │ . > │ ' _ │ Shift          │
├───────┼─────┴─┬───┴───┬─┴─────┴─────┴─────┴─────┴─────┴──┬──┴────┬┴─────┴┬───────┬───────┤
│       │       │       │                                  │       │       │       │       │
│ Ctrl  │ Meta  │ Alt   │             Space                │ AltGr │ Meta  │ Menu  │ Ctrl  │
└───────┴───────┴───────┴──────────────────────────────────┴───────┴───────┴───────┴───────┘
"""

LANGUAGES = [
    "eng",
    "deu",
    "fra",
    "ita",
    "spa",
    "pol",
    "ron",
    "nld",
    "swe",
]


class XKB(object):

    xkb = "/usr/share/X11/xkb"

    rules = path.join(xkb, "rules", "evdev.xml")
    symbols = path.join(xkb, "symbols", "eumak")

    def __init__(self):
        if not isdir(self.xkb):
            raise OSError("XKB installation not found at %s" % self.xkb)
        self._tree = ElementTree.parse(self.rules)
        self._root = self._tree.getroot()
        self._layout_list = self._root.find("./layoutList")

    def install(self):
        self._install_symbols()
        self._uninstall_layout()
        self._install_layout()
        self._tree.write(self.rules)

    def uninstall(self):
        self._uninstall_symbols()
        self._uninstall_layout()
        self._tree.write(self.rules)

    def _install_symbols(self):
        with open(self.symbols, "w") as f:
            f.write(b64decode(DATA))

    def _uninstall_symbols(self):
        if path.isfile(self.symbols):
            remove(self.symbols)

    def _install_layout(self):
        layout = ElementTree.SubElement(self._layout_list, "layout")
        config_item = ElementTree.SubElement(layout, "configItem")
        ElementTree.SubElement(config_item, "name").text = "eumak"
        ElementTree.SubElement(config_item, "shortDescription").text = "eumak"
        ElementTree.SubElement(config_item, "description").text = "European (Eumak)"
        language_list = ElementTree.SubElement(config_item, "languageList")
        for lang in LANGUAGES:
            ElementTree.SubElement(language_list, "iso639Id").text = lang
        ElementTree.SubElement(layout, "variantList")

    def _uninstall_layout(self):
        to_delete = []
        for layout in self._layout_list.iterfind("layout"):
            name = layout.find("configItem/name")
            if name.text == "eumak":
                to_delete.append(layout)
        for layout in to_delete:
            self._layout_list.remove(layout)


def main():
    parser = ArgumentParser(description="Eumak keyboard layout installer")
    parser.add_argument("-i", "--install", action="store_true")
    parser.add_argument("-u", "--uninstall", action="store_true")
    args = parser.parse_args()
    xkb = XKB()
    if args.install:
        xkb.install()
    elif args.uninstall:
        xkb.uninstall()
    else:
        print(REF, end="")
        print(LATIN, end="")
        print(GREEK, end="")
