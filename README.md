# pytracer
a simple python raytracer implementation

## Features:
- Lambertian diffuse
- Metals with fuzziness
- The classic checkerboard floor texture
- Emissive materials
- Optional denoiser
- Live preview while rendering
- PPM file output
- Miserable performance (slow af) 

## Example renders:
To create your own renders: Modify samples, resolution, maxBounces and ambient occlusion in "src/main.py" and add objects to the scene by calling scene.addObject() and passing an object as a parameter.

<p align="center">
  <img height="380" src="https://github.com/magnusKue/pytracer/blob/main/results/final6.png">
  <img height="200" src="https://github.com/magnusKue/pytracer/blob/main/results/lights2.png">
  <img width="307" height="200"  src="https://github.com/magnusKue/pytracer/blob/main/results/fuzzSteps.png">
</p>

### Denoising:
To denoise a render: Run "denoiser/denoise.py", choose the input file in the first filedialogue and choose the output folder in the second.

<p align="center">
  <img width="460" height="300" src="https://github.com/magnusKue/pytracer/blob/b09168ebfc334fc42beac90bb375a7fe27ea9f3a/results/final1.png">
  ➔
  <img width="460" height="300" src="https://github.com/magnusKue/pytracer/blob/b09168ebfc334fc42beac90bb375a7fe27ea9f3a/results/denoised/final1_denoised.png">
</p>
