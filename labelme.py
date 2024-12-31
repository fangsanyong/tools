import sys
import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QGraphicsView,
    QGraphicsScene, QVBoxLayout, QHBoxLayout, QComboBox, QWidget, QMessageBox,
    QGraphicsPixmapItem, QGraphicsTextItem, QListWidget
)
from PyQt5.QtGui import QPixmap, QPen, QMouseEvent, QColor, QFont
from PyQt5.QtCore import Qt, QRectF

class AnnotationTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOLOv5 Annotation Tool")
        self.setGeometry(100, 100, 1200, 800)
        
        # Variables
        self.image_folder = ""
        self.completed_folder = ""
        self.image_files = []
        self.current_image_index = -1
        self.current_image_path = ""
        self.current_annotations = []
        self.drawing = False
        self.start_point = None
        self.end_point = None
        self.current_class = 0
        self.class_list = []
        self.temp_rect = None
        self.viewing_mode = False

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()  # Changed to horizontal to add a left side panel

        # Left side panel for classes
        left_panel = QVBoxLayout()
        self.classes_list = QListWidget()
        self.classes_list.currentRowChanged.connect(self.set_current_class)
        left_panel.addWidget(QLabel("Classes:"))
        left_panel.addWidget(self.classes_list)
        
        # Add QComboBox for class selection
        self.class_input = QComboBox()
        left_panel.addWidget(QLabel("Current Class:"))
        left_panel.addWidget(self.class_input)
        
        main_layout.addLayout(left_panel)  # Add left panel to main layout

        # Right side for main content
        right_panel = QVBoxLayout()
        top_layout = QHBoxLayout()

        self.load_images_btn = QPushButton("Load Images")
        self.load_images_btn.clicked.connect(self.load_images)

        self.select_completed_btn = QPushButton("Select Completed/Output Folder")
        self.select_completed_btn.clicked.connect(self.select_completed_folder)

        self.load_classes_btn = QPushButton("Load Classes")
        self.load_classes_btn.clicked.connect(self.load_classes)

        self.next_image_btn = QPushButton("Next Image")
        self.next_image_btn.clicked.connect(self.next_image)

        self.prev_image_btn = QPushButton("Previous Image")
        self.prev_image_btn.clicked.connect(self.prev_image)

        self.view_annotations_btn = QPushButton("View Annotations")
        self.view_annotations_btn.clicked.connect(self.view_annotations)

        top_layout.addWidget(self.load_images_btn)
        top_layout.addWidget(self.select_completed_btn)
        top_layout.addWidget(self.load_classes_btn)
        top_layout.addWidget(self.prev_image_btn)
        top_layout.addWidget(self.next_image_btn)
        top_layout.addWidget(self.view_annotations_btn)

        right_panel.addLayout(top_layout)

        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        right_panel.addWidget(self.graphics_view)

        main_layout.addLayout(right_panel, 1)  # Add right panel with flexibility

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Override mouse events for drawing mode only
        self.graphics_view.mousePressEvent = lambda e: self.mouse_press_event(e) if not self.viewing_mode else None
        self.graphics_view.mouseMoveEvent = lambda e: self.mouse_move_event(e) if not self.viewing_mode else None
        self.graphics_view.mouseReleaseEvent = lambda e: self.mouse_release_event(e) if not self.viewing_mode else None



    def load_images(self):
        self.image_folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if not self.image_folder:
            return

        self.image_files = [
            os.path.join(self.image_folder, f)
            for f in os.listdir(self.image_folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]
        if self.image_files:
            self.current_image_index = 0  # Start at the first image
            self.current_image_path = self.image_files[0]
            self.current_annotations = []
            self.viewing_mode = False
            self.update_scene()
        else:
            QMessageBox.warning(self, "Warning", "No images found in the selected folder!")

    def select_completed_folder(self):
        self.completed_folder = QFileDialog.getExistingDirectory(self, "Select Completed/Output Folder")

    
    def load_classes(self):
        class_file, _ = QFileDialog.getOpenFileName(self, "Select Class File", "", "Text Files (*.txt)")
        if not class_file:
            return

        with open(class_file, "r") as f:
            self.class_list = [line.strip() for line in f if line.strip()]

        self.classes_list.clear()
        self.classes_list.addItems(self.class_list)
        self.class_input.clear()
        self.class_input.addItems(self.class_list)  # Populate QComboBox with class names

        
    def set_current_class(self, index):
        self.current_class = index
        self.class_input.setCurrentIndex(index)  # Sync QComboBox with QListWidget 

    def next_image(self):
        if not self.viewing_mode:
            self.save_and_next_image()
        else:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
            self.load_next_annotation()

    # def prev_image(self):
    #     if self.image_files:
    #         if not self.viewing_mode:
    #             if self.current_image_index > 0:
    #                 self.current_image_index -= 1
    #             else:
    #                 self.current_image_index = len(self.image_files) - 1  # Go to last image
    #             self.current_annotations = []
    #         else:
    #             self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
    #         self.current_image_path = self.image_files[self.current_image_index]
    #         self.update_scene()
    #     else:
    #         QMessageBox.warning(self, "Warning", "No images available to navigate!")
    def prev_image(self):
        if not self.image_files:
            QMessageBox.warning(self, "Warning", "No images available to navigate!")
            return

        if not self.viewing_mode:
            if self.current_image_index > 0:
                self.current_image_index -= 1
            else:
                self.current_image_index = len(self.image_files) - 1  # Wrap around to last image
            self.current_annotations = []  # Reset annotations when changing image in annotation mode
        else:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
            # Clear annotations when switching images in viewing mode to avoid confusion
            self.current_annotations = []

        self.current_image_path = self.image_files[self.current_image_index]
        self.update_scene()       
        
    def save_and_next_image(self):
        if self.current_annotations:
            self.save_annotations()
            self.move_to_completed()
        if self.current_image_index + 1 < len(self.image_files):
            self.current_image_index += 1
            self.current_image_path = self.image_files[self.current_image_index]
            self.current_annotations = []
            self.update_scene()
        else:
            QMessageBox.information(self, "Info", "All images have been annotated!")

    def save_annotations(self):
        if not self.completed_folder:
            QMessageBox.warning(self, "Warning", "Output folder not selected!")
            return

        base_name = os.path.splitext(os.path.basename(self.current_image_path))[0]
        txt_file = os.path.join(self.completed_folder, f"{base_name}.txt")

        with open(txt_file, "w") as f:
            for annotation in self.current_annotations:
                class_id, x_center, y_center, width, height = annotation
                f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

    def move_to_completed(self):
        if not self.completed_folder:
            QMessageBox.warning(self, "Warning", "Completed folder not selected!")
            return

        shutil.move(self.current_image_path, self.completed_folder)

    def mouse_press_event(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.start_point = self.graphics_view.mapToScene(event.pos())
            if self.temp_rect:
                self.scene.removeItem(self.temp_rect)
            self.temp_rect = self.scene.addRect(0, 0, 0, 0, QPen(Qt.blue, 2, Qt.DashLine))

    def mouse_move_event(self, event: QMouseEvent):
        if self.drawing:
            self.end_point = self.graphics_view.mapToScene(event.pos())
            if self.temp_rect:
                self.update_temp_rect()

    def mouse_release_event(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.end_point = self.graphics_view.mapToScene(event.pos())
            
            for item in self.scene.items():
                if isinstance(item, QGraphicsPixmapItem):
                    pixmap = item.pixmap()
                    img_width, img_height = pixmap.width(), pixmap.height()
                    break
            else:
                img_width, img_height = self.scene.width(), self.scene.height()

            # Truncate coordinates to ensure they are within image bounds
            start_x = max(0, min(self.start_point.x(), img_width))
            start_y = max(0, min(self.start_point.y(), img_height))
            end_x = max(0, min(self.end_point.x(), img_width))
            end_y = max(0, min(self.end_point.y(), img_height))

            # Ensure width and height are positive
            x_center = (start_x + end_x) / 2 / img_width
            y_center = (start_y + end_y) / 2 / img_height
            width = abs(end_x - start_x) / img_width
            height = abs(end_y - start_y) / img_height

            # Avoid zero-sized boxes
            width = max(width, 1e-6)
            height = max(height, 1e-6)

            self.current_class = self.class_input.currentIndex()
            self.current_annotations.append((self.current_class, x_center, y_center, width, height))
            self.update_scene()


    def update_temp_rect(self):
        if self.temp_rect and self.start_point and self.end_point:
            self.temp_rect.setRect(QRectF(self.start_point, self.end_point).normalized())

    def update_scene(self):
        self.scene.clear()
        if self.current_image_path:
            pixmap = QPixmap(self.current_image_path)
            self.scene.addPixmap(pixmap)
            self.graphics_view.setSceneRect(QRectF(pixmap.rect()))
            if not self.viewing_mode:
                self.temp_rect = self.scene.addRect(0, 0, 0, 0, QPen(Qt.blue, 2, Qt.DashLine))

        # Define colors for 80 classes with an attempt at visual distinction
        colors = [
            QColor(255, 0, 0),        # Red for class 0
            QColor(0, 255, 0),        # Green for class 1
            QColor(0, 0, 255),        # Blue for class 2
            QColor(255, 255, 0),      # Yellow for class 3
            QColor(255, 0, 255),      # Magenta for class 4
            QColor(0, 255, 255),      # Cyan for class 5
            QColor(128, 0, 0),        # Dark Red for class 6
            QColor(0, 128, 0),        # Dark Green for class 7
            QColor(0, 0, 128),        # Dark Blue for class 8
            QColor(128, 128, 0),      # Olive for class 9
            QColor(128, 0, 128),      # Purple for class 10
            QColor(0, 128, 128),      # Teal for class 11
            QColor(255, 128, 0),      # Orange for class 12
            QColor(64, 224, 208),     # Turquoise for class 13
            QColor(139, 0, 139),      # Dark Magenta for class 14
            QColor(255, 165, 0),      # Goldenrod for class 15
            QColor(128, 128, 128),    # Gray for class 16
            QColor(255, 20, 147),     # Deep Pink for class 17
            QColor(0, 255, 127),      # Spring Green for class 18
            QColor(75, 0, 130),       # Indigo for class 19
            QColor(173, 255, 47),     # Green Yellow for class 20
            QColor(255, 215, 0),      # Gold for class 21
            QColor(218, 165, 32),     # Golden Brown for class 22
            QColor(139, 69, 19),      # Saddle Brown for class 23
            QColor(255, 105, 180),    # Hot Pink for class 24
            QColor(127, 255, 212),    # Aquamarine for class 25
            QColor(106, 90, 205),     # Slate Blue for class 26
            QColor(34, 139, 34),      # Forest Green for class 27
            QColor(250, 128, 114),    # Salmon for class 28
            QColor(0, 139, 139),      # Dark Cyan for class 29
            QColor(255, 250, 240),    # Floral White for class 30
            QColor(255, 228, 181),    # Moccasin for class 31
            QColor(220, 20, 60),      # Crimson for class 32
            QColor(0, 206, 209),      # Dark Turquoise for class 33
            QColor(186, 85, 211),     # Medium Orchid for class 34
            QColor(240, 230, 140),    # Khaki for class 35
            QColor(60, 179, 113),     # Medium Sea Green for class 36
            QColor(255, 182, 193),    # Light Pink for class 37
            QColor(205, 133, 63),     # Peru for class 38
            QColor(107, 142, 35),     # Olive Drab for class 39
            QColor(153, 50, 204),     # Dark Orchid for class 40
            QColor(245, 245, 220),    # Beige for class 41
            QColor(176, 224, 230),    # Powder Blue for class 42
            QColor(238, 232, 170),    # Pale Goldenrod for class 43
            QColor(255, 222, 173),    # Navajo White for class 44
            QColor(210, 105, 30),     # Chocolate for class 45
            QColor(216, 191, 216),    # Thistle for class 46
            QColor(144, 238, 144),    # Light Green for class 47
            QColor(189, 183, 107),    # Dark Khaki for class 48
            QColor(255, 240, 245),    # Lavender Blush for class 49
            QColor(173, 216, 230),    # Light Blue for class 50
            QColor(240, 128, 128),    # Light Coral for class 51
            QColor(102, 205, 170),    # Medium Aquamarine for class 52
            QColor(147, 112, 219),    # Medium Purple for class 53
            QColor(255, 140, 0),      # Dark Orange for class 54
            QColor(255, 255, 224),    # Light Yellow for class 55
            QColor(221, 160, 221),    # Plum for class 56
            QColor(143, 188, 143),    # Dark Sea Green for class 57
            QColor(211, 211, 211),    # Light Grey for class 58
            QColor(218, 112, 214),    # Orchid for class 59
            QColor(244, 164, 96),     # Sandy Brown for class 60
            QColor(250, 235, 215),    # Antique White for class 61
            QColor(112, 128, 144),    # Slate Gray for class 62
            QColor(175, 238, 238),    # Pale Turquoise for class 63
            QColor(176, 196, 222),    # Light Steel Blue for class 64
            QColor(255, 239, 213),    # Papaya Whip for class 65
            QColor(184, 134, 11),     # Dark Goldenrod for class 66
            QColor(135, 206, 235),    # Sky Blue for class 67
            QColor(255, 248, 220),    # Cornsilk for class 68
            QColor(160, 82, 45),      # Sienna for class 69
            QColor(188, 143, 143),    # Rosy Brown for class 70
            QColor(124, 252, 0),      # Lawn Green for class 71
            QColor(255, 250, 205),    # Lemon Chiffon for class 72
            QColor(199, 21, 133),     # Medium Violet Red for class 73
            QColor(169, 169, 169),    # Dark Gray for class 74
            QColor(255, 218, 185),    # Peach Puff for class 75
            QColor(205, 92, 92),      # Indian Red for class 76
            QColor(139, 137, 137),    # Dim Gray for class 77
            QColor(240, 255, 255),    # Azure for class 78
            QColor(255, 228, 225),    # Misty Rose for class 79
        ]
        font = QFont("Arial", 10)

        for annotation in self.current_annotations:
            class_id, x_center, y_center, width, height = annotation
            color = colors[int(class_id) % len(colors)]

            for item in self.scene.items():
                if isinstance(item, QGraphicsPixmapItem):
                    pixmap = item.pixmap()
                    rect = QRectF(
                        (x_center - width / 2) * pixmap.width(),
                        (y_center - height / 2) * pixmap.height(),
                        width * pixmap.width(),
                        height * pixmap.height()
                    )
                    self.scene.addRect(rect, QPen(color, 2))
                    
                    class_name = self.class_list[int(class_id)] if int(class_id) < len(self.class_list) else "Unknown"
                    class_label = QGraphicsTextItem()
                    class_label.setPlainText(class_name)
                    class_label.setDefaultTextColor(color)
                    class_label.setFont(font)
                    class_label.setPos(rect.left() + 2, rect.top() + 2)
                    self.scene.addItem(class_label)
                    break

    def view_annotations(self):
        if not self.completed_folder:
            QMessageBox.warning(self, "Warning", "Completed folder not selected!")
            return
        
        self.viewing_mode = True
        self.image_files = [os.path.join(self.completed_folder, f) for f in os.listdir(self.completed_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not self.image_files:
            QMessageBox.warning(self, "Warning", "No images found in the completed folder!")
            self.viewing_mode = False
            return
        
        # Try to maintain the current image index if possible
        current_image_name = os.path.basename(self.current_image_path) if self.current_image_path else ""
        try:
            self.current_image_index = self.image_files.index(os.path.join(self.completed_folder, current_image_name))
        except ValueError:
            # If the current image isn't in the completed folder, default to the first image
            self.current_image_index = 0

    def load_next_annotation(self):
        if self.image_files:
            self.current_image_path = self.image_files[self.current_image_index]
            self.current_annotations = self.load_annotations_from_file(self.current_image_path)
            self.update_scene()

    def load_annotations_from_file(self, image_path):
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        txt_file = os.path.join(self.completed_folder, f"{base_name}.txt")
        annotations = []
        if os.path.exists(txt_file):
            with open(txt_file, "r") as f:
                for line in f:
                    parts = line.split()
                    if len(parts) == 5:
                        annotations.append(tuple(map(float, parts)))
        return annotations

# Main application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnnotationTool()
    window.show()
    sys.exit(app.exec_())