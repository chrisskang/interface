import compute_rhino3d.Util
import compute_rhino3d.Grasshopper as gh
import rhino3dm
import json

compute_rhino3d.Util.url = "http://localhost:6500/"
#compute_rhino3d.Util.apiKey = ""

pt1 = rhino3dm.Point3d(2, 1, 3)
circle = rhino3dm.Circle(pt1, 5)
angle = 90

indexList = [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
angleList = [0,30,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# convert circle to curve and stringify
curve = json.dumps(circle.ToNurbsCurve().Encode())

# create list of input trees

index_tree = gh.DataTree("index")
for a,i in enumerate(indexList):
    index_tree.Append([i], [a])

angle_tree = gh.DataTree("angle")
for a,i in enumerate(angleList):
    angle_tree.Append([i], [a])

trees = [index_tree, angle_tree]
# curve_tree = gh.DataTree("curve")
# curve_tree.Append([0], [curve])

# rotate_tree = gh.DataTree("rotate")
# rotate_tree.Append([0], [angle])
# trees = [curve_tree, rotate_tree]

output = gh.EvaluateDefinition('hops.gh', trees)
print(output)


def unit_vector(vector):
    return vector/ np.linalg.norm(vector)

def angle_between(v1, v2):

    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0,1.0))
# decode results
# branch = output['values'][0]['InnerTree']['{0}']
# print(branch)

# for item in branch:
#     print(item['data'])
#data = [json.loads(item['data']) for item in branch]

#lines = [rhino3dm.CommonObject.Decode(json.loads(item['data'])) for item in branch]

# filename = 'twisty.3dm'

# print('Writing {} lines to {}'.format(len(lines), filename))





# # create a 3dm file with results
# model = rhino3dm.File3dm()
# for l in lines:
#     model.Objects.AddCurve(l) # they're actually LineCurves...

# model.Write(filename)

