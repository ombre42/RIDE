#  Copyright 2008-2012 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import wx

from robotide.preferences import PreferencesPanel, PreferencesColorPicker
from robotide.preferences.saving import IntegerChoiceEditor


class ColorPreferences(PreferencesPanel):
    location = ("Grid Colors and Font Size",)
    title = "Grid Colors and Font Size"


    def __init__(self, settings, *args, **kwargs):
        super(ColorPreferences, self).__init__(*args, **kwargs)
        self._settings = settings
        # N.B. There really ought to be a "reset colors to defaults"
        # button, in case the user gets things hopelessly mixed up

        # what would make this UI much more usable is if there were a
        # preview window in the dialog that showed all the colors. I
        # don't have the time to do that right now, so this will have
        # to suffice.

        font_size_sizer = self._create_font_size_sizer(settings)
        colors_sizer = self._create_colors_sizer()
        main_sizer = wx.FlexGridSizer(rows=2, cols=1, hgap=10)
        main_sizer.Add(font_size_sizer)
        main_sizer.Add(colors_sizer)
        self.SetSizer(main_sizer)

    def _create_font_size_sizer(self, settings):
        f = IntegerChoiceEditor(settings,
            'font size',
            'Grid Font Size',
            [str(i) for i in range(8, 49)]
        )
        font_size_sizer = wx.FlexGridSizer(rows=1, cols=1)
        font_size_sizer.AddMany([f.label(self), (f.chooser(self),)])
        return font_size_sizer

    def _create_colors_sizer(self):
        colors_sizer = wx.GridBagSizer()
        self._create_foreground_pickers(colors_sizer)
        self._create_background_pickers(colors_sizer)
        return colors_sizer

    def _create_foreground_pickers(self, colors_sizer):
        row = 0
        for key, label in (
            ("text user keyword", "User Keyword Foreground"),
            ("text library keyword", "Library Keyword Foreground"),
            ("text commented", "Comments Foreground"),
            ("text variable", "Variable Foreground"),
            ("text string", "Default Foreground"),
            ("text empty", "Empty Foreground"),
            ):
            lbl = wx.StaticText(self, wx.ID_ANY, label)
            btn = PreferencesColorPicker(self, wx.ID_ANY, self._settings["Colors"], key)
            colors_sizer.Add(btn, (row, 0), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
            colors_sizer.Add(lbl, (row, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=4)
            row += 1

    def _create_background_pickers(self, colors_sizer):
        row = 0
        for key, label in (
            ("background assign", "Variable Background"),
            ("background keyword", "Keyword Background"),
            ("background mandatory", "Mandatory Field Background"),
            ("background optional", "Optional Field Background"),
            ("background must be empty", "Mandatory Empty Field Background"),
            ("background unknown", "Unknown Background"),
            ("background error", "Error Background"),
            ("background highlight", "Highlight Background")
            ):
            lbl = wx.StaticText(self, wx.ID_ANY, label)
            btn = PreferencesColorPicker(self, wx.ID_ANY, self._settings["Colors"], key)
            colors_sizer.Add(btn, (row, 2), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
            colors_sizer.Add(lbl, (row, 3), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=4)
            row += 1
