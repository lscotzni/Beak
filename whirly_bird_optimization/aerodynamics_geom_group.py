from openmdao.api import Group, IndepVarComp, Problem
from lsdo_utils.api import PowerCombinationComp, ScalarExpansionComp

import numpy as np


class AerodynamicsGeomGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)
        self.options.declare('mode', types = str)


    def setup(self):
        shape = self.options['shape']
        # mode = self.options['mode']

        comp = IndepVarComp()
        comp.add_output('area')
        comp.add_output('AR')
        self.add_subsystem('inputs_comp', comp, promotes=['*'])

        # b = sqrt(AR * S)
        comp = PowerCombinationComp(
            shape=shape,
            out_name='wing_span',
            powers_dict=dict(
                AR=0.5,
                area=0.5,
            )
        )
        self.add_subsystem('wing_span_comp', comp, promotes=['*'])

        # c = b / AR
        oas_shape = (9,)
        comp = PowerCombinationComp(
            shape=shape,
            out_name='wing_chord',
            powers_dict=dict(
                AR=-1.,
                wing_span=1.,
            )
        )
        self.add_subsystem('wing_chord_comp', comp, promotes=['*'])

        comp = ScalarExpansionComp(
            shape=oas_shape,
            out_name='oas_wing_chord',
            in_name='wing_chord',
        )
        self.add_subsystem('oas_wing_chord_comp', comp, promotes=['*'])