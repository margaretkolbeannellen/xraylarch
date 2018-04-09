#!/usr/bin/env python
"""
Linear Combination panel
"""
import os
import time
import wx
import numpy as np

from functools import partial
from collections import OrderedDict

from wxutils import (SimpleText, pack, Button, HLine, Choice, Check,
                     GridPanel, CEN, RCEN, LCEN, Font)

from larch.utils import index_of
from larch.wxlib import BitmapButton, FloatCtrl
from larch_plugins.wx.icons import get_icon
from larch_plugins.xasgui.xas_dialogs import EnergyUnitsDialog
from larch_plugins.xafs.xafsutils import guess_energy_units
from larch_plugins.xafs.xafsplots import plotlabels

np.seterr(all='ignore')

PLOTOPTS_1 = dict(style='solid', linewidth=3, marker='None', markersize=4)
PLOTOPTS_2 = dict(style='short dashed', linewidth=2, zorder=3,
                  marker='None', markersize=4)
PLOTOPTS_D = dict(style='solid', linewidth=2, zorder=2,
                  side='right', marker='None', markersize=4)


PlotOne_Choices = OrderedDict((('Raw Data', 'mu'),
                               ('Normalized', 'norm'),
                               ('Derivative', 'dmude'),
                               ('Normalized + Derivative', 'norm+deriv'),
                               ('Flattened', 'flat'),
                               ('Pre-edge subtracted', 'preedge'),
                               ('Raw Data + Pre-edge/Post-edge', 'prelines'),
                               ('Deconvolved + Normalized', 'deconv+norm'),
                               ('Deconvolved', 'deconv')))

PlotSel_Choices = OrderedDict((('Raw Data', 'mu'),
                               ('Normalized', 'norm'),
                               ('Flattened', 'flat'),
                               ('Derivative', 'dmude')))

PlotOne_Choices_nonxas = OrderedDict((('Raw Data', 'mu'),
                                      ('Derivative', 'dmude'),
                                      ('Data + Derivative', 'norm+deriv')))

PlotSel_Choices_nonxas = OrderedDict((('Raw Data', 'mu'),
                                      ('Derivative', 'dmude')))



class LinearComboPanel(wx.Panel):
    """Liear Combination Panel"""
    def __init__(self, parent, controller=None, reporter=None, **kws):
        wx.Panel.__init__(self, parent, -1, **kws)
        self.parent = parent
        self.controller = controller
        self.reporter = reporter
        self.skip_process = False
        self.build_display()

    def onPanelExposed(self, **kws):
        # called when notebook is selected
        try:
            fname = self.controller.filelist.GetStringSelection()
            gname = self.controller.file_groups[fname]
            dgroup = self.controller.get_group(gname)
            self.fill_form(dgroup)
        except:
            pass

    def larch_eval(self, cmd):
        "eval"
        self.controller.larch.eval(cmd)

    def build_display(self):
        self.SetFont(Font(10))
        titleopts = dict(font=Font(11), colour='#AA0000')

        panel = GridPanel(self, ncols=4, nrows=4, pad=2, itemstyle=LCEN)

        panel.Add(SimpleText(panel, ' Linear Combination Fitting',
                           **titleopts), dcol=6)

        panel.pack()

    def fill_form(self, dgroup):
        """fill in form from a data group"""
        opts = self.get_config(dgroup)
        self.skip_process = True

#         widlist = (self.xas_e0, self.xas_step, self.xas_pre1,
#                    self.xas_pre2, self.xas_nor1, self.xas_nor2,
#                    self.xas_vict, self.xas_nnor, self.xas_showe0,
#                    self.xas_autoe0, self.xas_autostep,
#                    self.deconv_form, self.deconv_ewid)
#
#         if dgroup.datatype == 'xas':
#             for k in widlist:
#                 k.Enable()
#
#             self.plotone_op.SetChoices(list(PlotOne_Choices.keys()))
#             self.plotsel_op.SetChoices(list(PlotSel_Choices.keys()))
#
#             self.plotone_op.SetStringSelection(opts['plotone_op'])
#             self.plotsel_op.SetStringSelection(opts['plotsel_op'])
#             self.xas_e0.SetValue(opts['e0'])
#             self.xas_step.SetValue(opts['edge_step'])
#             self.xas_pre1.SetValue(opts['pre1'])
#             self.xas_pre2.SetValue(opts['pre2'])
#             self.xas_nor1.SetValue(opts['norm1'])
#             self.xas_nor2.SetValue(opts['norm2'])
#             self.xas_vict.SetSelection(opts['nvict'])
#             self.xas_nnor.SetSelection(opts['nnorm'])
#             self.xas_showe0.SetValue(opts['show_e0'])
#             self.xas_autoe0.SetValue(opts['auto_e0'])
#             self.xas_autostep.SetValue(opts['auto_step'])
#             self.deconv_form.SetStringSelection(opts['deconv_form'])
#             self.deconv_ewid.SetValue(opts['deconv_ewid'])
#         else:
#             self.plotone_op.SetChoices(list(PlotOne_Choices_nonxas.keys()))
#             self.plotsel_op.SetChoices(list(PlotSel_Choices_nonxas.keys()))
#             self.plotone_op.SetStringSelection('Raw Data')
#             self.plotsel_op.SetStringSelection('Raw Data')
#             for k in widlist:
#                 k.Disable()
#
#         self.skip_process = False
#         self.process(dgroup)

    def read_form(self):
        "read for, returning dict of values"
        form_opts = {}
        return form_opts

    def onPlotOne(self, evt=None):
        self.plot(self.controller.get_group())

    def onPlotSel(self, evt=None):
        newplot = True
        pass

    def onCopyParam(self, name=None, evt=None):
        conf = self.get_config()
        conf.update(self.read_form())
        opts = {}


    def on_selpoint(self, evt=None, opt='e0'):
        "on point selected by cursor"
        xval, _ = self.controller.get_cursor()
        if xval is None:
            return


    def process(self, dgroup, **kws):
        """ handle process of XAS data
        """
        if self.skip_process:
            return
        self.skip_process = True
        form = self.read_form()

    def get_plot_arrays(self, dgroup):
        form = self.read_form()


    def plot(self, dgroup, title=None, plot_yarrays=None, delay_draw=False,
             new=True, zoom_out=True, with_extras=True, **kws):

        print("plot")