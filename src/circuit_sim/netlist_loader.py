from src.circuit_sim.components import *
from src.circuit_sim.node import Node

class Netlist:
    """The default input is string which passed to Circuit class. For giving netlest as file
, write the file's name and its destination such as "C:\\Users\\username\\Desktop\\file.txt, For giving netlist in terminal,
set termianl parameter to any number"""

    def __init__(self, string : str | None = None, filename : str | None = None, terminal : int | None = None, nodes : list | None = None, elements : list | None = None):
        self.netlist = list()
        self.nodes = list()
        self.elements = list()
        if nodes and elements:
            self.elements = elements
            self.nodes = nodes
            self.netlist = [string]

        elif string:
               string = string.split("\n")
               self.netlist = string

        elif filename:
            with open(file=filename, mode='r') as f:
                while 1:
                    _temp = f.readline()
                    if _temp == "":
                        break
                    self.netlist.append(_temp)

        elif terminal is not None:
             while 1:
                  _temp = input("Write element's information:\t")

                  if _temp == 'end':
                       break

                  self.netlist.append(_temp)

        else:
             raise SyntaxError("Invalid input. Please write valid input")
        self.add_element()

    def add_element(self):
        for item in self.netlist:
            if item == "":
                continue
            
            _temp_element = None
            _info = item.split(' ')

            node1, node2 = Node(int(_info[1])), Node(int(_info[2]))
            if  not self.nodes:
                self.nodes.extend([node1, node2])
                
            else:
                flag = [False, False]
                for i in self.nodes:
                    if node1.number == i:
                        node1 = i
                        flag[0] = True
                    if node2.number == i:
                        node2 = i
                        flag[1] = True
                if flag[0] == False:
                    self.nodes.append(node1)
                if flag[1] == False:
                    self.nodes.append(node2)

            if item[0] == 'R':
                _temp_element = Resistor(_info[0], node1, node2, int(_info[3]))
                self.elements.append(_temp_element)

            elif item[0] == 'I' or item[0] == 'V':

                match _info[3]:
                    case 'DC':
                        _temp_element = CurrentSource(_info[0], node1, node2, int(_info[4])) if item[0] == 'I' else VoltageSource(_info[0], node1, node2, int(_info[4]))            
                        self.elements.append(_temp_element)

                    case 'AC':
                        pass

                    case 'TR':
                        pass

            elif item[0] == 'L' or item[0] == 'C':

                if len(_info) == 4:
                    _temp_element = Capacitor(_info[0], node1, node2, int(_info[3])) if item[0] == 'C' else Inductor(_info[0], node1, node2, int(_info[3]))
                    self.elements.append()

                else:
                    _temp_element = Capacitor(_info[0], node1, node2, int(_info[3]), int(_info[4])) if item[0] == 'C' else Inductor(_info[0], node1, node2, int(_info[3]), int(_info[4]))
                    self.elements.append(_temp_element)
            
            node1.add_element(_temp_element)
            node2.add_element(_temp_element)
