import numpy as np
import open3d as o3d
import cv2
import time

start_time = time.time()

depth_map = cv2.imread('face.png', 0)
color_raw = cv2.imread("test.jpg")
depth_map = cv2.invert(depth_map)

#depth_map = cv2.resize(depth_map, (0,0), fx=0.5, fy=0.5)
#color_raw = cv2.resize(depth_map, (0,0), fx=0.5, fy=0.5)

print("Generating 3D mesh...")
color_raw = color_raw[:, :, ::-1].astype('float32') / 255.
depth_map = depth_map.astype('float32')

x = np.arange(0, depth_map.shape[1])
y = np.arange(0, depth_map.shape[0])
mesh_x, mesh_y = np.meshgrid(x, y)
z = (255. - depth_map) * 3.

xyz = np.zeros((np.size(mesh_x), 3))
xyz[:, 0] = np.reshape(mesh_x, -1)
xyz[:, 1] = np.reshape(mesh_y, -1)
xyz[:, 2] = np.reshape(z, -1)

colors = np.reshape(color_raw, (color_raw.shape[0] * color_raw.shape[1], 3))

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(xyz)
pcd.colors = o3d.utility.Vector3dVector(colors)
o3d.visualization.draw_geometries([pcd])
print("#####---%s seconds ---#####" % (time.time() - start_time))
   
