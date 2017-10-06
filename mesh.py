import numpy as np

def mesh_gen(cells):
  xx = np.linspace(0, 10, cells+1)#.reshape(cells, 1)
  XY = np.zeros((cells+1, cells+1, 2))
  for i in range(cells+1):
    for j in range(cells+1):
        XY[i, j, 0] = xx[i]
        XY[i, j, 1] = xx[j]
  return XY

class Cell(object):
  """ A single cell in the mesh, holds location and material data """

  def __init__(self, index, mesh_params, mat_map=None):
    """ Cell constructor, give index in a tuple (i,j) """
    
    # Constructor validations
    assert isinstance(index, tuple), "Index must be a tuple"
    assert len(index) == 2, "Index must be a length 2 tuple"
    
    try:
      assert mesh_params['cell_length'] > 0, "cell_length must be greater than 0"
    except KeyError:
      raise KeyError("Missing 'cell_length' parameter in mesh_params")
    
    self._index  = index

    try:
      self._length = float(mesh_params['cell_length'])
      self._area   = np.power(self._length, 2)
    except ValueError:
      raise TypeError("cell_length parameter must be a number")

    # Calculate global_idx
    x_node = mesh_params['x_cell'] + 1
    i,j = index[0], index[1]
    self._global_idx = [x_node*i + j,
                        x_node*i + j + 1,
                        x_node*(i + 1) + j,
                        x_node*(i + 1) + j + 1]
    
    # Get material properties
    if mat_map:
      self._mat_map = mat_map

    # Determine if on a boundary
    self._bounds = {}
    x_cell = mesh_params['x_cell']
    try:
      y_cell = mesh_params['y_cell']
    except KeyError:
      y_cell = x_cell
   
    if index[0] == 0:
      self._bounds.update({'x_min': None})
    if index[0] == y_cell:
      self._bounds.update({'x_max': None})
    if index[1] == 0:
      self._bounds.update({'y_min': None})
    if index[1] == x_cell:
      self._bounds.update({'y_max': None})


  # UTILITY FUNCTIONS ================================================

  # MATERIAL PROPERTIES  ==============================================
  def get(self, prop):
    try:
      x = self._length*(self._index[0] + 0.5)
      y = self._length*(self._index[1] + 0.5)
    
      return self._mat_map.get(prop, loc=(x,y))
    except AttributeError:
      raise AttributeError("This cell has no material map assigned")

  
  # ATTRIBUTES  =======================================================
    
  def area(self):
    return self._area
  
  def bounds(self, bound=None, value=None):
    if bound and bound in self._bounds:
      if value:
        self._bounds[bound] = value
      else:
        return self._bounds[bound]
    elif bound and not bound in self._bounds:
      raise KeyError("Cell does not have bound " + str(bound))
    else:
      return self._bounds    
  
  def global_idx(self):
    """ Returns global index, a list of the node indices """
    return self._global_idx

  def index(self):
    return self._index
  
  def length(self):
    return self._length
