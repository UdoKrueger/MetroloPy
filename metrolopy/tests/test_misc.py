# -*- coding: utf-8 -*-

# module test_misc

# Copyright (C) 2019 National Research Council Canada
# Author:  Harold Parks

# This file is part of MetroloPy.

# MetroloPy is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software 
# Foundation, either version 3 of the License, or (at your option) any later 
# version.

# MetroloPy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more 
# details.

# You should have received a copy of the GNU General Public License along with 
# MetroloPy. If not, see <http://www.gnu.org/licenses/>.
"""
Check that known bugs are fixed.
"""

import metrolopy as uc
import numpy as np

def test_reduce():
    a = uc.gummy(12.367,0.22,unit='mm/m')
    a.reduce_unit()
    assert abs(a.x - 0.012367) < 1e-15
    assert abs(a.u - 0.00022) < 1e-15
    assert a.unit is uc.one
    
def test_zero_derivative():
    u = 0.00223
    a = uc.gummy(0,u)
    b = a**2
    
    assert b.u == 0
    b.sim()
    assert abs((np.sqrt(2)*u**2-b.usim)/b.usim) < 0.1
    b.style = 'pmsim'
    assert '?' not in b.tostring()
    
def test_triangular(plot=False):
    a = uc.gummy(uc.TriangularDist(1,1))
    a.sim()
    assert abs((a.usim - 1/np.sqrt(6))/a.usim) < 0.1
    if plot:
        print('This should be a triangle with mode 1, lower limit 0 and upper limit 1:')
        a.hist()
        
    a = uc.gummy(uc.TriangularDist(-2.5,left_width=0.5,right_width=1.5))
    a.sim()
    if plot:
        print('this should be a triangle with mode -2.5, lower limit -3 and upper limit -1:')
        a.hist()
        
    a = uc.gummy(uc.TriangularDist(1,lower_limit=0.5,upper_limit=1.5))
    a.sim()
    if plot:
        print('this should be a triangle with mode 1, lower limit 0.5 and upper limit 1.5:')
        a.hist()
        
def test_zero_degc():
    a = uc.gummy(0, 0.15,unit='degC')
    a.style='xf'
    assert a.tostring() == '0.00'
    
def test_ufrom_multiletter():
    a = uc.gummy(10.0, 1, utype='A')
    b = uc.gummy(20.0, 2, utype='DUT')
    y = a - b
    assert abs(y.ufrom('A') - 1) < 1e-15
    assert abs(y.ufrom('DUT') - 2) < 1e-15