from src.circuit_sim.components import *
from src.circuit_sim.node import Node

class NetlistLoader:
    """The default input is string which passed to Circuit class. For giving netlest as file
, write the file's name and its destination such as "C:\Users\username\Desktop\file.txt, For giving netlist in terminal,
set termianl parameter to any number"""

    def __init__(self, string : str | None = None, filename = None , terminal : int | None = None):
        self.netlist = list()
        self.nodes = list()
        self.elements = dict()

        if string:
               string = string.split("\n")
               self.netlist = string
        elif filename:
            with open(file=filename, mode='r') as f:
                 pass
        elif terminal is not None:
             self.netlist = list()
             while 1:
                  _temp = input("Write element's information:\t")

                  if _temp == 'end':
                       break

                  self.netlist.append(_temp)
        else:
             raise SyntaxError("Invalid input. Please write valid input")

    def add_element(self):
        for i in self.netlist:
            if i[0] == 'R':
                _info = i.split(' ')
                self.elements.update({_info[0] : Resistor(_info[0], int(_info[1]), int(_info[2]), int(_info[3]))})

            elif i[0] == 'I' or i[0] == 'V':
                _info = i.split(' ')

                match _info[3][0]:
                    case 'D':
                        self.elements.update({_info[0] : CurrentSource(_info[0], int(_info[1]), int(_info[2]), int(_info[4])) if i[0] == 'I' else VoltageSource(_info[0], int(_info[1]), int(_info[2]), int(_info[4]))})

                    case 'A':
                        pass

                    case 'S':
                        pass

            elif i[0] == 'L' or i[0] == 'C':
                _info = i.split(' ')

                if len(_info) == 4:
                    self.elements.update({_info[0] : Capacitor(_info[0], int(_info[1]), int(_info[2]), int(_info[3])) if i[0] == 'I' else Inductor(_info[0], int(_info[1]), int(_info[2]), int(_info[3]))})

                else:
                    self.elements.update({_info[0] : Capacitor(_info[0], int(_info[1]), int(_info[2]), int(_info[3]), int(_info[4])) if i[0] == 'I' else Inductor(_info[0], int(_info[1]), int(_info[2]), int(_info[3]), int(_info[4]))})

    def add_node(self):
        for i in self.netlist:
            i.split(' ')
            if i[1] not in self.nodes:
                self.nodes.append(Node(int(i[1])))
            if i[2] not in self.nodes:
                self.nodes.append(Node(int(i[2])))
