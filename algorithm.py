def synpan(i):
  sb=i.select('B8').reduceNeighborhood(**{
  'reducer': ee.Reducer.mean(),
  'kernel': ee.Kernel.square(1),}).rename('B8_syn')
  sb=sb.reproject(i.select('B8').projection())
  return i.addBands(sb)

def paned(i):
 img1=ee.Image(1)
 pan=i.select('B8')
 proj=pan.projection()
 pans=i.select('B8_syn')
 ms=i.select('B[1-7]').resample().reproject('EPSG:32623', None,15)
 ms=ms.reproject(pan.projection())
 bandas=['B7','B6', 'B4','B3', 'B2']
 for banda in bandas:
  bb=ms.select(banda)
  nb=(pan.divide(pans)).multiply(bb)\
   .rename('%s_pan'%banda)
  img1=img1.addBands(nb)
 b5=i.select('B5').resample().reproject('EPSG:32623', None,15)
 b5=b5.reproject(proj).rename('B5_pan')
 img1=img1.addBands(b5)
 img1=img1.addBands([pan,pans])
 ms1=img1.select('B.*').set('system:time_start', i.get('system:time_start'))
 return ms1
