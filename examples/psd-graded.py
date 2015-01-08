import woo.dem
import woo.core
import woo.log
from minieigen import *
import math
S=woo.master.scene=woo.core.Scene(fields=[woo.dem.DemField(gravity=(0,0,-1))])
#psd=[(0.04,0),(.1,.7),(.2,1)]
psd=[(.05,0),(.08,.4),(.12,.7),(.2,1)]
#S.dem.par.add(woo.dem.Wall.make(.1,axis=2,sense=1))
#z0=.05
mat=woo.dem.FrictMat(density=1000,young=1e4,tanPhi=.9)
#matFloor=woo.dem.FrictMat(density=1000,young=1e8,tanPhi=.4)
#S.dem.par.add(woo.triangulated.quadrilateral(Vector3(0,0,z0),Vector3(1,0,z0),Vector3(0,1,z0),Vector3(1,1,z0),mat=matFloor,halfThick=.05,div=(4,4)))
#S.periodic=True
#S.cell.setBox(1,1,2)

# attributes common to all inlets
inletKw=dict(maxMass=-1,maxNum=-1,massRate=0,maxAttempts=5000,materials=[mat])
S.engines=[
	woo.dem.InsertionSortCollider([woo.dem.Bo1_Sphere_Aabb(),woo.dem.Bo1_Wall_Aabb(),woo.dem.Bo1_Facet_Aabb()]),
	# regular bias
	woo.dem.BoxInlet(
		box=((0,0,0),(1,1,2)),
		generator=woo.dem.PsdSphereGenerator(psdPts=psd,discrete=False,mass=True),
		# spatialBias=woo.dem.AxialBias(d01=(.02,.1),axis=2,fuzz=.5),
		spatialBias=woo.dem.PsdAxialBias(psdPts=psd,axis=2,fuzz=.1,discrete=False),
		**inletKw
	),
	# inverted bias, with capsules
	woo.dem.BoxInlet(
		box=((1.5,0,0),(2.5,1,2)),
		generator=woo.dem.PsdCapsuleGenerator(psdPts=psd,shaftRadiusRatio=(.8,1.5)),
		spatialBias=woo.dem.PsdAxialBias(psdPts=psd,axis=2,fuzz=.1,invert=True),
		**inletKw
	),
	# discrete PSD
	woo.dem.BoxInlet(
		box=((3,0,0),(4,1,2)),
		generator=woo.dem.PsdSphereGenerator(psdPts=psd,discrete=True),
		spatialBias=woo.dem.PsdAxialBias(psdPts=psd,axis=2,fuzz=.1,discrete=True),
		**inletKw
	),
	# reordered discrete PSD
	woo.dem.BoxInlet(
		box=((4.5,0,0),(5.5,1,2)),
		generator=woo.dem.PsdSphereGenerator(psdPts=psd,discrete=True),
		spatialBias=woo.dem.PsdAxialBias(psdPts=psd,axis=2,discrete=True,reorder=[2,0,1,3]),
		**inletKw
	),
	# radial bias in arc inlet
	woo.dem.ArcInlet(
		node=woo.core.Node(pos=(7,1,.65),ori=Quaternion((1,0,0),math.pi/2)),cylBox=((.2,-math.pi/2,0),(1.3,.75*math.pi,1)),
		generator=woo.dem.PsdSphereGenerator(psdPts=psd),
		spatialBias=woo.dem.PsdAxialBias(psdPts=psd,axis=0,fuzz=.7),
		**inletKw
	),
]

S.one()

woo.gl.Gl1_DemField.colorBy='radius'
woo.gl.Renderer.iniViewDir=(0,-1,0)

# abuse DEM nodes to stick labels on the top
for i,t in enumerate(['graded','inverted (capsules)','discrete','reordered','radial']):
	S.dem.nodesAppend(woo.core.Node((1+i*1.5,0,2.2),dem=woo.dem.DemData(),rep=woo.gl.LabelGlRep(text=t)))

# woo.log.setLevel('PsdSphereGenerator',woo.log.TRACE)
#S.trackEnergy=True
#S.engines=woo.dem.DemField.minimalEngines(damping=.6)+[woo.core.PyRunner(100,'e=woo.utils.unbalancedEnergy(S)\nprint "E",e\nif e<.05: S.stop()')]
#S.saveTmp()
#S.run(); S.wait()
#woo.triangulated.spheroidsToSTL(stl='/tmp/big.stl',dem=S.dem,tol=.001,clipCell=True)
#print 'Saving STL'
#woo.triangulated.spheroidsToSTL(stl='/tmp/spheroids.stl',dem=S.dem,tol=.001)
