import numpy as np
import cv2

class Viewer:
    def __init__(self):
        self.nrows = 0
        self.ncols = 0
        self.points = []

    def readData(self, fname):
        infile = open(fname, 'r')
        if infile.fail():
            print(" Warning: Cann't read the file ")
            return
        self.nrows, self.ncols = map(int, infile.readline().split())
        self.points = np.zeros((self.nrows, self.ncols), dtype=np.float32)
        maxalb = 0.0
        maxz = 0.0
        for i in range(self.nrows):
            for j in range(self.ncols):
                mask, x, y, z, nx, ny, nz, r, g, b, alb = map(float, infile.readline().split())
                self.points[i][j] = {
                    'mask': mask,
                    'xyz': [x, y, z],
                    'normal': [nx, ny, nz],
                    'rgb': [r, g, b],
                    'albedo': alb
                }
                maxalb = max(alb, maxalb)
                maxz = max(z, maxz)
        for i in range(self.nrows):
            for j in range(self.ncols):
                self.points[i][j]['albedo'] /= maxalb

    def display_original(self):
        for i in range(self.nrows - 1):
            for j in range(self.ncols - 1):
                mask = 1
                mask *= self.points[i][j]['mask']
                mask *= self.points[i + 1][j]['mask']
                mask *= self.points[i + 1][j + 1]['mask']
                mask *= self.points[i][j + 1]['mask']
                if mask:
                    r, g, b = self.points[i][j]['rgb']
                    cv2.rectangle(self.points[i][j]['xyz'], self.points[i + 1][j]['xyz'], self.points[i + 1][j + 1]['xyz'], self.points[i][j + 1]['xyz'], (r, g, b))

    def normal_color(self, normal):
        rgb = [0.5 * (1.0 + normal[0]), 0.5 * (1.0 + normal[1]), 0.5 * (1.0 + normal[2])]
        return rgb

    def display_albedo(self):
        for i in range(self.nrows - 1):
            for j in range(self.ncols - 1):
                mask = 1
                mask *= self.points[i][j]['mask']
                mask *= self.points[i + 1][j]['mask']
                mask *= self.points[i + 1][j + 1]['mask']
                mask *= self.points[i][j + 1]['mask']
                if mask:
                    r = self.points[i][j]['albedo']
                    g = self.points[i][j]['albedo']
                    b = self.points[i][j]['albedo']
                    cv2.rectangle(self.points[i][j]['xyz'], self.points[i + 1][j]['xyz'], self.points[i + 1][j + 1]['xyz'], self.points[i][j + 1]['xyz'], (r, g, b))

    def display_heightmap(self):
        for i in range(self.nrows - 1):
            for j in range(self.ncols - 1):
                mask = 1
                mask *= self.points[i][j]['mask']
                mask *= self.points[i + 1][j]['mask']
                mask *= self.points[i + 1][j + 1]['mask']
                mask *= self.points[i][j + 1]['mask']
                if mask:
                    r = self.points[i][j]['xyz'][2]
                    g = self.points[i][j]['xyz'][2]
                    b = self.points[i][j]['xyz'][2]
                    assert 0.0 <= r <= 1.0
                    cv2.rectangle(self.points[i][j]['xyz'], self.points[i + 1][j]['xyz'], self.points[i + 1][j + 1]['xyz'], self.points[i][j + 1]['xyz'], (r, g, b))

    def display_normalfield(self):
        dim = 2
        glEnable(GL_LIGHT0)
        for i in range(self.nrows - 1):
            for j in range(self.ncols - 1):
                mask = 1
                mask *= self.points[i][j]['mask']
                mask *= self.points[i + 1][j]['mask']
                mask *= self.points[i + 1][j + 1]['mask']
                mask *= self.points[i][j + 1]['mask']
                if mask:
                    rgb = self.normal_color(self.points[i][j]['normal'])
                    cv2.rectangle(self.points[i][j]['xyz'], self.points[i + 1][j]['xyz'], self.points[i + 1][j + 1]['xyz'], self.points[i][j + 1]['xyz'], rgb)

    def display_normalvectors(self):
        for i in range(0, self.nrows, 5):
            for j in range(0, self.ncols, 5):
                if self.points[i][j]['mask']:
                    x0, y0, z0 = self.points[i][j]['xyz']
                    cv2.line((x0, y0, z0), (x0 + 0.025 * self.points[i][j]['normal'][0], y0 + 0.025 * self.points[i][j]['normal'][1], z0 + 0.025 * self.points[i][j]['normal'][2]), (1.0, 0.0, 0.0), 2)
                    cv2.circle((x0 + 0.010 * self.points[i][j]['normal'][0], y0 + 0.010 * self.points[i][j]['normal'][1], z0 + 0.010 * self.points[i][j]['normal'][2]), 2, (0.0, 1.0, 1.0), -1)

    def display_mask(self):
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.points[i][j]['mask']:
                    cv2.circle(self.points[i][j]['xyz'], 1, (0.0, 1.0, 0.0), -1)
                else:
                    cv2.circle(self.points[i][j]['xyz'], 1, (0.2, 0.2, 0.2), -1)
                if self.points[i][j]['mask'] and self.points[i][j]['albedo'] == 0.0:
                    cv2.circle(self.points[i][j]['xyz'], 5, (1.0, 0.0, 0.0), -1)
                if self.points[i][j]['mask'] and self.points[i + 1][j]['mask'] == 0:
                    cv2.circle(self.points[i][j]['xyz'], 5, (1.0, 1.0, 0.0), -1)
                if self.points[i][j]['mask'] and self.points[i - 1][j]['mask'] == 0:
                    cv2.circle(self.points[i][j]['xyz'], 5, (1.0, 1.0, 0.0), -1)
                if self.points[i][j]['mask'] and self.points[i][j + 1]['mask'] == 0:
                    cv2.circle(self.points[i][j]['xyz'], 5, (1.0, 1.0, 0.0), -1)
                if self.points[i][j]['mask'] and self.points[i][j - 1]['mask'] == 0:
                    cv2.circle(self.points[i][j]['xyz'], 5, (1.0, 1.0, 0.0), -1)

    def display_pointcloud(self):
        glDisable(GL_LIGHTING)
        glPointSize(1)
        glBegin(GL_POINTS)
        for i in range(self.nrows):
            for j in range(self.ncols):
                rgb = self.normal_color(self.points[i][j]['normal'])
                glColor3fv(rgb)
                glVertex3fv(self.points[i][j]['xyz'])
        glEnd()
        glEnable(GL_LIGHTING)

    def display_verticalbars(self):
        glBegin(GL_LINES)
        for i in range(0, self.nrows - 1, 5):
            for j in range(0, self.ncols - 1, 5):
                mask = self.points[i][j]['mask']
                if mask:
                    rgb = self.normal_color(self.points[i][j]['normal'])
                    glColor3fv(rgb)
                    glNormal3fv(self.points[i][j]['normal'])
                    x, y, z = self.points[i][j]['xyz']
                    glVertex3f(x, y, 0.0)
                    x, y, z = self.points[i][j]['xyz']
                    glVertex3f(x, y, z)
        glEnd()

    def display_model(self):
        glBegin(GL_QUADS)
        for i in range(self.nrows - 1):
            for j in range(self.ncols - 1):
                mask = 1
                mask *= self.points[i][j]['mask']
                mask *= self.points[i + 1][j]['mask']
                mask *= self.points[i + 1][j + 1]['mask']
                mask *= self.points[i][j + 1]['mask']
                if mask:
                    rgb = self.normal_color(self.points[i][j]['normal'])
                    glColor3fv(self.points[i][j]['rgb'])
                    glNormal3fv(self.points[i][j]['normal'])
                    glVertex3fv(self.points[i][j]['xyz'])
                    rgb = self.normal_color(self.points[i][j + 1]['normal'])
                    glColor3fv(self.points[i][j + 1]['rgb'])
                    glNormal3fv(self.points[i][j + 1]['normal'])
                    glVertex3fv(self.points[i][j + 1]['xyz'])
                    rgb = self.normal_color(self.points[i + 1][j + 1]['normal'])
                    glColor3fv(self.points[i + 1][j + 1]['rgb'])
                    glNormal3fv(self.points[i + 1][j + 1]['normal'])
                    glVertex3fv(self.points[i + 1][j + 1]['xyz'])
                    rgb = self.normal_color(self.points[i + 1][j]['normal'])
                    glColor3fv(self.points[i + 1][j]['rgb'])
                    glNormal3fv(self.points[i + 1][j]['normal'])
                    glVertex3fv(self.points[i + 1][j]['xyz'])
        glEnd()

    def draw(self):
        glClearColor(0.2, 0.2, 0.2, 0.0)
        self.display_normalfield()
        self.display_normalvectors()

    def init(self):
        type = 1
        if type < 3:
            camera().setPosition(Vec((type == 0) ? 1.0 : 0.0, (type == 1) ? 1.0 : 0.0, (type == 2) ? 1.0 : 0.0))
            camera().lookAt(sceneCenter())
            camera().setType(Camera.ORTHOGRAPHIC)
            camera().showEntireScene()
            constraint = WorldConstraint()
            constraint.setRotationConstraintType(AxisPlaneConstraint.FORBIDDEN)
            camera().frame().setConstraint(constraint)
        readData(filename)
        restoreStateFromFile()
        help()

    def helpString(self):
        text = "<h2>S i m p l e V i e w e r</h2>"
        text += "Use the mouse to move the camera around the object. "
        text += "You can respectively revolve around, zoom and translate with the three mouse buttons. "
        text += "Left and middle buttons pressed together rotate around the camera view direction axis<br><br>"
        text += "Pressing <b>Alt</b> and one of the function keys (<b>F1</b>..<b>F12</b>) defines a camera keyFrame. "
        text += "Simply press the function key again to restore it. Several keyFrames define a "
        text += "camera path. Paths are saved when you quit the application and restored at next start.<br><br>"
        text += "Press <b>F</b> to display the frame rate, <b>A</b> for the world axis, "
        text += "<b>Alt+Return</b> for full screen mode and <b>Control+S</b> to save a snapshot. "
        text += "See the <b>Keyboard</b> tab in this window for a complete shortcut list.<br><br>"
        text += "Double clicks automates single click actions: A left button double click aligns the closer axis with the camera (if close enough). "
        text += "A middle button double click fits the zoom of the camera and the right button re-centers the scene.<br><br>"
        text += "A left button double click while holding right button pressed defines the camera <i>Revolve Around Point</i>. "
        text += "See the <b>Mouse</b> tab and the documentation web pages for details.<br><br>"
        text += "Press <b>Escape</b> to exit the viewer."
        return text


