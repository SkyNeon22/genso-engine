


'''The core of the engine.
   Please read all of the text below.

   SOME FEATURES
   --------

   - 3D support (OpenGl with glm included (glm makes 3d math easier))

   - A lot of control of the core components of the engine

   - Included documentation

   - A lot of built-ins

   - Registry system


   INCLUDED COMPONENTS
   --------

   - Enemies and Behaviors (and built-ins)

   - Shottypes (Legacy TH2-TH8, YinYang focused TH10-TH20, Custom TH9.5 or TH12.5(or any other custom shottype))(and built-ins)

   - Visuals (3D and 2D)

   - Spellcard System and Nonspells (and built-ins)

   - Projectiles and Pickups (and built-ins)

   - Stage system

   - Registry system (with built-in registries)

   ADDITIONS
   --------

   - Additional functions

   - Interpolation formulas

   To import the additions add: from core.additions import *

   To import utils: from core.utils import *




   PLANNED FEATURES
   --------

   - Compilation by using Nuitka (binary compilation)

   - A custom compilation module (no binary compilation)

   - Multithreading and Multiprocessing

   - Advanced logging

   - Better error catching

   - A custom programming language

   - ImGUI bindings

   - Networking
   
   FAQ
   ------- 
   
   1.Q:To be added
     A:To be added

   Engine is in active development
   -------

   SO PLEASE REPORT THE BUGS
   --------
   
   '''

# game
from core.game import *
from core.low import *
# visuals
from core.visuals import *
# sound, music
from core.sound import *