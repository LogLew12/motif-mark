import cairo

# Creating the cairo surface
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 1000)
ctx = cairo.Context(surface)

# drawing line
line_col = "black"
ctx.set_line_width(5)
ctx.move_to(50, 500)
ctx.line_to(950, 500)
ctx.stroke()

# drawing rectangle
ctx.rectangle(400, 450, 200, 100)  # Rectangle(x0, y0, x1, y1)
ctx.fill()

# saving png
surface.write_to_png("test.png")
