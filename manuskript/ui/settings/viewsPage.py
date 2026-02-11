#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gdk
from rich import inspect

from manuskript.data import Settings, SettingsKeys


"""
Tree/Colours/Icon color => viewSettings/Tree/Icon
Tree/Colours/Text color => viewSettings/Tree/Text
Tree/Colours/Background color => viewSettings/Tree/Background
Tree/Icon size => viewSettings/Tree/iconSize
Tree/Char counter => countSpaces
Tree/Folders => viewSettings/Tree/InfoFolder
Tree/Text => viewSettings/Tree/InfoText

Outline/Colours/Icon color => ViewSettings/Outline/Icon
Outline/Colours/Text color => ViewSettings/Outline/Text
Outline/Colours/Background color => ViewSettings/Outline/Background
Outline/Visible columns/Title => outlineViewColumns/0 (c'est un tableau :/)
Outline/Visible columns/POV => outlineViewColumns/5
Outline/Visible columns/Label => outlineViewColumns/7
Outline/Visible columns/Status => outlineViewColumns/8
Outline/Visible columns/Compile => outlineViewColumns/9
Outline/Visible columns/Word count => outlineViewColumns/11
Outline/Visible columns/Goal => outlineViewColumns/12
Outline/Visible columns/Percentage => outlineViewColumns/13

Index cards/Item Colours/Icon colour => viewSettings/Cork/Icon
Index cards/Item Colours/Text colour => viewSettings/Cork/Text
Index cards/Item Colours/Background colour => viewSettings/Cork/Background
Index cards/Item Colours/Border colour => viewSettings/Cork/Border
Index cards/Item Colours/Corner colour => viewSettings/Cork/Corner
Index cards/Style/Old Style => corkStyle = old
Index cards/Style/New Style => corkStyle = new
Index cards/Background/Colour => corkBackground/color [bugged]
Index cards/Background/Image => corkBackground/image [bugged]

Text Editor/Colours/Background => textEditor/background
Text Editor/Colours/Transparent => textEditor/backgroundTransparent
Text Editor/Colours/Color => textEditor/fontColor
Text Editor/Font/Family => textEditor/font ( "font": >> "FreeSerif <<,11,-1,5,50,0,0,0,0,0",)
Text Editor/Font/Size => textEditor/font ( "font": "FreeSerif, >> 11 <<,-1,5,50,0,0,0,0,0",)
Text Editor/Font/Misspelled => textEditor/misspelled
Text Editor/Text area/max width => textEditor/maxWidth=0
Text Editor/Text area/max width value => textEditor/maxWidth>0
Text Editor/Text area/top-bottom margins => textEditor/marginsTB
Text Editor/Text area/left-right margins => textEditor/marginsLR
Text Editor/Paragraphs/Alignment => textEditor/textAlignment
Text Editor/Paragraphs/line spacing => [unknown]
Text Editor/Paragraphs/line spacing value => textEditor/lineSpacing
Text Editor/Paragraphs/tab width => textEditor/tabWidth
Text Editor/Paragraphs/Indent 1st line => textEditor/indent
Text Editor/Paragraphs/Spacing first value => textEditor/spacingAbove
Text Editor/Paragraphs/Spacing second value => textEditor/spacingBelow
Text Editor/Cursor/Use block insertion of => textEditor/cursorWidth = 1
Text Editor/Cursor/Use block insertion value => textEditor/cursorWidth > 1
Text Editor/Cursor/Disable blinking => textEditor/cursorNotBlinking
Text Editor/Cursor/Typewriter mode => textEditor/alwaysCenter [don't ask me why]
Text Editor/Cursor/Focus mode => textEditor/focusMode

fullScreen : fullScreenTheme [ TODO For later, the files are stored in ./manuskript/resources/themes/newtheme.theme]
themeEdit/Theme name =>
themeEdit/Window Background/color =>
themeEdit/Window Background/Image =>
themeEdit/Window Background/Type =>
themeEdit/Text Background/colour =>
themeEdit/Text Background/opacity =>
themeEdit/Text Background/position =>
themeEdit/Text Background/width =>
themeEdit/Text Background/corner radius =>
themeEdit/Text Background/margins =>
themeEdit/Text Background/padding =>
themeEdit/Text Options/Color =>
themeEdit/Text Options/Font =>
themeEdit/Text Options/Size =>
themeEdit/Text Options/Misspelled =>
themeEdit/Paragraph Options/Alignment =>
themeEdit/Paragraph Options/Line Spacing =>
themeEdit/Paragraph Options/Line Spacing value =>
themeEdit/Paragraph Options/Tab width =>
themeEdit/Paragraph Options/Indent 1st line =>
themeEdit/Paragraph Options/Spacing above =>
themeEdit/Paragraph Options/Spacing below =>
"""


