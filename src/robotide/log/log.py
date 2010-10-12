#  Copyright 2008-2010 Nokia Siemens Networks Oyj
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

from robotide.pluginapi import Plugin, ActionInfo, RideLogMessage
from robotide.context.font import Font


class LogPlugin(Plugin):
    """Viewer for internal log messages."""
    
    def __init__(self, app):
        Plugin.__init__(self, app)
        self._log = []
        self._window = None

    def enable(self):
        self._create_menu()
        self.subscribe(self._log_message, RideLogMessage)

    def disable(self):
        self.unsubscribe_all()
        self.unregister_actions()
        if self._window:
            self._window.close(self.notebook)

    def _create_menu(self):
        self.unregister_actions()
        self.register_action(ActionInfo('Tools', 'View RIDE Log',
                                        self.OnViewLog))

    def _log_message(self, log_event):
        self._log.append(log_event)
        if self._window:
            self._window.update_log()

    def OnViewLog(self, event):
        if not self._window:
            self._window = _LogWindow(self.notebook, self._log)
            self._window.update_log()
        else:
            self.notebook.show_tab(self._window)


class _LogWindow(wx.TextCtrl):

    def __init__(self, notebook, log):
        wx.TextCtrl.__init__(self, notebook, style=wx.TE_READONLY | wx.TE_MULTILINE)
        self._log = log
        self._create_ui()
        self._add_to_notebook(notebook)
        self.SetFont(Font().fixed_log)

    def _create_ui(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self)
        self.SetSizer(sizer)

    def _add_to_notebook(self, notebook):
        notebook.add_tab(self, 'Log', allow_closing=True)
        notebook.show_tab(self)

    def close(self, notebook):
        notebook.delete_tab(self)

    def update_log(self):
        self.SetValue(self._decode_log(self._log))

    def _decode_log(self, log):
        result = ''
        for msg in log:
            result += '%s [%s]: %s\n\n' % (msg.timestamp, msg.level, msg.message)
        return result