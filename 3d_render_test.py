import sys
from PyQt5.QtWidgets import QApplication
from simpleViewer import Viewer  # Assuming simpleViewer.py exists and has a Viewer class

if __name__ == "__main__":
    assert len(sys.argv) == 2, "This program requires exactly one argument"

    app = QApplication(sys.argv)

    viewer = Viewer()
    viewer.setDataFile(sys.argv[1])
    viewer.setWindowTitle("simpleViewer")

    viewer.show()

    sys.exit(app.exec_())


