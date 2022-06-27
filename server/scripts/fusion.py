# fusion.py
#
# This script provides a class for fusion.
# We will expect an input from emonet and audioprocess.

import math

class fusion:
  emojimap = {(-0.83333, 0.58333): '0x1f620', 
              (-0.5, 0.16667): '0x1f627', 
		  (-0.83333, 0.5): '0x1f630', 
              (-0.0, 0.66667): '0x1f632', 
              (0.66667, 0.58333): '0x1f601', 
              (-0.58333, 0.16667): '0x1f616', 
              (-0.33333, -0.25): '0x1f615', 
              (-0.58333, -0.08333): '0x1f622', 
              (-0.58333, -0.41667): '0x1f61e', 
              (-0.5, -0.08333): '0x1f635', 
              (-0.58333, -0.33333): '0x1f613',
              (0.33333, -0.41667): '0x1f924', 
              (-0.41667, -0.16667): '0x1f611',
              (0.5, 0.41667): '0x1f618', 
              (-0.5, -0.33333): '0x1F62E', 
              (0.16667, 0.16667): '0x1f979', 
              (0.66667, 0.33333): '0x1f60b', 
              (-0.75, 0.91667): '0x1f631', 
              (-1.0, 0.75): '0x1f92e', 
              (-0.5, 0.0): '0x1fae4', 
              (-0.08333, 0.08333): '0x1f92d',
              (-0.08333, 0.33333): '0x1f62e', 
              (0.25, 0.08333): '0x1fae3', 
              (-0.16667, -0.0): '0x1f928',
              (-0.33333, -0.41667): '0x1f644',
              (-0.66667, -0.33333): '0x1F635', 
              (-0.5, 0.66667): '0x1f624', 
              (-1.0, 0.91667): '0x1f92c', 
              (0.91667, 0.83333): '0x1f602', 
              (-0.58333, 0.66667): '0x1f628', 
              (-0.25, 0.41667): '0x1f621', 
              (-0.58333, -0.16667): '0xFE0F', 
              (-0.5, 0.33333): '0x1f62c', 
              (0.75, 0.58333): '0x1f604', 
              (0.08333, 0.08333): '0x1f605', 
              (0.5, -0.0): '0x1f600', 
              (0.66667, 0.66667): '0x1f606',
              (0.83333, 0.41667): '0x1f917', 
              (-0.08333, 0.5): '0x1f62f',
              (0.66667, 0.5): '0x1f61a',
              (0.58333, 0.16667): '0x1f619',
              (0.41667, 0.0): '0x263A', 
              (-0.83333, 0.83333): '0x1f62d',
              (-0.41667, -0.08333): '0x1F926', 
              (-0.66667, -0.5): '0x1f922',
              (0.5, 0.08333): '0x1f913',
              (0.83333, 0.83333): '0x1f973', 
              (-0.41667, -0.58333): '0x1f614', 
              (-0.5, 0.08333): '0x1f623',
              (-0.41667, 0.08333): '0x1f926', 
              (0.58333, -0.83333): '0x1f60c',
              (0.08333, -1.0): '0x1f634', 
              (0.0, -0.91667): '0x1f62a', 
              (0.33333, -0.16667): '0x1f642', 
              (0.5, -0.25): '0x1f607', 
              (0.83333, 0.66667): '0x1f60d', 
              (0.91667, 0.5): '0x1f970', 
              (0.66667, 0.16667): '0x1f60a',
              (0.41667, 0.08333): '0x1f60e', 
              (-0.41667, -0.25): '0x1f972', 
              (0.75, 0.16667): '0x263a-fe0f',
              (0.16667, 0.08333): '0x1f60f',
              (-0.41667, 0.25): '0x1f927',
              (0.75, 0.66667): '0x1f61d', 
              (-0.0, -0.25): '0x1f914',
              (-0.41667, 0.33333): '0x1f62b',
              (-0.33333, 0.08333): '0x1f612', 
              (-0.5, -0.16667): '0x1f643', 
              (0.5, 0.5): '0x1f61c', 
              (0.08333, -0.08333): '0x1f974', 
              (-0.5, -0.25): '0x1f61f', 
              (0.0, -0.83333): '0x1f971',
              (0.41667, 0.41667): '0x1f92a'}

  G = list(emojimap.keys())
  def __init__(self, Ratio=0.35):
    # R is the ratio contribution for audio arousal. So if R = 0.9, then
    # fusion will take 0.9 arousal from audio and 0.1 from video.
    self.Ratio = Ratio

  def dist(self, p, q):
    r = math.sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2)
    return r

  def get_nearest_emoji(self, datapoint):
    # set the nearest emoji as the first emoji coordinate
    dmin = self.dist(self.G[0], datapoint)
    ptmin = self.G[0]
    # for every emoji coordinate...
    for g in self.G:
      # compute the distance from the current point
      d = self.dist(g, datapoint)
      if(d < dmin):
        # if nearer to the input datapoint, then that is the new best emoji
        dmin = d
        ptmin = g

    emoji = self.emojimap[ptmin]    
    return emoji

  def coord_to_emoji(self, coords):
    emoji = self.get_nearest_emoji(coords)
    return emoji

  def fuse(self, emonet, audiopy):
    valence = emonet[0]
    arousal = self.Ratio*audiopy + (1-self.Ratio)*emonet[1]
    datapoint = (valence, arousal)
    return datapoint

