#!/usr/bin/env python
# --!-- coding: utf8 --!--

from enum import Enum, unique
from manuskript.data.signals import Signals
import hashlib

@unique
class DataStatus(Enum):
    UNDEFINED = 0
    CHANGED = 1
    LOADING = 2
    LOADED = 3
    SAVING = 4
    SAVED = 5


class AbstractData:

    def __init__(self, path: str):
        self.dataPath = path
        self.dataStatus = DataStatus.UNDEFINED
        self.signals = Signals.getCommonInstance()
        self.fieldChecksums = {}

    def changePath(self, path: str):
        print("{} -> {}".format(self.dataPath, path))

        self.dataPath = path

    def complete(self, statusCompletion: bool = True):
        if self.dataStatus == DataStatus.LOADING:
            self.dataStatus = DataStatus.LOADED if statusCompletion else DataStatus.UNDEFINED
        elif self.dataStatus == DataStatus.SAVING:
            self.dataStatus = DataStatus.SAVED

    def load(self):
        self.dataStatus = DataStatus.LOADING
        self.fieldChecksums = {}

    def save(self):
        self.dataStatus = DataStatus.SAVING
        self.fieldChecksums = {}

    def __checksum(self, data):
        b = repr(data).encode('utf-8')
        return hashlib.blake2b(b, digest_size=16).hexdigest()
    
    def _updateFieldNotifyOnChange(self, attributeName: str, newValue):
        key = f"{self.__class__.__name__}.{attributeName}"

        oldValue = getattr(self, attributeName)

        if oldValue == newValue:
            return

        setattr(self, attributeName, newValue)

        originalChecksum = self.fieldChecksums.get(key)

        if originalChecksum is None:
            self.fieldChecksums[key] = self.__checksum(oldValue)

        elif originalChecksum == self.__checksum(newValue):
            self.fieldChecksums.pop(key)

        print(f"{key}")

        userData = {'sender': self.__class__.__name__, 'isDirty': bool(self.fieldChecksums)}

        self.signals.emit("data-content-changed", userData)

    def notifyDataChanged(self):
        # checksum = self.__checksum(data)
        # if not key in self.dataChanges:
        #     self.dataChanges[key] = checksum 
        #     print(f"{self.dataChanges[key]}")
        # else:
        #     if self.dataChanges[key] == checksum:
        #         print("Reverted !")
        
        self.signals.emit("data-content-changed")
