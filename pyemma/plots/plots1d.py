
# This file is part of PyEMMA.
#
# Copyright (c) 2018 Computational Molecular Biology Group, Freie Universitaet Berlin (GER)
#
# PyEMMA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import


import numpy as _np

__author__ = 'thempel'


def plot_feature_histograms(xyzall, feature_labels=None, ax=None, ylog=False, outfile=None, n_bins=50, **kwargs):
    r"""Feature histogram plot

    Parameters
    ----------
    xyzall : (Concatenated list of) input features; np.array containing time series data to be plotted.
    feature_labels : Labels of histogrammed features. Either list of strings or pyemma Featurizer object.
    ax : matplotlib Axes object, optional, default = None
        the axes to plot to. When set to None the default Axes object will be used.
    ylog : If True, plot logarithm of histogram values.
    n_bins : Number of bins the histogram uses.
    outfile : If not None, saves plot to this file. 
    **kwargs: Will be parsed to pyplot.plo when plotting the MLE datapoints (not the bootstrapped means).
            See the doc of pyplot for more options. Most useful lineproperties like `marker='o'` and/or :markersize=5

    Returns
    -------
    ax : Axes object containing the plot

    """

    if not isinstance(xyzall, _np.ndarray):
        raise UserWarning('Input data hast to be a numpy array. Did you concatenate your data?')

    if xyzall.shape[1] > 50:
        raise NotImplementedError('This function only works for a finite number of dimensions.')

    if feature_labels is not None:
        if not isinstance(feature_labels, list):
            from pyemma.coordinates.data.featurization.featurizer import MDFeaturizer as _MDFeaturizer
            if isinstance(feature_labels, _MDFeaturizer):
                feature_labels = feature_labels.describe()
            else:
                raise UserWarning('feature_labels must be a list of feature labels or a pyemma featurizer object!')
        if not xyzall.shape[1] == len(feature_labels):
            raise UserWarning('feature_labels must have the same dimension as the input data xyzall.')

    import matplotlib.pyplot as _plt
    # check input
    if ax is None:
        ax = _plt.gca()
    hist_offset = -.2
    for h, coordinate in enumerate(xyzall.T):
        hist, edges = _np.histogram(coordinate, bins=n_bins)
        if not ylog:
            y = hist / hist.max()
        else:
            y = _np.log(hist) / _np.log(hist).max()
        ax.fill_between(edges[:-1], y + h + hist_offset, color='b', y2=h + hist_offset, alpha=.25, **kwargs)
        ax.axhline(y=h + hist_offset, xmin=0, xmax=1, color='k', linewidth=.2)
    ax.set_ylim(hist_offset, h + hist_offset + 1)

    # formatting
    if feature_labels is not None:
        ax.set_yticks(_np.array(range(len(feature_labels))) + .3)
        ax.set_yticklabels(feature_labels);
    else:
        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.set_ylabel('Feature histograms')
    ax.set_xlabel('Feature values');

    # show or save
    # if outfile is None:
    #    _plt.show()
    if outfile is not None:
        _plt.savefig(outfile)
    return ax
