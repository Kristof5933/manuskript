#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gdk
from rich import inspect

from manuskript.data import Settings, SettingsKeys
from manuskript.ui.util import rgbaFromHex, rgbaToHex


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
        self.textEditorColorsBackground: Gtk.ColorButton = builder.get_object("text_editor_colors_background")
        self.textEditorColorsForeground: Gtk.ColorButton = builder.get_object("text_editor_colors_foreground")
        self.textEditorColorsRestoreDefaults: Gtk.Button = builder.get_object("text_editor_colors_restore_defaults")
        self.textEditorFontFamily: Gtk.FontButton = builder.get_object("text_editor_font_family")
        self.textEditorFontSize: Gtk.SpinButton = builder.get_object("text_editor_font_size")
        self.textEditorMisspelled: Gtk.ColorButton = builder.get_object("text_editor_misspelled")
        self.textEditorTextAreaMaxWidth: Gtk.CheckButton = builder.get_object("text_editor_text_area_max_width")
        self.textEditorTextAreaWidth: Gtk.SpinButton = builder.get_object("text_editor_text_area_width")
        self.textEditorTextAreaTopBottomMargins: Gtk.SpinButton = builder.get_object("text_editor_text_area_top_bottom_margins")
        self.textEditorTextAreaLeftRightMargins: Gtk.SpinButton = builder.get_object("text_editor_text_area_left_right_margins")

        self.textEditorParagraphsAlignment: Gtk.ComboBox = builder.get_object("text_editor_paragraphs_alignment")
        self.textEditorParagraphsLineSpacing: Gtk.ComboBox = builder.get_object("text_editor_paragraphs_line_spacing")
        self.textEditorParagraphsLineSpacingProportional: Gtk.SpinButton = builder.get_object("text_editor_paragraphs_line_spacing_proportional")
        self.textEditorParagraphsTabWidth: Gtk.SpinButton = builder.get_object("text_editor_paragraphs_tab_width")
        self.textEditorParagraphsIndentFirstLine: Gtk.ToggleButton = builder.get_object("text_editor_paragraphs_indent_first_line")
        self.textEditorParagraphsSpacingAbove: Gtk.SpinButton = builder.get_object("text_editor_paragraphs_spacing_above")
        self.textEditorParagraphsSpacingBelow: Gtk.SpinButton = builder.get_object("text_editor_paragraphs_spacing_below")
        self.textEditorCursorBlockInsertion: Gtk.ToggleButton = builder.get_object("text_editor_cursor_block_insertion")
        self.textEditorCursorBlockInsertionSize: Gtk.SpinButton = builder.get_object("text_editor_cursor_block_insertion_size")
        self.textEditorCursorDisableBlinking: Gtk.ToggleButton = builder.get_object("text_editor_cursor_disable_blinking")
        self.textEditorCursorTypewriterMode: Gtk.ToggleButton = builder.get_object("text_editor_cursor_typewriter_mode")
        self.textEditorCursorFocusMode: Gtk.ComboBox = builder.get_object("text_editor_cursor_focus_mode")

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
        self.indexCardsBackgroundColor.set_rgba(rgbaFromHex(settings.get(SettingsKeys.CorkBackground.COLOR)))
        self.indexCardsBackgroundImage.set_filename(settings.get(SettingsKeys.CorkBackground.IMAGE))
        self.textEditorColorsBackground.set_rgba(rgbaFromHex(settings.get(SettingsKeys.TextEditor.BACKGROUND)))
        self.textEditorColorsForeground.set_rgba(rgbaFromHex(settings.get(SettingsKeys.TextEditor.FONT_COLOR)))
        self.textEditorFontFamily.set_font(self.extractFontName(settings.get(SettingsKeys.TextEditor.FONT)))
        self.textEditorFontSize.set_value(self.extractFontSize(settings.get(SettingsKeys.TextEditor.FONT)))
        self.textEditorMisspelled.set_rgba(rgbaFromHex(settings.get(SettingsKeys.TextEditor.MISSPELLED)))
        maxWidth=settings.get(SettingsKeys.TextEditor.MAX_WIDTH)
        self.textEditorTextAreaMaxWidth.set_active(maxWidth==0)
        self.textEditorTextAreaWidth.set_sensitive(maxWidth>0)
        self.textEditorTextAreaWidth.set_value(maxWidth)
        self.textEditorTextAreaTopBottomMargins.set_value(settings.get(SettingsKeys.TextEditor.MARGINS_TB))
        self.textEditorTextAreaLeftRightMargins.set_value(settings.get(SettingsKeys.TextEditor.MARGINS_LR))
        self.textEditorParagraphsAlignment.set_active(self.findComboValueIndex(self.textEditorParagraphsAlignment, settings.get(SettingsKeys.TextEditor.TEXT_ALIGNMENT), 3))
        spacingSetting=settings.get(SettingsKeys.TextEditor.LINE_SPACING)
        
        # Proportional spacing represents all possible values, but 100, 150 and 200.
        if spacingSetting in [100, 150, 200]:
            self.textEditorParagraphsLineSpacing.set_active(self.findComboValueIndex(self.textEditorParagraphsLineSpacing, spacingSetting, 1))
            self.textEditorParagraphsLineSpacingProportional.set_sensitive(False)
        else:
            self.textEditorParagraphsLineSpacing.set_active(self.findComboValueIndex(self.textEditorParagraphsLineSpacing, 0, 1))
            self.textEditorParagraphsLineSpacingProportional.set_sensitive(True)

        self.textEditorParagraphsLineSpacingProportional.set_value(settings.get(SettingsKeys.TextEditor.LINE_SPACING))
        self.textEditorParagraphsTabWidth.set_value(settings.get(SettingsKeys.TextEditor.TAB_WIDTH))
        self.textEditorParagraphsIndentFirstLine.set_active(settings.get(SettingsKeys.TextEditor.INDENT))
        self.textEditorParagraphsSpacingAbove.set_value(settings.get(SettingsKeys.TextEditor.SPACING_ABOVE))
        self.textEditorParagraphsSpacingBelow.set_value(settings.get(SettingsKeys.TextEditor.SPACING_BELOW))

        cursorBlockSize = settings.get(SettingsKeys.TextEditor.CURSOR_WIDTH)
        if cursorBlockSize == 1:
            self.textEditorCursorBlockInsertion.set_active(False)
            self.textEditorCursorBlockInsertionSize.set_sensitive(False)
            self.textEditorCursorBlockInsertionSize.set_value(9)
        else:
            self.textEditorCursorBlockInsertion.set_active(True)
            self.textEditorCursorBlockInsertionSize.set_sensitive(True)
            self.textEditorCursorBlockInsertionSize.set_value(cursorBlockSize)
        self.textEditorCursorDisableBlinking.set_active(settings.get(SettingsKeys.TextEditor.CURSOR_NOT_BLINKING))
        # Original manuskript discrepency, "always center" is used as "typewriter mode"
        self.textEditorCursorTypewriterMode.set_active(settings.get(SettingsKeys.TextEditor.ALWAYS_CENTER)) 
        self.textEditorCursorFocusMode.set_active(self.findComboValueIndex(self.textEditorCursorFocusMode, settings.get(SettingsKeys.TextEditor.FOCUS_MODE), 0))

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
        self.textEditorColorsBackground.connect("color-set", self._textEditorColorsBackgroundColorSet)
        self.textEditorColorsForeground.connect("color-set", self._textEditorColorsForegroundColorSet)
        self.textEditorColorsRestoreDefaults.connect("clicked", self._textEditorColorsRestoreDefaultsClicked)
        self.textEditorFontFamily.connect("font-set", self._textEditorFontFamilyFontSet)
        self.textEditorFontSize.connect("value-changed", self._textEditorFontSizeValueChanged)
        self.textEditorMisspelled.connect("color-set", self._textEditorMisspelledColorSet)
        self.textEditorTextAreaMaxWidth.connect("toggled", self._textEditorTextAreaMaxWidthToggled)
        self.textEditorTextAreaWidth.connect("value-changed", self._textEditorTextareaWidthValueChanged)
        self.textEditorTextAreaTopBottomMargins.connect("value-changed", self._textEditorTextAreaTopBottomMarginsValueChanged)
        self.textEditorTextAreaLeftRightMargins.connect("value-changed", self._textEditorTextAreaLeftRightMarginsValueChanged)
        self.textEditorParagraphsAlignment.connect("changed", self._textEditorParagraphsAlignmentChanged)
        self.textEditorParagraphsLineSpacing.connect("changed", self._textEditorParagraphsLineSpacingChanged)
        self.textEditorParagraphsLineSpacingProportional.connect("value-changed", self._textEditorParagraphsLineSpacingProportionalValueChanged)
        self.textEditorParagraphsTabWidth.connect("value-changed", self._standardSpinButtonValueChanged, SettingsKeys.TextEditor.TAB_WIDTH)
        self.textEditorParagraphsIndentFirstLine.connect("toggled", self._standardToggleButtonToggled, SettingsKeys.TextEditor.INDENT)
        self.textEditorParagraphsSpacingAbove.connect("value-changed", self._standardSpinButtonValueChanged, SettingsKeys.TextEditor.SPACING_ABOVE)
        self.textEditorParagraphsSpacingBelow.connect("value-changed", self._standardSpinButtonValueChanged, SettingsKeys.TextEditor.SPACING_BELOW)
        self.textEditorCursorBlockInsertion.connect("toggled", self._textEditorCursorBlockInsertionToggled, SettingsKeys.TextEditor.CURSOR_WIDTH)
        self.textEditorCursorBlockInsertionSize.connect("value-changed", self._standardSpinButtonValueChanged, SettingsKeys.TextEditor.CURSOR_WIDTH)
        self.textEditorCursorDisableBlinking.connect("toggled", self._standardToggleButtonToggled, SettingsKeys.TextEditor.CURSOR_NOT_BLINKING)
        self.textEditorCursorTypewriterMode.connect("toggled", self._standardToggleButtonToggled, SettingsKeys.TextEditor.ALWAYS_CENTER)
        self.textEditorCursorFocusMode.connect("changed", self._standardComboChanged, {'column': 0, 'settingsKey': SettingsKeys.TextEditor.FOCUS_MODE})

        print("done")


    # TODO : externalise
    def findComboValueIndex(self, combobox: Gtk.ComboBox, value: str, column: int):
        model = combobox.get_model()

        row: Gtk.TreeModelRow
        for i, row in enumerate(model):
            if row[column] == value:
                return i
        
        return None
            
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

    def _indexCardsBackgroundColorColorSet(self, button: Gtk.ColorButton):
        self.settings.set(SettingsKeys.CorkBackground.COLOR, rgbaToHex(button.get_rgba()))

    def _indexCardsBackgroundImageFileSet(self, button: Gtk.FileChooser):
        self.settings.set(SettingsKeys.CorkBackground.IMAGE, button.get_filename())

    def _textEditorColorsBackgroundColorSet(self, button: Gtk.ColorButton):
        self.settings.set(SettingsKeys.TextEditor.BACKGROUND, rgbaToHex(button.get_rgba()))

    def _textEditorColorsForegroundColorSet(self, button: Gtk.ColorButton):
        self.settings.set(SettingsKeys.TextEditor.FONT_COLOR, rgbaToHex(button.get_rgba()))

    def _textEditorColorsRestoreDefaultsClicked(self, button: Gtk.Button):
        backgroundColor="#ffffff"
        foregroundColor="#1a1a1a"
        self.settings.set(SettingsKeys.TextEditor.BACKGROUND, backgroundColor)
        self.settings.set(SettingsKeys.TextEditor.FONT_COLOR, foregroundColor)
        self.textEditorColorsBackground.set_rgba(rgbaFromHex(backgroundColor))
        self.textEditorColorsForeground.set_rgba(rgbaFromHex(foregroundColor))

    def extractFontName(self, fontString: str) -> str:
        parts = fontString.split(',')
        return parts[0]

    def extractFontSize(self, fontString: str) -> int:
        parts = fontString.split(',')
        return int(parts[1])

    def replaceFontName(self, fontString: str, newFontName: str) -> str:
        parts = fontString.split(',')
        parts[0] = newFontName
        return ','.join(parts)

    def replaceFontSize(self, fontString: str, newFontSize: int) -> str:
        parts = fontString.split(',')
        parts[1] = str(newFontSize)
        return ','.join(parts)
    
    def _textEditorFontFamilyFontSet(self, button: Gtk.FontButton):
        currentFont=self.settings.get(SettingsKeys.TextEditor.FONT)
        pangoFont=button.get_font_face()
        self.settings.set(SettingsKeys.TextEditor.FONT, self.replaceFontName(currentFont, str(pangoFont.get_family().get_name())))

    def _textEditorFontSizeValueChanged(self, button: Gtk.SpinButton):
        currentFont=self.settings.get(SettingsKeys.TextEditor.FONT)
        self.settings.set(SettingsKeys.TextEditor.FONT, self.replaceFontSize(currentFont, button.get_value_as_int()))

    def _textEditorMisspelledColorSet(self, button: Gtk.ColorButton):
        self.settings.set(SettingsKeys.TextEditor.MISSPELLED, rgbaToHex(button.get_rgba()))

    def _textEditorTextAreaMaxWidthToggled(self, button: Gtk.ToggleButton):
        if button.get_active():
            self.settings.set(SettingsKeys.TextEditor.MAX_WIDTH, 0)
            self.textEditorTextAreaWidth.set_sensitive(False)
        else:
            lastEditedValue=self.textEditorTextAreaWidth.get_value()

            if lastEditedValue==0.0:
                lastEditedValue=600.0

            self.settings.set(SettingsKeys.TextEditor.MAX_WIDTH, lastEditedValue)
            self.textEditorTextAreaWidth.set_value(lastEditedValue)
            self.textEditorTextAreaWidth.set_sensitive(True)

    def _textEditorTextareaWidthValueChanged(self, button: Gtk.SpinButton):
        self.settings.set(SettingsKeys.TextEditor.MAX_WIDTH, button.get_value_as_int())

    def _textEditorTextAreaTopBottomMarginsValueChanged(self, button: Gtk.SpinButton):
        self.settings.set(SettingsKeys.TextEditor.MARGINS_TB, button.get_value_as_int())

    def _textEditorTextAreaLeftRightMarginsValueChanged(self, button: Gtk.SpinButton):
        self.settings.set(SettingsKeys.TextEditor.MARGINS_LR, button.get_value_as_int())

    def _textEditorParagraphsAlignmentChanged(self, combo: Gtk.ComboBox):
        value = self.getComboSelectedValue(combo, 3)

        self.settings.set(SettingsKeys.TextEditor.TEXT_ALIGNMENT, value)

    def _textEditorParagraphsLineSpacingChanged(self, combo: Gtk.ComboBox):
        value = self.getComboSelectedValue(combo, 1)

        print(f"Value: {value}")
        
        if value!=0:
            self.settings.set(SettingsKeys.TextEditor.LINE_SPACING, value)
            self.textEditorParagraphsLineSpacingProportional.set_sensitive(False)
        else:
            self.settings.set(SettingsKeys.TextEditor.LINE_SPACING, self.textEditorParagraphsLineSpacingProportional.get_value_as_int())
            self.textEditorParagraphsLineSpacingProportional.set_sensitive(True)

    def _textEditorParagraphsLineSpacingProportionalValueChanged(self, button: Gtk.SpinButton):
        self.settings.set(SettingsKeys.TextEditor.LINE_SPACING, button.get_value_as_int())

    def _standardSpinButtonValueChanged(self, button: Gtk.SpinButton, settingsKey: str):
        self.settings.set(settingsKey, button.get_value_as_int())

    def _standardComboChanged(self, combo: Gtk.ComboBox, userData: dict):
        value = self.getComboSelectedValue(combo, userData["column"])
        self.settings.set(userData["settingsKey"], value)

    def _standardToggleButtonToggled(self, toggleButton: Gtk.ToggleButton, settingsKey: str):
        self.settings.set(settingsKey, toggleButton.get_active())

    def _textEditorCursorBlockInsertionToggled(self, button: Gtk.ToggleButton, settingsKey: str):
        if button.get_active():
            self.settings.set(settingsKey, self.textEditorCursorBlockInsertionSize.get_value_as_int())
            self.textEditorCursorBlockInsertionSize.set_sensitive(True)
        else:
            self.settings.set(settingsKey, 1)
            self.textEditorCursorBlockInsertionSize.set_sensitive(False)
