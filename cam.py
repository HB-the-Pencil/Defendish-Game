class Camera:
    """Class to represent a camera, which draws everything on screen."""

    def __init__(self, x, y, w, h):
        """
        Initialize the camera's window.

        :param x: X-location of the camera.
        :param y: Y-location of the camera.
        :param w: Width of the camera.
        :param h: Height of the camera.
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def move(self, x_mov, y_mov):
        """
        Move the camera.

        :param x_mov: Movement along the x-axis.
        :param y_mov: Movement along the y-axis.

        :return: Moves the camera. Not updated until the draw call.
        """
        self.x += x_mov
        self.y += y_mov

    def draw(self):
        """
        Draw the things that are in frame (needed?)

        :return: Draws whatever is in frame.
        """
        pass