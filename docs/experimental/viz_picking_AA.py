"""
=====================
Simple picking
=====================

Here we present a tutorial showing how to interact with objects in the
3D world. All objects to be picked are part of a single actor.
FURY likes to bundle objects in a few actors to reduce code and
increase speed.

When the objects are picked they will change size and color.
"""

import numpy as np

import vtk
from fury import actor, ui, utils, window

centers = 0.2 * np.array([[0, 0, 0], [100, 0, 0], [200, 0, 0.0]])
colors = np.array([[0.8, 0, 0], [0, 0.8, 0], [0, 0, 0.8]])
radii = 0.1 * np.array([50, 100, 150.0])

selected = np.zeros(3, dtype=bool)

###############################################################################
# Let's create a panel to show what is picked

panel = ui.Panel2D(size=(400, 200), color=(1, 0.5, 0.0), align='right')
panel.center = (150, 200)

text_block = ui.TextBlock2D(text='Left click on object \n')
# panel.add_element(text_block, (0.3, 0.3))

###############################################################################
# Build scene and add an actor with many objects.

scene = window.Scene()

label_actor = actor.vector_text(text='Test')

###############################################################################
# This actor is made with 3 cubes of different orientation

directions = np.array(
    [
        [np.sqrt(2) / 2, 0, np.sqrt(2) / 2],
        [np.sqrt(2) / 2, np.sqrt(2) / 2, 0],
        [0, np.sqrt(2) / 2, np.sqrt(2) / 2],
    ]
)
fury_actor = actor.cube(centers, directions, colors, scales=radii)
# fury_actor.GetProperty().SetRepresentationToSurface()
fury_actor.GetProperty().SetRepresentationToWireframe()
fury_actor.GetProperty().SetInterpolationToFlat()
# fury_actor.GetProperty().EdgeVisibilityOn()
# fury_actor.GetProperty().SetEdgeColor(0,0,0)
fury_actor.GetProperty().SetLineWidth(5)
# fury_actor.GetProperty().ShadingOff()
# fury_actor.GetProperty().SetRenderLinesAsTubes(True)

#Tests with mapper
fury_actor.GetMapper().ScalarVisibilityOff()
# scene.GetRenderWindow().GetZbufferData()

# PBR
# fury_actor.GetProperty().SetSpecular(1.0)
# fury_actor.GetProperty().SetAmbient(1)

fury_actor2 = actor.cube(0.2 * np.array([[-100,0,0],[-200,0,0],[-300,0,0]]),directions, colors, scales=radii)
# fury_actor2.GetProperty().SetRepresentationToWireframe()
# fury_actor2.GetProperty().SetAmbient(1)
# scene.add(fury_actor2)

###############################################################################
# Access the memory of the vertices of all the cubes

vertices = utils.vertices_from_actor(fury_actor)
num_vertices = vertices.shape[0]
num_objects = centers.shape[0]

###############################################################################
# Access the memory of the colors of all the cubes

vcolors = utils.colors_from_actor(fury_actor, 'colors')

###############################################################################
# Adding an actor showing the axes of the world coordinates
ax = actor.axes(scale=(10, 10, 10))

scene.add(fury_actor)
# scene.add(label_actor)
# scene.add(ax)
scene.reset_camera()

###############################################################################
# Make the window appear

scene.fxaa_off()
# scene.projection('parallel')

showm = window.ShowManager(scene, size=(1024, 768), multi_samples=8, order_transparent=True)

#####################################

"""
print("Step 0")
z_buffer = vtk.vtkFloatArray()
showm.window.GetZbufferData(0,0,1023,767, z_buffer)

print("Step 1")
#####
image = vtk.vtkImageData()
image.SetDimensions(1024, 768, 1)
image.SetScalarTypeToFloat()
image.GetPointData().SetScalars(z_buffer)

print("Step 2")
# Create a texture from the vtkImageData object
texture = vtk.vtkTexture()
texture.SetInputData(image)


print("Step 3")
# Create a quad that fills the render window
quad = vtk.vtkPlaneSource()
quad.SetPoint1(1024, 0, 0)
quad.SetPoint2(0, 768, 0)
quad.SetOrigin(0, 0, 0)

print("Step 4")
# Map the texture onto the quad
quad_mapper = vtk.vtkPolyDataMapper()
quad_mapper.SetInputConnection(quad.GetOutputPort())


print("Step 5")
quad_actor = vtk.vtkActor()
quad_actor.SetMapper(quad_mapper)
quad_actor.SetTexture(texture)

print("Step 6")
scene.add(quad_actor)
"""
############################

showm.initialize()

print(showm.window.GetAlphaBitPlanes())
#####
# print(showm.scene.GetActiveCamera().GetParallelProjection())

# print(showm.window.GetDebug())

# scene.add(panel)

###############################################################################
# Change interactive to True to start interacting with the scene

interactive = True

if interactive:

    showm.start()


###############################################################################
# Save the current framebuffer in a PNG file

window.record(showm.scene, size=(1024, 768), out_path='viz_picking.png')
