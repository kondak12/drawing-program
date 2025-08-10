import pygame, os


def get_image(img_name: str):
    return pygame.image.load(os.path.join(r"resources\imgs", img_name))

PROGRAM_LOGO = get_image("drawing_program_logo.png")

BUTTONS = {
    "LINE_SIZE" : [
        get_image("1_draw_radius_black.jpg"),
        get_image("2_draw_radius_black.jpg"),
        get_image("3_draw_radius_black.jpg")
    ],
    "ACTION_BACK" : [
        get_image("action_back_black.jpg"),
        get_image("action_back_grey.jpg")
    ],
    "ACTION_FORWARD" : [
        get_image("action_forward_black.jpg"),
        get_image("action_forward_grey.jpg")
    ],
    "BRUSH" : [
        get_image("brush_black.jpg"),
        get_image("brush_grey.jpg")
    ],
    "FILL": [
        get_image("fill_black.jpg"),
        get_image("fill_grey.jpg")
    ],
    "RECT": [
        get_image("rect_black.jpg"),
        get_image("rect_grey.jpg")
    ],
    "CIRCLE" : [
        get_image("circle_black.jpg"),
        get_image("circle_grey.jpg")
    ],
    "IMPORT" : [
        get_image("import_black.jpg"),
        get_image("import_grey.jpg")
    ],
    "EXPORT" : [
        get_image("export_black.jpg"),
        get_image("export_grey.jpg")
    ]
}