# Pansharpening_Landsat

create a def that make fusion in landsat from Rahaman 2017

PANSHARPENING

Tem versão em portugues abaixo.

"Firstly, we generated a synthetic image known as “Synthetic Pan” image (Syn PAN ) as a function of averaging of the PAN image over a moving kernel of n × n size (i.e., 3 × 3 in this study). Here, we opted to consider a 3 × 3 moving window in order to retain the local variabilities of the reflectance regimes. Secondly, we employed the Syn PAN image in conjunction with PAN and specific MS bands (MS i ) in order to generate pan-sharpened MS bands of interest (i.e., Fused i )."

Above, the process that I put in colab. Foward to make the pansharpening of landsat is necessary adjust NIR band (used in NDVI, NDWI, NDBI and others) because it isn't correlated with the panchromatic band. Then, I looked for a fusion method that calcule band individually based. Rahaman et al (2017) (https://www.mdpi.com/2220-9964/6/6/168) use this proceed and describe it. I  didn't find that code in colab, even in java script, and here my contribution that permit use of band by band fusion.

--  
Para melhorar a resolução da imagem de satélite costuma-se utilizar a técnica de pansharpening, que é a fusão de uma imagem de baixa resolução com outra de maior resolução. Na imagem do landsat a banda pancromática de 15 metros é usada como referencia para reescalar a de 30. A banda pancromática é preto e branca e não capta os detalhes espectrais que as outras - Multiespectrais- (vermelha, verde, azul, infravermelho próximo e médios) podem fazer.
Os métodos de fusão costumam juntar bandas multi espectrais para criar uma imagem, juntar com a pancromática e daí derivar novamente bandas multi espectrais com resolução de 15 metros.
O problema é que a banda infravermelha próxima, banda 5 no landsat 8, não é bem correlacionada com a pancromática e fazer o fusionamento dela pode incorrer em erros. Essa banda é usada em diversos índices muito conhecidos como o NDVI, NDBI e NDWI, por exemplo. 
Rahaman et al (2017) (https://www.mdpi.com/2220-9964/6/6/168) mostrou que o fusionamento pode ocorrer desde que seja feita através de uma banda de cada vez. Esse é um procedimento não muito utilizado e não encontrei nada para usar no google earth engine. 
O que apresento aqui são duas def (métodos) em python que permite esse uso e consegue fazer o fusionamento banda por banda.

Example:
roi4 = ee.Geometry.Rectangle(\  
[[-42.946797281314836, -22.39472469429372],  
[-42.92057776318739, -22.376874965199057] ] )  

colID="LANDSAT/LC08/C02/T1_RT_TOA"  
img = ee.ImageCollection(colID).filterBounds(roi4)\  
          .sort('CLOUD_COVER')\  
          .select("B[2-8]").first()  
  
#here was needed reproject the MS bands to match with panchromatic band.  
#I don't know why this happened, but put a question,and a possible solution, to Geo community here:  
#https://gis.stackexchange.com/questions/448332/landsat-8-panchromatic-band-and-multispectral-overlap-in-gee

img=img.reproject(img.select('B8').projection())
imgI=synpan(img)
imgP=paned(imgI)

parRgb={'bands': ['B5','B4', 'B3'], 'min': 0, 'max': 0.5, 'gamma': [0.95, 1.1, 1]}  
parRgbP={'bands': ['B5_pan','B4_pan', 'B3_pan'], 'min': 0, 'max': 0.5, 'gamma': [0.95, 1.1, 1]}  
Map.addLayer(img.clip(roi4), parRgb, 'RGB_30')  
Map.addLayer(imgP.clip(roi4), parRgbP, 'RGB_15')  
Map = geemap.Map(location=roi.centroid().coordinates().getInfo()[::-1], zoom_start = 11, width=500, height=500)  
Map.add_basemap('SATELLITE')  
Map.addLayer(roi1,{},'teresopolis')  
Map.addLayerControl()  
Map
