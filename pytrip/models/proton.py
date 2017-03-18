#
#    Copyright (C) 2010-2016 PyTRiP98 Developers.
#
#    This file is part of PyTRiP98.
#
#    PyTRiP98 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PyTRiP98 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PyTRiP98.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Collection of proton RBE models.

[1] A. Carabe, M. Moteabbed, N. Depauw, J. Schuemann, and H. Paganetti,
"Range uncertainty in proton therapy due to variable biological effectiveness,"
Phys. Med. Biol. 57(5), 1159–1172 (2012).
https://doi.org/10.1088/0031-9155/57/5/1159

[2] M. Wedenberg, B. Lind, and B. Haardemark,
"A model for the relative biological effectiveness of protons:
The tissue specific parameter alpha/beta of photons is a predictor for the sensitivity to LET changes,"
Acta Oncol. 52(3), 580–588 (2013).
http://dx.doi.org/10.3109/0284186X.2012.705892

[3]  A. L. McNamara, J. Schuemann, and H. Paganetti,
"A phenomenological relative biological effectiveness (RBE) model for proton therapy based on all published
in vitro cell survival data,"
Phys. Med. Biol. 60(21), 8399–8416
https://doi.org/10.1088/0031-9155/60/21/8399
"""

import numpy as np
import logging

logger = logging.getLogger(__name__)


def rbe_carabe(dose, let, abx):
    """
    Carabe proton RBE model

    input parameters may be either numpy.array or scalars
    TODO: handle Cube() class directly

    :params dose: physical proton dose in [Gy]
    :params let: LET in [keV/um]
    :params abx: alpha_x / beta_x [Gy^-1]

    :returns: RBE for the given parameters

    :ref: https://doi.org/10.1088/0031-9155/57/5/1159
    """

    _labx = 2.686 * let / abx
    _apx = 0.843 + 0.154 * _labx
    _bpx = 1.090 + 0.006 * _labx
    _bpx *= _bpx

    rbe = _rbe_apx(dose, _apx, _bpx, abx)
    return rbe


def rbe_wedenberg(dose, let, abx):
    """
    Wedenberg proton RBE model

    input parameters may be either numpy.array or scalars
    TODO: handle Cube() class directly

    :params dose: physical proton dose in [Gy]
    :params let: LET in [keV/um]
    :params abx: alpha_x / beta_x [Gy^-1]

    :returns: RBE for the given parameters

    :ref: http://dx.doi.org/10.3109/0284186X.2012.705892
    """

    _apx = 1.000 + 0.434 * let / abx
    _bpx = 1.000

    rbe = _rbe_apx(dose, _apx, _bpx, abx)
    return rbe


def rbe_mcnamara(dose, let, abx):
    """
    McNamara proton RBE model

    input parameters may be either numpy.array or scalars
    TODO: handle Cube() class directly

    :params dose: physical proton dose in [Gy]
    :params let: LET in [keV/um]
    :params abx: alpha_x / beta_x [Gy^-1]

    :returns: RBE for the given parameters

    :ref: https://doi.org/10.1088/0031-9155/60/21/8399
    """

    _apx = 0.999064 + 0.35605 * let / abx
    _bpx = 1.1012 - 0.0038703 * np.sqrt(abx) * let
    _bpx *= _bpx

    rbe = _rbe_apx(dose, _apx, _bpx, abx)
    return rbe


def _rbe_apx(dose, apx, bpx, abx):
    """
    :params dose: proton dose
    :params apx: alpha_p / alpha_x
    :params bpx: beta_p / beta_x
    :params abx: alpha_x / beta_x
    """

    rbe = np.sqrt(abx*abx + 4*apx*abx*dose + 4*bpx*dose*dose - abx) / (2 * dose)
    return rbe