#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Handy

from manuskript.data import Settings, SettingsKeys


class RevisionsPage:

    def __init__(self, settings: Settings):
        self.settings = settings

        builder = Gtk.Builder()
        builder.add_from_file("ui/settings/revisions.glade")

        self.widget = builder.get_object("revisions_page")

        self.revisionsKeep = builder.get_object("revisions_keep")
        self.revisionsSmartremove = builder.get_object("revisions_smartremove")
        self.revisionPerMinute = builder.get_object("revisions_per_minute")
        self.revisionPer10Minutes = builder.get_object("revisions_per_10_minutes")
        self.revisionPerHour = builder.get_object("revisions_per_hour")
        self.revisionPerDay = builder.get_object("revisions_per_day")
        self.revisionPerWeek = builder.get_object("revisions_per_week")

        self.revisionsKeep.set_active(self.settings.get(SettingsKeys.Revisions.KEEP))
        self.revisionsSmartremove.set_active(self.settings.get(SettingsKeys.Revisions.SMARTREMOVE))
        self.revisionPerMinute.set_value(self.settings.get(SettingsKeys.Revisions.Rules.DELAY_PER_MINUTE))
        self.revisionPer10Minutes.set_value(self.settings.get(SettingsKeys.Revisions.Rules.DELAY_PER_10_MINUTES))
        self.revisionPerHour.set_value(self.settings.get(SettingsKeys.Revisions.Rules.DELAY_PER_HOUR))
        self.revisionPerDay.set_value(self.settings.get(SettingsKeys.Revisions.Rules.DELAY_PER_DAY))
        self.revisionPerWeek.set_value(self.settings.get(SettingsKeys.Revisions.Rules.DELAY_PER_WEEK))

        self.revisionsKeep.connect("toggled", self._revisionsKeepToggled)
        self.revisionsSmartremove.connect("toggled", self._revisionsSmartremoveToggled)
        self.revisionPerMinute.connect("value-changed", self._revisionPerMinuteChanged)
        self.revisionPer10Minutes.connect("value-changed", self._revisionPer10MinutesChanged)
        self.revisionPerHour.connect("value-changed", self._revisionPerHourChanged)
        self.revisionPerDay.connect("value-changed", self._revisionPerDayChanged)
        self.revisionPerWeek.connect("value-changed", self._revisionPerWeekChanged)

    def _revisionsKeepToggled(self, button: Gtk.ToggleButton):
        self.settings.set(SettingsKeys.Revisions.KEEP, button.get_active())

    def _revisionsSmartremoveToggled(self, button: Gtk.ToggleButton):
        self.settings.set(SettingsKeys.Revisions.SMARTREMOVE, button.get_active())

    def _revisionPerMinuteChanged(self, button: Gtk.SpinButton):
        self.settings.set(SettingsKeys.Revisions.Rules.DELAY_PER_MINUTE, button.get_value_as_int())

    def _revisionPer10MinutesChanged(self, button: Gtk.SpinButton):
        self.settings.set(SettingsKeys.Revisions.Rules.DELAY_PER_10_MINUTES, button.get_value_as_int())

    def _revisionPerHourChanged(self, button: Gtk.SpinButton):
        self.settings.set(SettingsKeys.Revisions.Rules.DELAY_PER_HOUR, button.get_value_as_int())

    def _revisionPerDayChanged(self, button: Gtk.SpinButton):
        self.settings.set(SettingsKeys.Revisions.Rules.DELAY_PER_DAY, button.get_value_as_int())

    def _revisionPerWeekChanged(self, button: Gtk.SpinButton):
        self.settings.set(SettingsKeys.Revisions.Rules.DELAY_PER_WEEK, button.get_value_as_int())
