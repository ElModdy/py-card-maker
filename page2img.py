import sys
import papyrus_pb2
import cairocffi
import math

DPI = 200 # defined by cairocffi
SQUID_PATH = "/data/data/com.steadfastinnovation.android.projectpapyrus/files/data/pages/"
ANKI_PATH = "/sdcard/AnkiDroid/collection.media/"

def cm_to_point(cm):
    return cm / 2.54 * DPI


def u32_to_4f(u):
    return [((u>>24) & 0xFF) / 255.0, ((u>>16) & 0xFF) / 255.0, ((u>>8) & 0xFF) / 255.0, (u & 0xFF) / 255.0]


def get_surface(items, height, width):
    surface = cairocffi.ImageSurface(cairocffi.FORMAT_ARGB32, width, height)
    context = cairocffi.Context(surface)

    # Paint the page white
    context.set_source_rgb(1, 1, 1)
    context.paint()

    for item in items:
        if item.type == papyrus_pb2.Item.Type.Value('Stroke'):
            #print(item)
            context.save()
            # Translate to reference_point (stroke origin)
            context.translate(cm_to_point(item.stroke.reference_point.x), cm_to_point(item.stroke.reference_point.y))
            # Set source color
            argb = u32_to_4f(item.stroke.color)
            context.set_source_rgba(argb[1], argb[2], argb[3], argb[0])
            # Set line width
            width = cm_to_point(item.stroke.weight)
            # Other parameter
            context.set_line_join(cairocffi.LINE_JOIN_ROUND)
            context.set_line_cap(cairocffi.LINE_CAP_ROUND)
            context.move_to(0, 0)

            for point in item.stroke.point:
                context.line_to(cm_to_point(point.x), cm_to_point(point.y))
                if point.HasField('pressure'):
                    context.set_line_width(width * point.pressure)
                else:
                    context.set_line_width(width)
                context.stroke()
                context.move_to(cm_to_point(point.x), cm_to_point(point.y))
            context.restore()
        elif item.type == papyrus_pb2.Item.Type.Value('Shape') and item.shape.ellipse is not None:

            context.save()
            context.new_sub_path()
            context.translate(cm_to_point(item.shape.ellipse.center_x), cm_to_point(item.shape.ellipse.center_y))
            context.set_line_width(item.shape.ellipse.weight)
            argb = u32_to_4f(item.shape.ellipse.color)
            context.set_source_rgba(argb[1], argb[2], argb[3], argb[0])
            context.scale(cm_to_point(item.shape.ellipse.radius_x), cm_to_point(item.shape.ellipse.radius_y))
            context.arc(0, 0, 1, (item.shape.ellipse.start_angle / 360) * 2 * math.pi,
                        (item.shape.ellipse.sweep_angle / 360) * 2 * math.pi)
            context.close_path()
            context.stroke()
            context.restore()
        elif item.type == papyrus_pb2.Item.Type.Value('Text'):

            context.save()
            context.set_font_size(item.text.weight)

            # Color
            argb = u32_to_4f(item.text.color)
            context.set_source_rgba(argb[1], argb[2], argb[3], argb[0])

            context.move_to(cm_to_point(item.text.bounds.left), cm_to_point(item.text.bounds.top))
            tw = int(item.text.weight)
            size_m = cairocffi.Matrix(tw, 0, 0, tw, 0, 0)
            scaledFont = cairocffi.ScaledFont(cairocffi.ToyFontFace("sans-serif"), size_m)
            glyphs = scaledFont.text_to_glyphs(cm_to_point(item.text.bounds.left), cm_to_point(item.text.bounds.bottom),
                                               item.text.text, False)
            context.show_glyphs(glyphs)
            context.restore()
        else:
            print(item)
            print("Item of type {} not supported".format(papyrus_pb2.Item.Type.Name(item.type)))

    return surface


def get_bigger(b1, b2):
    if b1 is None:
        return b2

    if b1.left > b2.left:
        b1.left = b2.left
    if b1.top > b2.top:
        b1.top = b2.top
    if b1.right < b2.right:
        b1.right = b2.right
    if b1.bottom < b2.bottom:
        b1.bottom = b2.bottom

    return b1


def crop_surface(surface, bounds):
    width = int(cm_to_point(bounds.right - bounds.left))
    height = int(cm_to_point(bounds.bottom - bounds.top))

    new_surface = cairocffi.ImageSurface(cairocffi.FORMAT_ARGB32, width, height)
    context = cairocffi.Context(new_surface)
    context.set_source_surface(surface, -int(cm_to_point(bounds.left)), -int(cm_to_point(bounds.top)))
    context.paint()
    return new_surface


def handle_page(page_name):
    page_path = "{}{}.page".format(SQUID_PATH, page_name)

    page = papyrus_pb2.Page()
    page.ParseFromString(open(page_path).read())


    separator = 0
    for item in page.layer.item:
        if item.type == papyrus_pb2.Item.Type.Value('Stroke'):
            if item.stroke.color == 4294961979:
                separator = item.stroke.bounds.top
                print(item.stroke.bounds)
                break

    btop = bdown = None
    for item in page.layer.item:
        if item.type == papyrus_pb2.Item.Type.Value('Stroke') and item.stroke.color != 4294961979:
            if item.stroke.bounds.top > separator:
                bdown = get_bigger(bdown, item.stroke.bounds)
            else:
                btop = get_bigger(btop, item.stroke.bounds)

    print("bTop")
    print(btop)
    print("bDown")
    print(bdown)

    top_right = 0 if btop is None else btop.right

    height = int(cm_to_point(bdown.bottom))
    width = int(cm_to_point(max(bdown.right, top_right)))

    surface = get_surface(page.layer.item, height, width)

    bugged = True

    if btop is not None:
        bugged = False
        stop = crop_surface(surface, btop)
        stop.write_to_png('{}{}top.png'.format(ANKI_PATH, page_name))

    sdown = crop_surface(surface, bdown)
    sdown.write_to_png('{}{}down.png'.format(ANKI_PATH, page_name))

    return bugged