class ViewsPage:

    def __init__(self, settings: Settings):
        self.settings = settings

        builder = Gtk.Builder()
        builder.add_from_file("ui/settings/views.glade")

        self.widget = builder.get_object("views_page")

        self.treeIconColor = builder.get_object("tree_icon_color")
        self.treeTextColor = builder.get_object("tree_text_color")
        self.treeBackgroundColor = builder.get_object("tree_background_color")
        self.treeIconSize: Gtk.Scale = builder.get_object("tree_icon_size")
        self.treeCharWordCounter: Gtk.ToggleButton = builder.get_object("tree_char_word_counter")
        self.treeFolders = {
            "itemCount": (builder.get_object("tree_folders_item_count"), "Count"),
            "wordCount": (builder.get_object("tree_folders_word_count"), "WC"),
            "charCount": (builder.get_object("tree_folders_char_count"), "CC"),
            "progress": (builder.get_object("tree_folders_progress"), "Progress"),
            "summary": (builder.get_object("tree_folders_summary"), "Summary"),
            "nothing": (builder.get_object("tree_folders_nothing"), "Nothing"),
        }
        self.treeText = {
            "wordCount": (builder.get_object("tree_text_word_count"), "WC"),
            "charCount": (builder.get_object("tree_text_char_count"), "CC"),
            "progress": (builder.get_object("tree_text_progress"), "Progress"),
            "summary": (builder.get_object("tree_text_summary"), "Summary"),
            "nothing": (builder.get_object("tree_text_nothing"), "Nothing"),
        }
        self.outlineIconColor = builder.get_object("outline_icon_color")
        self.outlineTextColor = builder.get_object("outline_text_color")
        self.outlineBackgroundColor = builder.get_object("outline_background_color")
        self.outlineVisibleColumns = {
            "title": (builder.get_object("outline_visible_title"), 0),
            "POV": (builder.get_object("outline_visible_pov"), 5),
            "label": (builder.get_object("outline_visible_label"), 7),
            "status": (builder.get_object("outline_visible_status"), 8),
            "compile": (builder.get_object("outline_visible_compile"), 9),
            "word count": (builder.get_object("outline_visible_word_count"), 11),
            "goal": (builder.get_object("outline_visible_goal"), 12),
            "percentage": (builder.get_object("outline_visible_percentage"), 13),
        }
        self.indexCardsColorsIconColor = builder.get_object("index_cards_colors_icon_color")
        self.indexCardsColorsTextColor = builder.get_object("index_cards_colors_text_color")
        self.indexCardsColorsBackgroundColor = builder.get_object("index_cards_colors_background_color")
        self.indexCardsColorsBorderColor = builder.get_object("index_cards_colors_border_color")
        self.indexCardsColorsCornerColor = builder.get_object("index_cards_colors_corner_color")
        self.indexCardsStyle = {
            "old": (builder.get_object("index_card_old_style"), "old"),
            "new": (builder.get_object("index_card_new_style"), "new")
        }
        self.indexCardsBackgroundColor: Gtk.ColorButton = builder.get_object("index_cards_background_color")
        self.indexCardsBackgroundImage: Gtk.FileChooser = builder.get_object("index_cards_background_image")

        # TODO : improve code (two references to self.<combo>)
        self.treeIconColor.set_active(self.findComboValueIndex(self.treeIconColor, settings.get(SettingsKeys.ViewSettings.Tree.ICON), 0))
        self.treeTextColor.set_active(self.findComboValueIndex(self.treeTextColor, settings.get(SettingsKeys.ViewSettings.Tree.TEXT), 0))
        self.treeBackgroundColor.set_active(self.findComboValueIndex(self.treeTextColor, settings.get(SettingsKeys.ViewSettings.Tree.BACKGROUND), 0))
        self.treeIconSize.set_value(settings.get(SettingsKeys.ViewSettings.Tree.ICON_SIZE))
        self.treeCharWordCounter.set_active(settings.get(SettingsKeys.COUNT_SPACES))
        self.setRadioButtonValue(self.treeFolders, settings.get(SettingsKeys.ViewSettings.Tree.INFO_FOLDER))
        self.setRadioButtonValue(self.treeText, settings.get(SettingsKeys.ViewSettings.Tree.INFO_TEXT))
        self.outlineIconColor.set_active(self.findComboValueIndex(self.outlineIconColor, settings.get(SettingsKeys.ViewSettings.Outline.ICON), 0))
        self.outlineTextColor.set_active(self.findComboValueIndex(self.outlineTextColor, settings.get(SettingsKeys.ViewSettings.Outline.TEXT), 0))
        self.outlineBackgroundColor.set_active(self.findComboValueIndex(self.outlineBackgroundColor, settings.get(SettingsKeys.ViewSettings.Outline.BACKGROUND), 0))
        outlineViewColumns = settings.get(SettingsKeys.OUTLINE_VIEW_COLUMNS)
        for key in self.outlineVisibleColumns:
            visibleColumnButton: Gtk.CheckButton = self.outlineVisibleColumns[key][0]
            visibleColumnValue: Gtk.CheckButton = self.outlineVisibleColumns[key][1]
            visibleColumnButton.set_active(visibleColumnValue in outlineViewColumns)
        self.indexCardsColorsIconColor.set_active(self.findComboValueIndex(self.indexCardsColorsIconColor, settings.get(SettingsKeys.ViewSettings.Cork.ICON), 0))
        self.indexCardsColorsTextColor.set_active(self.findComboValueIndex(self.indexCardsColorsTextColor, settings.get(SettingsKeys.ViewSettings.Cork.TEXT), 0))
        self.indexCardsColorsBackgroundColor.set_active(self.findComboValueIndex(self.indexCardsColorsBackgroundColor, settings.get(SettingsKeys.ViewSettings.Cork.BACKGROUND), 0))
        self.indexCardsColorsBorderColor.set_active(self.findComboValueIndex(self.indexCardsColorsBorderColor, settings.get(SettingsKeys.ViewSettings.Cork.BORDER), 0))
        self.indexCardsColorsCornerColor.set_active(self.findComboValueIndex(self.indexCardsColorsCornerColor, settings.get(SettingsKeys.ViewSettings.Cork.CORNER), 0))
        self.setRadioButtonValue(self.indexCardsStyle, settings.get(SettingsKeys.CORK_STYLE))
        rgba = Gdk.RGBA()
        if rgba.parse(settings.get(SettingsKeys.CorkBackground.COLOR)):
            self.indexCardsBackgroundColor.set_rgba(rgba)
        self.indexCardsBackgroundImage.set_filename(settings.get(SettingsKeys.CorkBackground.IMAGE))

        self.treeIconColor.connect("changed", self._treeIconColorChanged)        
        self.treeTextColor.connect("changed", self._treeTextColorChanged)
        self.treeBackgroundColor.connect("changed", self._treeBackgroundColorChanged)
        self.treeIconSize.connect("value-changed", self._treeIconSizeChanged)
        self.treeCharWordCounter.connect("toggled", self._treeCharWordCountToggled)
        self.connectRadioButton("toggled", self.treeFolders, self._treeFoldersToggled)
        self.connectRadioButton("toggled", self.treeText, self._treeTextToggled)
        self.outlineIconColor.connect("changed", self._outlineIconColorChanged)        
        self.outlineTextColor.connect("changed", self._outlineTextColorChanged)
        self.outlineBackgroundColor.connect("changed", self._outlineBackgroundColorChanged)
        for key in self.outlineVisibleColumns:
            visibleColumnButton: Gtk.CheckButton = self.outlineVisibleColumns[key][0]
            visibleColumnButton.connect("toggled", self._oulineVisibleColumnsToggled)
        self.indexCardsColorsIconColor.connect("changed", self._indexCardsColorsIconColorChanged)
        self.indexCardsColorsTextColor.connect("changed", self._indexCardsColorsTextColorChanged)
        self.indexCardsColorsBackgroundColor.connect("changed", self._indexCardsColorsBackgroundColorChanged)
        self.indexCardsColorsBorderColor.connect("changed", self._indexCardsColorsBorderColorChanged)
        self.indexCardsColorsCornerColor.connect("changed", self._indexCardsColorsCornerColorChanged)
        self.connectRadioButton("toggled", self.indexCardsStyle, self._indexCardsColorsStyleChanged)
        self.indexCardsBackgroundColor.connect("color-set", self._indexCardsBackgroundColorColorSet)
        self.indexCardsBackgroundImage.connect("file-set", self._indexCardsBackgroundImageFileSet)


    # TODO : externalise
    def findComboValueIndex(self, combobox: Gtk.ComboBox, value: str, column: int):
        model = combobox.get_model()

        for i, row in enumerate(model):
            if row[column] == value:
                return i
            
    # TODO : externalise
    def getComboSelectedValue(self, combobox: Gtk.ComboBox, column: int):
        tree_iter = combobox.get_active_iter()

        if tree_iter is None:
            return

        model = combobox.get_model()
        return model[tree_iter][column]

    # TODO : externalise
    def connectRadioButton(self, signal, radioButtons: dict, handler):
        for radioButton in radioButtons:
            radioWidget = radioButtons[radioButton][0]
            
            radioWidget.connect(signal, handler)

    # TODO : externalise
    def setRadioButtonValue(self, radioButtons: dict, value):
        
        for radioButton in radioButtons:
            radioWidget = radioButtons[radioButton][0]
            radioSettingsValue = radioButtons[radioButton][1]
            
            if radioSettingsValue==value:
                radioWidget.set_active(True)

    def _treeIconColorChanged(self, combo: Gtk.ComboBox):
        value = self.getComboSelectedValue(combo, 0)

        self.settings.set(SettingsKeys.ViewSettings.Tree.ICON, value)

    def _treeTextColorChanged(self, combo: Gtk.ComboBox):
        value = self.getComboSelectedValue(combo, 0)

        self.settings.set(SettingsKeys.ViewSettings.Tree.TEXT, value)

    def _treeBackgroundColorChanged(self, combo: Gtk.ComboBox):
        value = self.getComboSelectedValue(combo, 0)

        self.settings.set(SettingsKeys.ViewSettings.Tree.BACKGROUND, value)

    def _treeIconSizeChanged(self, scale: Gtk.Scale):
        self.settings.set(SettingsKeys.ViewSettings.Tree.ICON_SIZE, scale.get_value())

    def _treeCharWordCountToggled(self, toggleButton: Gtk.ToggleButton):
        self.settings.set(SettingsKeys.COUNT_SPACES, toggleButton.get_active())

    def _treeFoldersToggled(self, button):
        for radioButton in self.treeFolders:
            radioWidget = self.treeFolders[radioButton][0]
            radioSettingsValue = self.treeFolders[radioButton][1]

            if button==radioWidget:
                self.settings.set(SettingsKeys.ViewSettings.Tree.INFO_FOLDER, radioSettingsValue)

    def _treeTextToggled(self, button):
        for radioButton in self.treeText:
            radioWidget = self.treeText[radioButton][0]
            radioSettingsValue = self.treeText[radioButton][1]

            if button==radioWidget:
                self.settings.set(SettingsKeys.ViewSettings.Tree.INFO_TEXT, radioSettingsValue)

    def _outlineIconColorChanged(self, combo: Gtk.ComboBox):
        value = self.getComboSelectedValue(combo, 0)

        self.settings.set(SettingsKeys.ViewSettings.Outline.ICON, value)

    def _outlineTextColorChanged(self, combo: Gtk.ComboBox):
        value = self.getComboSelectedValue(combo, 0)

        self.settings.set(SettingsKeys.ViewSettings.Outline.TEXT, value)

    def _outlineBackgroundColorChanged(self, combo: Gtk.ComboBox):
        value = self.getComboSelectedValue(combo, 0)

        self.settings.set(SettingsKeys.ViewSettings.Outline.BACKGROUND, value)

    def _oulineVisibleColumnsToggled(self, checkbutton: Gtk.CheckButton):
        columns=[]
        for key in self.outlineVisibleColumns:
            visibleColumnButton: Gtk.CheckButton = self.outlineVisibleColumns[key][0]
            visibleColumnValue: Gtk.CheckButton = self.outlineVisibleColumns[key][1]
            if visibleColumnButton.get_active():
                columns.append(visibleColumnValue)
        
        self.settings.set(SettingsKeys.OUTLINE_VIEW_COLUMNS, columns)

    def _indexCardsColorsIconColorChanged(self, combo: Gtk.ComboBox):
        value = self.getComboSelectedValue(combo, 0)

        self.settings.set(SettingsKeys.ViewSettings.Cork.ICON, value)

    def _indexCardsColorsTextColorChanged(self, combo: Gtk.ComboBox):
        value = self.getComboSelectedValue(combo, 0)

        self.settings.set(SettingsKeys.ViewSettings.Cork.TEXT, value)

    def _indexCardsColorsBackgroundColorChanged(self, combo: Gtk.ComboBox):
        value = self.getComboSelectedValue(combo, 0)

        self.settings.set(SettingsKeys.ViewSettings.Cork.BACKGROUND, value)

    def _indexCardsColorsBorderColorChanged(self, combo: Gtk.ComboBox):
        value = self.getComboSelectedValue(combo, 0)

        self.settings.set(SettingsKeys.ViewSettings.Cork.BORDER, value)

    def _indexCardsColorsCornerColorChanged(self, combo: Gtk.ComboBox):
        value = self.getComboSelectedValue(combo, 0)

        self.settings.set(SettingsKeys.ViewSettings.Cork.CORNER, value)

    def _indexCardsColorsStyleChanged(self, button):
        for radioButton in self.indexCardsStyle:
            radioWidget = self.indexCardsStyle[radioButton][0]
            radioSettingsValue = self.indexCardsStyle[radioButton][1]

            if button==radioWidget:
                self.settings.set(SettingsKeys.CORK_STYLE, radioSettingsValue)

    # TODO : put in a library
    def rgba_to_hex(self, rgba):
        r = int(rgba.red * 255)
        g = int(rgba.green * 255)
        b = int(rgba.blue * 255)
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def _indexCardsBackgroundColorColorSet(self, button: Gtk.ColorButton):
        self.settings.set(SettingsKeys.CorkBackground.COLOR, self.rgba_to_hex(button.get_rgba()))

    def _indexCardsBackgroundImageFileSet(self, button: Gtk.FileChooser):
        self.settings.set(SettingsKeys.CorkBackground.IMAGE, button.get_filename())
