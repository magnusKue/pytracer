# Image

imageWidth = 256
imageHeight = 256

maxColorVal = 255

# Render

output = ""
output += f"P3\n{imageWidth} {imageHeight} \n{maxColorVal}\n"

for y in range(imageHeight):
    for x in range(imageWidth):
        r = x / (imageWidth-1) 
        g = y / (imageHeight-1)
        b = 0

        ir = int(255.999 * r)
        ig = int(255.999 * g)
        ib = int(255.999 * b)

        output += f"{ir} {ig} {ib}\n"

with open("C:\\Users\\Magnus\\Magnus\\Code\\py\\raytracer\\v01\\output2.ppm", "w") as fp:
    fp.write(output)

