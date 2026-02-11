#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Handy

from manuskript.data import Settings, SettingsKeys
from manuskript.util import AppSettings, AppSettingsKeys


class GeneralPage:

    def __init__(self, settings: Settings):
        self.settings = settings

        builder = Gtk.Builder()
        builder.add_from_file("ui/settings/general.glade")

        self.appSettings = AppSettings()

        self.widget = builder.get_object("general_page")

        self.generalLanguage = builder.get_object("general_language")
        self.generalFontSize = builder.get_object("general_font_size")
        self.automaticLoad = builder.get_object("automatic_load")
        self.autoSave = builder.get_object("auto_save")
        self.autoSaveDelay = builder.get_object("auto_save_delay")
        self.autoSaveNoChanges = builder.get_object("auto_save_nochanges")
        self.autoSaveNoChangesDelay = builder.get_object("auto_save_nochanges_delay")
        self.saveOnQuit = builder.get_object("save_on_quit")
        self.saveToZip = builder.get_object("save_to_zip")

        self.generalLanguage.set_active(self.generalLanguageValueIndex(self.appSettings.getValue(AppSettingsKeys.GENERAL_LANGUAGE)))
        self.generalFontSize.set_value(self.appSettings.getValue(AppSettingsKeys.GENERAL_FONTSIZE))
        self.automaticLoad.set_active(self.appSettings.getValue(AppSettingsKeys.AUTOMATIC_LOAD))
        self.autoSave.set_active(self.settings.get(SettingsKeys.AUTO_SAVE))
        self.autoSaveDelay.set_value(self.settings.get(SettingsKeys.AUTO_SAVE_DELAY))
        self.autoSaveNoChanges.set_active(self.settings.get(SettingsKeys.AUTO_SAVE_NO_CHANGES))
        self.autoSaveNoChangesDelay.set_value(self.settings.get(SettingsKeys.AUTO_SAVE_NO_CHANGES_DELAY))
        self.saveOnQuit.set_active(self.settings.get(SettingsKeys.SAVE_ON_QUIT))
        self.saveToZip.set_active(self.settings.get(SettingsKeys.SAVE_TO_ZIP))

        self.generalLanguage.connect("changed", self._generalLanguageChanged)
        self.generalFontSize.connect("value-changed", self._generalFontSizeChanged)
        self.automaticLoad.connect("toggled", self._automaticLoadToggled)
        self.autoSave.connect("toggled", self._autoSaveToggled)
        self.autoSaveDelay.connect("value-changed", self._autoSaveChanged)
        self.autoSaveNoChanges.connect("toggled", self._autoSaveNoChangesToggled)
        self.autoSaveNoChangesDelay.connect("value-changed", self._autoSaveNoChangesChanged)
        self.saveOnQuit.connect("toggled", self._saveOnQuitToggled)
        self.saveToZip.connect("toggled", self._saveToZipToggled)

    def generalLanguageValueIndex(self, generalLanguage: str):
        model = self.generalLanguage.get_model()

        for i, row in enumerate(model):
            if row[0] == generalLanguage:
                return i

    def _generalLanguageChanged(self, combo: Gtk.ComboBox):
        tree_iter = combo.get_active_iter()

        if tree_iter is None:
            return

        model = combo.get_model()
        value = model[tree_iter][0]

        self.appSettings.setValue(AppSettingsKeys.GENERAL_LANGUAGE, value)

    def _generalFontSizeChanged(self, button: Gtk.SpinButton):
        self.appSettings.setValue(AppSettingsKeys.GENERAL_FONTSIZE, button.get_value())

    def _automaticLoadToggled(self, button: Gtk.ToggleButton):
        self.appSettings.setValue(AppSettingsKeys.AUTOMATIC_LOAD, button.get_active())

    def _autoSaveToggled(self, button: Gtk.ToggleButton):
        self.settings.set(SettingsKeys.AUTO_SAVE, button.get_active())

    def _autoSaveChanged(self, button: Gtk.SpinButton):
        self.settings.set(SettingsKeys.AUTO_SAVE_DELAY, button.get_value())

    def _autoSaveNoChangesToggled(self, button: Gtk.ToggleButton):
        self.settings.set(SettingsKeys.AUTO_SAVE_NO_CHANGES, button.get_active())

    def _autoSaveNoChangesChanged(self, button: Gtk.SpinButton):
        self.settings.set(SettingsKeys.AUTO_SAVE_NO_CHANGES_DELAY, button.get_value())

    def _saveOnQuitToggled(self, button: Gtk.ToggleButton):
        self.settings.set(SettingsKeys.SAVE_ON_QUIT, button.get_active())

    def _saveToZipToggled(self, button: Gtk.ToggleButton):
        self.settings.set(SettingsKeys.SAVE_TO_ZIP, button.get_active())
