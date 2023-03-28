

from layer_store import SequenceLayerStore
from layers import black, lighten, rainbow, invert


# s = SequenceLayerStore()
# for color in [
#     (255, 255, 255),
#     (0, 0, 0),
#     (255, 0, 255),
# ]:
#     assert(s.get_color(color, 0, 1, 1)== color)

# s = SequenceLayerStore()
# s.add(black)
# # Light comes after black.
# s.add(lighten)
# assert(s.get_color((100, 100, 100), 0, 20, 40)== (40, 40, 40))
# s.erase(lighten)
# s.add(rainbow)
# # Rainbow comes before black.
# assert(s.get_color((20, 20, 20), 7, 0, 0)== (0, 0, 0))


# s = SequenceLayerStore()
# s.add(black)
# s.add(lighten)
# s.erase(lighten)
# assert(s.get_color((25, 25, 25), 7, 0, 0)== (0, 0, 0))


s = SequenceLayerStore()
s.add(invert)
s.add(lighten)
s.add(rainbow)
s.add(black)
assert(s.get_color((100, 100, 100), 0, 0, 0)== (215, 215, 215))
s.special() # Ordering: Black, Invert, Lighten, Rainbow.
#             # Remove: Invert
assert(s.get_color((100, 100, 100), 7, 0, 0)== (40, 40, 40))
s.special() # Ordering: Black, Lighten, Rainbow.
            # Remove: Lighten
assert(s.get_color((100, 100, 100), 7, 0, 0)== (0, 0, 0))
s.special() # Ordering: Black, Rainbow.
            # Remove: Black
assert(s.get_color((100, 100, 100), 7, 0, 0)== (91, 214, 104))


s = SequenceLayerStore()
s.add(rainbow)
s.add(invert)



assert(s.get_color((100, 100, 100), 7, 0, 0)== (255-91, 255-214, 255-104))
s.add(black)
assert(s.get_color((100, 100, 100), 7, 0, 0)== (255, 255, 255))
s.special() # Ordering: Black, Invert, Rainbow.
#             # Remove: Invert
assert(s.get_color((100, 100, 100), 7, 0, 0)== (0, 0, 0))
s.add(black)
assert(s.get_color((100, 100, 100), 7, 0, 0)== (0, 0, 0))
s.erase(black)
assert(s.get_color((100, 100, 100), 7, 0, 0)== (91, 214, 104))
