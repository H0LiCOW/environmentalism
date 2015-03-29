import make_ope_moircs_2015a as mkope

# HE0435
# Note that for this target, we will only observe in H-band
mkope.make_h('HE0435',firstobs=True)

# HE1104
mkope.make_h('HE1104',firstobs=True,filtchange=False)
mkope.make_j('HE1104')
mkope.make_ks('HE1104')

# RXJ1131
mkope.make_ks('RXJ1131',firstobs=True,filtchange=False)
mkope.make_h('RXJ1131')
mkope.make_j('RXJ1131')

# B1608
mkope.make_j('B1608',firstobs=True,filtchange=False)
mkope.make_h('B1608')
mkope.make_ks('B1608')

# Standard star FS27
mkope.make_std()
