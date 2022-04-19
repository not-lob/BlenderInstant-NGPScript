# BlenderInstant-NGPScript

1. Align your image set in Reality Capture with all images in the same Calibration and Lens Distortion group
2. Create a preview mesh from your alignment
3. Export a FBX from Reality Capture, ensure Export Cameras and Undistort Images are set to Yes
4. Open Blender, and delete the default cube, camera and light
5. Import your previously created FBX
6. Copy and paste the script into a new Text item in the Scripting view
7. Save your Blender project (script won't run without this step)
8. Run the script
9. Add scale, aabb_scale, and offset to the generated transform.json (example values below but dataset dependent)

```
    "scale": 0.15,
    "aabb_scale": 16,
    "offset": [0.5, 0.5, 0.5],
```
10. Copy your undistorted images to an images subfolder in your dataset folder and transforms.json to the root of the dataset folder
11. Run the instant-ngp testbed with your dataset
