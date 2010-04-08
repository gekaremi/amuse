from amuse.legacy import *
from amuse.legacy.interface.gd import GravitationalDynamicsInterface
from amuse.legacy.interface.gd import GravitationalDynamics
from amuse.legacy.support.lit import LiteratureRefs

class OctgravInterface(LegacyInterface, LiteratureRefs, GravitationalDynamicsInterface):
    """
        .. [#] Gaburov, Nitadori, Harfst, Portegies Zwart & Makino,"A gravitational tree code on graphics processing units:
               Implementation in CUDA", in preparetion; and main MUSE paper, arXiv/0807.1996
    """

    include_headers = ['octgrav_code.h', 'parameters.h', 'worker_code.h', 'local.h']

    def __init__(self, convert_nbody = None, **kwargs):
        LegacyInterface.__init__(self, name_of_the_worker="worker_code", **kwargs)
        """
        self.parameters = parameters.Parameters(self.parameter_definitions, self)
        if convert_nbody is None:
            convert_nbody = nbody_system.nbody_to_si.get_default()

        self.convert_nbody = convert_nbody
        """
        LiteratureRefs.__init__(self)

    def setup_module(self):
        self.initialize_code()
        self.commit_parameters()
        self.commit_particles()

    def cleanup_module(self):
        self.cleanup_code()

class Octgrav(GravitationalDynamics):

    def __init__(self, convert_nbody = None):

        if convert_nbody is None:
            convert_nbody = nbody_system.nbody_to_si.get_default()


        legacy_interface = OctgravInterface()

        GravitationalDynamics.__init__(
            self,
            legacy_interface,
            convert_nbody,
        )

    def define_parameters(self, object):
        object.add_method_parameter(
            "get_eps2",
            "set_eps2",
            "epsilon_squared",
            "smoothing parameter for gravity calculations", 
            nbody_system.length * nbody_system.length, 
            0.3 | nbody_system.length * nbody_system.length
        )
        object.add_method_parameter(
            "get_time_step",
            None,
            "timestep",
            "constant timestep for iteration", 
            nbody_system.time, 
            0.7 | nbody_system.time
        )
        object.add_method_parameter(
            "get_theta_for_tree",
            "set_theta_for_tree",
            "openings_angle",
            "openings angle for building the tree between 0 and 1", 
            units.none,
            0.5 | units.none
        )
