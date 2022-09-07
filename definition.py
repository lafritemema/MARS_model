
import abc
from typing import Dict, List

import model

from .movement import Movement
from .equipment import EquipmentI, Operation
from .reference import ReferenceI

class Definition(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def parse(serialize_definition: Dict):
        return

    @abc.abstractmethod
    def to_dict(self):
        return


class Path(Definition):

    """ Class used to represent a Movement
    """
    def __init__(self, uf: ReferenceI, ut: EquipmentI, movements: List[Movement]):
        """Movement object initializer

        Args:
            uf (int): user frame id
            ut (int): user tool id
            points (List[Point]): list of points describing the movement
        """
        self.__uf: ReferenceI = uf
        self.__ut: EquipmentI = ut
        self.__movements: List[Movement] = movements

    @property
    def user_tool(self) -> EquipmentI:
        return self.__ut

    @property
    def user_frame(self) -> ReferenceI:
        return self.__uf

    @property
    def movements(self) -> List[Movement]:
        return self.__movements

    @staticmethod
    def parse(serialize_movement: Dict) -> 'Path':
        # get the user tool from dict
        ut = serialize_movement['ut']
        # get the corresponding equipment
        ut = model.EQUIPMENT['EFFECTOR'][ut]

        # get the user frame from dict
        uf = serialize_movement['uf']
        # get the corresponding reference
        uf = model.REFERENCE['FRAME'][uf]

        movements = []

        for sp in serialize_movement['movements']:
            movements.append(Movement.parse(sp))

        return Path(uf, ut, movements)

    def to_dict(self):
        return { 
            "uf": self.__uf.name,
            "ut": self.__ut.name,
            "movements": [p.to_dict() for p in self.__movements]
        }

    def to_cmd_data(self) -> Dict:
        """build and return a dictionnary describing the path for commands generation

        Returns:
            Dict: dictionnary describing the path
        """
        # init list for setttings
        m_paras = []
        # init list for position
        m_positions = []
        
        # extract settings and position from movement list
        for movement in self.__movements:
            # get dict describing the movement
            mvt_cmd_def = movement.to_cmd_data()
            
            # insert parameters in m_para and position in m_positions
            m_paras.extend(mvt_cmd_def['parameters'])
            m_positions.append(mvt_cmd_def['position'])

        return {
            "uf": self.__uf.value,
            "ut": self.__ut.value,
            "movements": {
                "parameters": m_paras,
                "positions": m_positions
            }
        }

class Drilling(Definition):
    
    # TODO add other parameters in the futur: DrillingCycleLimit, ClampingCycleLimit, TemperatureAlarm, CurrentAlarm
    # update __init__ parse and to_dict

    """function to init Drilling operation object
    Args:
      speed (int): drill rotation speed in rpm
      feed (int) : drill feed in mm/tr
      peak_frequency (float): peak vibration frequency in Hz
      peak_amplitude (float): peak movement amplitude in mm
      clamp_weight (float): clampling weight in kg
      drill_thickness (float) : thickness of the hole in mm
    """
    def __init__(self,
                 speed:int,
                 feed:int,
                 peak_frequency:float,
                 peak_amplitude:float,
                 clamp_weight:float,
                 drill_thickness:float):
        self.__speed = speed
        self.__feed = feed
        self.__drill_thickness = drill_thickness
        self.__peak_frequency = peak_frequency
        self.__peak_amplitude = peak_amplitude
        self.__clamp_weight = clamp_weight

    @property
    def speed(self):
        return self.__speed
    
    @property
    def feed(self):
        return self.__feed

    @property
    def peak_amplitude(self):
        return self.__peak_amplitude
    
    @property
    def peak_frequency(self):
        return self.__peak_frequency
    
    @property
    def drill_thickness(self):
        return self.__drill_thickness

    @property
    def clamp_weight(self):
        return self.__clamp_weight

    @staticmethod
    def parse(serialize_definition:Dict):
    
        speed = serialize_definition['speed']
        feed = serialize_definition['feed']
        peak_frequency = serialize_definition['peak_frequency']
        peak_amplitude = serialize_definition['peak_amplitude']
        clamp_weight = serialize_definition['clamp_weight']
        drill_thickness = serialize_definition['drill_thickness']
        
        return Drilling(speed,
                        feed,
                        peak_frequency,
                        peak_amplitude,
                        clamp_weight,
                        drill_thickness)

    def to_dict(self):
        return {
            'speed' : self.__speed,
            'feed' : self.__feed,
            'peak_frequency' : self.__peak_frequency,
            'peak_amplitude' : self.__peak_amplitude,
            'clamp_weight' : self.__clamp_weight,
            'drill_thickness' : self.__drill_thickness
        }
        


class Probing(Definition):
    def __init__(self, ut:EquipmentI, uf:ReferenceI, movement:Movement):
        self.__uf: ReferenceI = uf
        self.__ut: EquipmentI = ut
        self.__movement:Movement = movement
    
    @property
    def user_tool(self):
        return self.__ut

    @property
    def user_frame(self):
        return self.__uf
    
    @property
    def movement(self):
        return self.__movement

    def parse(serialize_definition: Dict):
        try:
            ut = serialize_definition['ut']
            ut = model.EQUIPMENT['EFFECTOR'][ut]

            uf = serialize_definition['uf']
            uf = model.REFERENCE['FRAME'][uf]

            movement = Movement.parse(serialize_definition['movement'])
            return Probing(ut, uf, movement)
        except KeyError as error:
            raise 
    
    def to_dict(self):
        return {
            'ut': self.__ut.name,
            'uf': self.__uf.name,
            'movement': self.__movement.to_dict()
        }


class Manipulation(Definition):
    
    def __init__(self, manipulation_type:Operation, equipment:EquipmentI):
        self.__operation:Operation = manipulation_type
        self.__equipment:EquipmentI = equipment

    @property
    def operation(self) -> str:
        return self.__operation.name
    
    @property
    def equipment(self) -> EquipmentI:
        return self.__equipment

    @staticmethod
    def parse(manipulation_definition:Dict):
        eq_type = manipulation_definition['equipment']['type']
        eq_ref = manipulation_definition['equipment']['reference']
        operation = manipulation_definition['manipulation']

        equipement = model.EQUIPMENT[eq_type][eq_ref]

        manip_type = Operation[operation]

        return Manipulation(manip_type, equipement)

    def to_dict(self):
        return self.__operation.apply_on(self.__equipment)
    