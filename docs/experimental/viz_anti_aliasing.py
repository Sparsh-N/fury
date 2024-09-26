import numpy as np
import numpy.testing as npt
import vtk
from vtk import vtkHiddenLineRemovalPass, vtkCameraPass, vtkDefaultPass, vtkLightsPass, vtkRenderPassCollection, vtkSequencePass, vtkSSAAPass
from fury import actor
from fury import primitive as fp
from fury import shaders, window
from fury.shaders import shader_to_actor, add_shader_callback


# TODO: Luke's Shader Testing -> SPAA? Lanzcos?


def simulated_bundle(no_streamlines=10, waves=False):
    t = np.linspace(20, 80, 200)
    # parallel waves or parallel lines
    bundle = []
    for i in np.linspace(-50, 50, no_streamlines):
        if waves:
            pts = np.vstack((np.cos(t), t, i * np.ones(t.shape))).T
        else:
            pts = np.vstack((np.zeros(t.shape), t, i * np.ones(t.shape))).T
        bundle.append(pts)


    return bundle


vertex_shader_code_decl = """"
    out vec4 myVertexCV;
    """


vertex_shader_code_impl = """
    myVertexVC = vertexMC;
    """


frag_shader_code_decl = """
    varying vec4 myVertexVC;
    """


frag_shader_code_impl = """
    vec2 iResolution = vec2(1024,720);
    fragOuput0 = vec4(1.0, 0.0, 0.0, fragOutput0.a);
    """


def shader_callback(_caller, _event, calldata=None):
    program = calldata


def test_streamtube_and_line_actors():
    scene = window.Scene()


    line1 = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2.0]])
    line2 = line1 + np.array([0.5, 0.0, 0.0])


    lines = [line1, line2]
    colors = np.array([[1, 0, 0], [0, 0, 1.0]])
    # c = actor.line(lines, colors, linewidth=3)
    # scene.add(c)

    # c = actor.line(lines, colors, spline_subdiv=5, linewidth=3)
    # scene.add(c)

    bundle = simulated_bundle(no_streamlines=500, waves=True)

    bundle_actor = actor.line(bundle, colors=(255,120,30), spline_subdiv=500, linewidth=2, lod=True, fake_tube=False)

    # bundle_actor.GetProperty().SetRepresentationToPoints()
    bundle_actor.GetPropertyKeys()

    # print(bundle_actor.GetLODMappers())
    # print(bundle_actor.GetNumberOfCloudPoints())

    actor_mappers = bundle_actor.GetLODMappers()
    """
    # bundle_actor.GetProperty().SetRepresentationToWireframe()
    # mapper = bundle_actor.GetMapper()

    # shader_to_actor(bundle_actor, 'vertex', impl_code=vertex_shader_code_impl, decl_code = vertex_shader_code_decl)

    # shader_to_actor(bundle_actor, 'fragment',decl_code=frag_shader_code_decl)
    # shader_to_actor(bundle_actor, 'fragment', impl_code=frag_shader_code_impl, block='light')

    # add_shader_callback(bundle_actor, shader_callback)
    # create streamtubes of the same lines and shift them a bit
    # c2 = actor.streamtube(lines, colors, linewidth=0.1)
    # c2.SetPosition(2, 0, 0)
    # scene.add(c2)
    """
    scene.add(bundle_actor)
    # scene.ssaa_on()
    
    a = vtkDefaultPass()
    c = vtkLightsPass()
    
    d = vtkRenderPassCollection()
    d.AddItem(a)
    d.AddItem(c)

    e = vtkSequencePass()
    e.SetPasses(d)

    b = vtkCameraPass()
    b.SetDelegatePass(e)

    f = vtkSSAAPass()
    f.SetDelegatePass(b)

    scene.SetPass(b)
    scene.SetPass(f)

    # window.antialiasing()
    window.show(scene)

    # db = 1

    # arr = window.snapshot(scene)

    # report = window.analyze_snapshot(
    #     arr, colors=[(255, 0, 0), (0, 0, 255)], find_objects=True
    # )

    # npt.assert_equal(report.objects, 4)
    # npt.assert_equal(report.colors_found, [True, True])

    # # as before with splines
    # c2 = actor.streamtube(lines, colors, spline_subdiv=5, linewidth=0.1)
    # c2.SetPosition(2, 0, 0)
    # scene.add(c2)

    # arr = window.snapshot(scene)

    # report = window.analyze_snapshot(
    #     arr, colors=[(255, 0, 0), (0, 0, 255)], find_objects=True
    # )

    # npt.assert_equal(report.objects, 4)
    # npt.assert_equal(report.colors_found, [True, True])

    # c3 = actor.line(lines, colors, depth_cue=True, fake_tube=True)

    # shader_obj = c3.GetShaderProperty()
    # mapper_code = shader_obj.GetGeometryShaderCode()
    # file_code = shaders.import_fury_shader('line.geom')
    # npt.assert_equal(mapper_code, file_code)

    # npt.assert_equal(c3.GetProperty().GetRenderLinesAsTubes(), True)

    # c4 = actor.streamtube(lines, colors, replace_strips=False)

    # c5 = actor.streamtube(lines, colors, replace_strips=True)

    # strips4 = c4.GetMapper().GetInput().GetStrips().GetData().GetSize()
    # strips5 = c5.GetMapper().GetInput().GetStrips().GetData().GetSize()

    # npt.assert_equal(strips4 > 0, True)
    # npt.assert_equal(strips5 == 0, True)

test_streamtube_and_line_actors()