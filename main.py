import sys
import os

from PyQt6.QtWidgets import (QApplication, QMainWindow, QSplitter, QTreeView, 
                             QGraphicsView, QGraphicsScene, QStackedWidget, QListWidget,
                             QListWidgetItem, QListView, QComboBox, QWidget, QSizePolicy,
                             QToolBar, QMessageBox, QDialog, QVBoxLayout, QLabel, QMenu,
                             QHBoxLayout, QPushButton, QProgressDialog,
                             QSlider, QSpinBox, QDoubleSpinBox, QGroupBox, QCheckBox)
from PyQt6.QtGui import QPixmap, QAction, QIcon, QTransform, QFileSystemModel, QImageReader, QImage, QPainter, QColor, QPen, QFont, QBrush, QPageSize
from PyQt6.QtCore import Qt, QDir, QFileInfo, QSize, QThread, pyqtSignal, QSizeF
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw, ImageFont


# 313 ab cluster centers from pts_in_hull.npy (for colorization)
HULL_PTS = [
    -90., -90., -90., -90., -90., -80., -80., -80., -80., -80., -80., -80., -80., -70., -70., -70., -70., -70., -70., -70., -70.,
    -70., -70., -60., -60., -60., -60., -60., -60., -60., -60., -60., -60., -60., -60., -50., -50., -50., -50., -50., -50., -50., -50.,
    -50., -50., -50., -50., -50., -50., -40., -40., -40., -40., -40., -40., -40., -40., -40., -40., -40., -40., -40., -40., -40., -30.,
    -30., -30., -30., -30., -30., -30., -30., -30., -30., -30., -30., -30., -30., -30., -30., -20., -20., -20., -20., -20., -20., -20.,
    -20., -20., -20., -20., -20., -20., -20., -20., -20., -10., -10., -10., -10., -10., -10., -10., -10., -10., -10., -10., -10., -10.,
    -10., -10., -10., -10., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 10., 10., 10., 10., 10., 10., 10.,
    10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 20., 20., 20., 20., 20., 20., 20., 20., 20., 20., 20., 20., 20., 20., 20.,
    20., 20., 20., 30., 30., 30., 30., 30., 30., 30., 30., 30., 30., 30., 30., 30., 30., 30., 30., 30., 30., 30., 40., 40., 40., 40.,
    40., 40., 40., 40., 40., 40., 40., 40., 40., 40., 40., 40., 40., 40., 40., 40., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.,
    50., 50., 50., 50., 50., 50., 50., 50., 50., 60., 60., 60., 60., 60., 60., 60., 60., 60., 60., 60., 60., 60., 60., 60., 60., 60.,
    60., 60., 60., 70., 70., 70., 70., 70., 70., 70., 70., 70., 70., 70., 70., 70., 70., 70., 70., 70., 70., 70., 70., 80., 80., 80.,
    80., 80., 80., 80., 80., 80., 80., 80., 80., 80., 80., 80., 80., 80., 80., 80., 90., 90., 90., 90., 90., 90., 90., 90., 90., 90.,
    90., 90., 90., 90., 90., 90., 90., 90., 90., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 50., 60., 70., 80., 90.,
    20., 30., 40., 50., 60., 70., 80., 90., 0., 10., 20., 30., 40., 50., 60., 70., 80., 90., -20., -10., 0., 10., 20., 30., 40., 50.,
    60., 70., 80., 90., -30., -20., -10., 0., 10., 20., 30., 40., 50., 60., 70., 80., 90., 100., -40., -30., -20., -10., 0., 10., 20.,
    30., 40., 50., 60., 70., 80., 90., 100., -50., -40., -30., -20., -10., 0., 10., 20., 30., 40., 50., 60., 70., 80., 90., 100., -50.,
    -40., -30., -20., -10., 0., 10., 20., 30., 40., 50., 60., 70., 80., 90., 100., -60., -50., -40., -30., -20., -10., 0., 10., 20.,
    30., 40., 50., 60., 70., 80., 90., 100., -70., -60., -50., -40., -30., -20., -10., 0., 10., 20., 30., 40., 50., 60., 70., 80., 90.,
    100., -80., -70., -60., -50., -40., -30., -20., -10., 0., 10., 20., 30., 40., 50., 60., 70., 80., 90., -80., -70., -60., -50.,
    -40., -30., -20., -10., 0., 10., 20., 30., 40., 50., 60., 70., 80., 90., -90., -80., -70., -60., -50., -40., -30., -20., -10.,
    0., 10., 20., 30., 40., 50., 60., 70., 80., 90., -100., -90., -80., -70., -60., -50., -40., -30., -20., -10., 0., 10., 20., 30.,
    40., 50., 60., 70., 80., 90., -100., -90., -80., -70., -60., -50., -40., -30., -20., -10., 0., 10., 20., 30., 40., 50., 60., 70.,
    80., -110., -100., -90., -80., -70., -60., -50., -40., -30., -20., -10., 0., 10., 20., 30., 40., 50., 60., 70., 80., -110., -100.,
    -90., -80., -70., -60., -50., -40., -30., -20., -10., 0., 10., 20., 30., 40., 50., 60., 70., 80., -110., -100., -90., -80., -70.,
    -60., -50., -40., -30., -20., -10., 0., 10., 20., 30., 40., 50., 60., 70., -110., -100., -90., -80., -70., -60., -50., -40., -30.,
    -20., -10., 0., 10., 20., 30., 40., 50., 60., 70., -90., -80., -70., -60., -50., -40., -30., -20., -10., 0.,
]

MODEL_URLS = {
    "prototxt": "https://raw.githubusercontent.com/richzhang/colorization/caffe/models/colorization_deploy_v2.prototxt",
    "caffemodel": "https://huggingface.co/spaces/viveknarayan/Image_Colorization/resolve/main/colorization_release_v2.caffemodel",
    "candy.t7": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/candy.t7",
    "la_muse.t7": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/la_muse.t7",
    "mosaic.t7": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/mosaic.t7",
    "feathers.t7": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/feathers.t7",
    "the_scream.t7": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/the_scream.t7",
    "udnie.t7": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/udnie.t7",
    "starry_night.t7": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/starry_night.t7",
    "the_wave.t7": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/the_wave.t7",
    "composition_vii.t7": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/composition_vii.t7",
}


def get_model_dir():
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
    os.makedirs(model_dir, exist_ok=True)
    return model_dir


def ensure_models(transform_type, progress_callback=None):
    """Download AI models if missing. Returns list of required model paths."""
    model_dir = get_model_dir()

    if transform_type == "colorize":
        required = ["prototxt", "caffemodel"]
    elif transform_type.startswith("style_"):
        style_name = transform_type.replace("style_", "") + ".t7"
        required = [style_name]
    else:
        return []

    import urllib.request
    downloaded = []
    for name in required:
        path = os.path.join(model_dir, name)
        if not os.path.exists(path):
            if progress_callback:
                progress_callback(f"正在下載模型: {name}...")
            try:
                urllib.request.urlretrieve(MODEL_URLS[name], path)
            except Exception as e:
                raise RuntimeError(f"模型下載失敗 ({name}): {e}")
        downloaded.append(path)
    return downloaded


class AIImageWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    STYLE_NAMES = {
        "style_candy": "Candy",
        "style_la_muse": "La Muse",
        "style_mosaic": "Mosaic",
        "style_feathers": "Feathers",
        "style_the_scream": "The Scream",
        "style_udnie": "Udnie",
        "style_starry_night": "Starry Night (梵谷)",
        "style_the_wave": "The Wave (神奈川沖浪裏)",
        "style_composition_vii": "Composition VII",
    }

    def __init__(self, image_path, transform_type):
        super().__init__()
        self.image_path = image_path
        self.transform_type = transform_type

    def run(self):
        try:
            import cv2
            import numpy as np

            img = cv2.imread(self.image_path)
            if img is None:
                self.error.emit(f"無法讀取圖片：{self.image_path}")
                return

            if self.transform_type == "upscale":
                result = self._upscale(img)
            elif self.transform_type == "colorize":
                result = self._colorize(img)
            elif self.transform_type.startswith("style_"):
                result = self._style_transfer(img)
            else:
                self.error.emit(f"未知的轉換類型：{self.transform_type}")
                return

            dir_name = os.path.dirname(self.image_path)
            base_name = os.path.basename(self.image_path)
            name, _ = os.path.splitext(base_name)
            new_path = os.path.join(dir_name, f"{name}_{self.transform_type}.png")
            cv2.imwrite(new_path, result)
            self.finished.emit(new_path)

        except ImportError:
            self.error.emit("需要安裝 opencv-python-headless\n請執行：pip install opencv-python-headless")
        except Exception as e:
            self.error.emit(str(e))

    def _colorize(self, img):
        import cv2
        import numpy as np

        model_paths = ensure_models("colorize")
        prototxt, caffemodel = model_paths

        net = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)

        # conv8_313_rh is a Scale layer (bias_term: false): constant weight = 2.606
        net.getLayer("conv8_313_rh").blobs = [
            np.full((1, 313, 1, 1), 2.606, dtype=np.float32),
        ]

        # class8_ab is Convolution 313->2: ab cluster centers weight + zero bias
        pts = np.array(HULL_PTS, dtype=np.float32).reshape(2, 313, 1, 1)
        net.getLayer("class8_ab").blobs = [pts, np.zeros((2,), dtype=np.float32)]

        h, w = img.shape[:2]
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_float = img_rgb.astype(np.float32) / 255.0

        lab = cv2.cvtColor(img_float, cv2.COLOR_RGB2Lab)
        L = lab[:, :, 0]

        input_blob = cv2.dnn.blobFromImage(
            cv2.resize(L, (224, 224)),
            scalefactor=1.0,
            mean=50,
        )
        net.setInput(input_blob)
        result = net.forward()  # (1, 2, 224, 224)

        a = cv2.resize(result[0, 0], (w, h))
        b = cv2.resize(result[0, 1], (w, h))

        lab_out = np.zeros((h, w, 3), dtype=np.float32)
        lab_out[:, :, 0] = np.clip(L, 0, 100)
        lab_out[:, :, 1] = a
        lab_out[:, :, 2] = b

        rgb_out = cv2.cvtColor(lab_out, cv2.COLOR_Lab2RGB)
        rgb_out = np.clip(rgb_out * 255, 0, 255).astype(np.uint8)
        return cv2.cvtColor(rgb_out, cv2.COLOR_RGB2BGR)

    def _style_transfer(self, img):
        import cv2
        import numpy as np

        style_name = self.transform_type.replace("style_", "") + ".t7"
        model_paths = ensure_models(self.transform_type)
        model_path = model_paths[0]

        net = cv2.dnn.readNetFromTorch(model_path)

        h, w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, scalefactor=1.0, size=(w, h),
                                     mean=(103.939, 116.779, 123.680),
                                     swapRB=False, crop=False)
        net.setInput(blob)
        output = net.forward()

        output = output.reshape((3, output.shape[2], output.shape[3]))
        output = output.transpose(1, 2, 0)
        output += (103.939, 116.779, 123.680)
        output = np.clip(output, 0, 255).astype(np.uint8)
        return output

    def _upscale(self, img):
        import cv2
        h, w = img.shape[:2]
        scale = 2.0
        new_w, new_h = int(w * scale), int(h * scale)
        upscaled = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

        sharpen = cv2.GaussianBlur(upscaled, (0, 0), 3.0)
        result = cv2.addWeighted(upscaled, 1.5, sharpen, -0.5, 0)
        return result


class LocalImageWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    SUFFIX_MAP = {
        "grayscale": "_bw",
        "emboss": "_emboss",
        "edge_detect": "_edges",
        "blur": "_blur",
        "sharpen": "_sharpen",
        "warm": "_warm",
        "cool": "_cool",
        "sepia": "_sepia",
        "brightness_contrast": "_adjust",
        "color_balance": "_adjust",
    }

    def __init__(self, image_path, operation, params=None):
        super().__init__()
        self.image_path = image_path
        self.operation = operation
        self.params = params or {}

    def run(self):
        try:
            img = Image.open(self.image_path)
            img = ImageOps.exif_transpose(img)

            if img.mode == 'RGBA':
                bg = Image.new('RGB', img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                img = bg
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            result = self.apply_operation(img)

            dir_name = os.path.dirname(self.image_path)
            base_name = os.path.basename(self.image_path)
            name, _ = os.path.splitext(base_name)
            suffix = self.SUFFIX_MAP.get(self.operation, "_processed")
            new_path = os.path.join(dir_name, f"{name}{suffix}.png")

            result.save(new_path)
            self.finished.emit(new_path)

        except Exception as e:
            self.error.emit(str(e))

    def apply_operation(self, img):
        op = self.operation

        if op == "grayscale":
            return ImageOps.grayscale(img).convert('RGB')

        elif op == "emboss":
            return img.filter(ImageFilter.EMBOSS)

        elif op == "edge_detect":
            return img.filter(ImageFilter.FIND_EDGES)

        elif op == "blur":
            radius = self.params.get("radius", 5)
            return img.filter(ImageFilter.GaussianBlur(radius=radius))

        elif op == "sharpen":
            return img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

        elif op == "warm":
            r, g, b = img.split()
            r = r.point(lambda i: min(255, int(i * 1.15)))
            b = b.point(lambda i: int(i * 0.85))
            return Image.merge('RGB', (r, g, b))

        elif op == "cool":
            r, g, b = img.split()
            r = r.point(lambda i: int(i * 0.85))
            b = b.point(lambda i: min(255, int(i * 1.15)))
            return Image.merge('RGB', (r, g, b))

        elif op == "sepia":
            gray = ImageOps.grayscale(img)
            r_lut = [min(255, int(v * 1.2 + 40)) for v in range(256)]
            g_lut = [min(255, int(v * 1.0 + 20)) for v in range(256)]
            b_lut = [min(255, int(v * 0.8)) for v in range(256)]
            r = gray.point(r_lut)
            g = gray.point(g_lut)
            b = gray.point(b_lut)
            return Image.merge('RGB', (r, g, b))

        elif op == "brightness_contrast":
            brightness = self.params.get("brightness", 1.0)
            contrast = self.params.get("contrast", 1.0)
            img = ImageEnhance.Brightness(img).enhance(brightness)
            img = ImageEnhance.Contrast(img).enhance(contrast)
            return img

        elif op == "color_balance":
            r_factor = self.params.get("red", 1.0)
            g_factor = self.params.get("green", 1.0)
            b_factor = self.params.get("blue", 1.0)
            r, g, b = img.split()
            r = r.point(lambda i: min(255, int(i * r_factor)))
            g = g.point(lambda i: min(255, int(i * g_factor)))
            b = b.point(lambda i: min(255, int(i * b_factor)))
            return Image.merge('RGB', (r, g, b))

        return img


class AdjustmentDialog(QDialog):
    def __init__(self, title, sliders_config, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(380, 220)

        layout = QVBoxLayout()
        self.sliders = {}

        for name, config in sliders_config.items():
            row = QVBoxLayout()
            label = QLabel(f"{config['label']}: {config['default']:.1f}")

            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(int(config['min'] * 100), int(config['max'] * 100))
            slider.setValue(int(config['default'] * 100))
            slider.valueChanged.connect(
                lambda v, lbl=label, cfg=config: lbl.setText(f"{cfg['label']}: {v/100:.1f}")
            )

            row.addWidget(label)
            row.addWidget(slider)
            layout.addLayout(row)
            self.sliders[name] = slider

        buttons = QHBoxLayout()
        ok_btn = QPushButton("套用 (Apply)")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("取消 (Cancel)")
        cancel_btn.clicked.connect(self.reject)
        buttons.addStretch()
        buttons.addWidget(ok_btn)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)

        self.setLayout(layout)

    def get_values(self):
        return {name: slider.value() / 100.0 for name, slider in self.sliders.items()}


PAPER_SIZES = {
    "A4": (210.0, 297.0),
    "A3": (297.0, 420.0),
    "A5": (148.0, 210.0),
    "A2": (420.0, 594.0),
    "Letter": (215.9, 279.4),
    "Legal": (215.9, 355.6),
    "B4": (250.0, 353.0),
    "B5": (176.0, 250.0),
}

PRINT_DPI = 300


def pil_to_qimage(pil_img):
    if pil_img.mode != "RGBA":
        pil_img = pil_img.convert("RGBA")
    data = pil_img.tobytes("raw", "RGBA")
    return QImage(data, pil_img.width, pil_img.height, QImage.Format.Format_RGBA8888)


class SplitPrintDialog(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.setWindowTitle("分割列印 - 預覽")
        self.resize(1000, 700)

        self.pil_image = Image.open(image_path)
        self.pil_image = ImageOps.exif_transpose(self.pil_image)
        if self.pil_image.mode != "RGB":
            self.pil_image = self.pil_image.convert("RGB")

        # Settings
        self.paper_key = "A4"
        self.orientation = "portrait"
        self.margin_mm = 10.0
        self.overlap_mm = 5.0
        self.cols = 2
        self.rows = 2

        self.setup_ui()
        self.update_preview()

    def setup_ui(self):
        self.resize(1100, 720)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- Preview ---
        preview_container = QWidget()
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_label = QLabel("  📐 分割預覽 (紅線 = 每頁邊界)")
        self.preview_scene = QGraphicsScene()
        self.preview_view = QGraphicsView(self.preview_scene)
        self.preview_view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.preview_view.setStyleSheet("background: #2d2d2d; border: 1px solid #555;")
        preview_layout.addWidget(preview_label)
        preview_layout.addWidget(self.preview_view)

        # --- Controls ---
        controls_container = QWidget()
        controls_container.setMinimumWidth(280)
        controls_container.setMaximumWidth(320)
        controls = QVBoxLayout(controls_container)
        controls.setContentsMargins(4, 4, 4, 4)
        controls.setSpacing(6)

        # Paper
        g1 = QGroupBox("紙張設定")
        g1_layout = QVBoxLayout(g1)
        self.paper_combo = QComboBox()
        for k in PAPER_SIZES:
            self.paper_combo.addItem(k, k)
        self.paper_combo.currentIndexChanged.connect(self.on_setting_changed)
        g1_layout.addWidget(QLabel("紙張大小:"))
        g1_layout.addWidget(self.paper_combo)

        orient_row = QHBoxLayout()
        self.portrait_cb = QCheckBox("直向")
        self.portrait_cb.setChecked(True)
        self.portrait_cb.toggled.connect(self.on_setting_changed)
        self.landscape_cb = QCheckBox("橫向")
        self.landscape_cb.toggled.connect(self.on_setting_changed)
        orient_row.addWidget(self.portrait_cb)
        orient_row.addWidget(self.landscape_cb)
        g1_layout.addLayout(orient_row)

        self.margin_spin = QDoubleSpinBox()
        self.margin_spin.setRange(0, 50)
        self.margin_spin.setValue(10)
        self.margin_spin.setSuffix(" mm")
        self.margin_spin.valueChanged.connect(self.on_setting_changed)
        g1_layout.addWidget(QLabel("邊距:"))
        g1_layout.addWidget(self.margin_spin)
        controls.addWidget(g1)

        # Pages
        g2 = QGroupBox("分割設定")
        g2_layout = QVBoxLayout(g2)
        col_row = QHBoxLayout()
        col_row.addWidget(QLabel("欄:"))
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(1, 20)
        self.cols_spin.setValue(2)
        self.cols_spin.valueChanged.connect(self.on_setting_changed)
        col_row.addWidget(self.cols_spin)
        col_row.addWidget(QLabel("行:"))
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(1, 20)
        self.rows_spin.setValue(2)
        self.rows_spin.valueChanged.connect(self.on_setting_changed)
        col_row.addWidget(self.rows_spin)
        g2_layout.addLayout(col_row)

        self.overlap_spin = QDoubleSpinBox()
        self.overlap_spin.setRange(0, 50)
        self.overlap_spin.setValue(5)
        self.overlap_spin.setSuffix(" mm")
        self.overlap_spin.valueChanged.connect(self.on_setting_changed)
        g2_layout.addWidget(QLabel("重疊:"))
        g2_layout.addWidget(self.overlap_spin)
        controls.addWidget(g2)

        # Info
        g3 = QGroupBox("資訊")
        self.info_label = QLabel("載入中...")
        self.info_label.setWordWrap(True)
        g3_layout = QVBoxLayout(g3)
        g3_layout.addWidget(self.info_label)
        controls.addWidget(g3)

        # Page Preview
        g4 = QGroupBox("單頁預覽")
        g4_layout = QVBoxLayout(g4)
        page_sel = QHBoxLayout()
        page_sel.addWidget(QLabel("頁碼:"))
        self.page_spin = QSpinBox()
        self.page_spin.setRange(1, 1)
        self.page_spin.valueChanged.connect(self.update_page_preview)
        page_sel.addWidget(self.page_spin)
        g4_layout.addLayout(page_sel)
        self.page_preview_label = QLabel()
        self.page_preview_label.setMinimumSize(200, 200)
        self.page_preview_label.setStyleSheet(
            "background: #3d3d3d; border: 1px solid #666;"
        )
        self.page_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        g4_layout.addWidget(self.page_preview_label)
        controls.addWidget(g4)

        controls.addStretch()

        # Action buttons
        btn_row = QHBoxLayout()
        self.print_btn = QPushButton("🖨️ 列印")
        self.print_btn.setStyleSheet(
            "QPushButton { background: #2196F3; color: white; padding: 6px 12px;"
            " font-weight: bold; border-radius: 3px; }"
            "QPushButton:hover { background: #1976D2; }"
        )
        self.print_btn.clicked.connect(self.do_print)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(self.print_btn)
        btn_row.addWidget(cancel_btn)
        controls.addLayout(btn_row)

        splitter.addWidget(preview_container)
        splitter.addWidget(controls_container)
        splitter.setSizes([780, 320])
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(splitter)

    def get_paper_dims(self):
        w, h = PAPER_SIZES[self.paper_key]
        if self.orientation == "landscape":
            return max(w, h), min(w, h)
        return min(w, h), max(w, h)

    def on_setting_changed(self):
        self.paper_key = self.paper_combo.currentData()
        self.orientation = "landscape" if self.landscape_cb.isChecked() else "portrait"
        self.margin_mm = self.margin_spin.value()
        self.overlap_mm = self.overlap_spin.value()
        self.cols = self.cols_spin.value()
        self.rows = self.rows_spin.value()
        self.update_preview()

    def calculate_layout(self):
        pw, ph = self.get_paper_dims()
        printable_w = pw - 2 * self.margin_mm
        printable_h = ph - 2 * self.margin_mm
        step_x = printable_w - self.overlap_mm
        step_y = printable_h - self.overlap_mm

        img_w, img_h = self.pil_image.size
        img_w_mm = img_w * 25.4 / PRINT_DPI
        img_h_mm = img_h * 25.4 / PRINT_DPI

        # Scale image to cover the total poster grid (may crop edges)
        total_w_mm = (self.cols - 1) * step_x + printable_w
        total_h_mm = (self.rows - 1) * step_y + printable_h
        scale = max(total_w_mm / img_w_mm, total_h_mm / img_h_mm)

        px_per_mm = PRINT_DPI / 25.4

        pages = []
        for r in range(self.rows):
            for c in range(self.cols):
                x_mm = c * step_x
                y_mm = r * step_y
                pages.append({
                    "x_mm": x_mm,
                    "y_mm": y_mm,
                    "w_mm": printable_w,
                    "h_mm": printable_h,
                    "col": c,
                    "row": r,
                    "index": r * self.cols + c + 1,
                    "has_image": (
                        x_mm < img_w_mm * scale and y_mm < img_h_mm * scale
                        and x_mm + printable_w > 0 and y_mm + printable_h > 0
                    ),
                })

        return {
            "pages": pages,
            "cols": self.cols,
            "rows": self.rows,
            "scale_pct": scale * 100,
            "printable_w_mm": printable_w,
            "printable_h_mm": printable_h,
            "total_w_mm": total_w_mm,
            "total_h_mm": total_h_mm,
            "img_w_mm": img_w_mm,
            "img_h_mm": img_h_mm,
            "step_x": step_x,
            "step_y": step_y,
            "scale": scale,
            "px_per_mm": PRINT_DPI / 25.4,
            "orig_px_per_mm": img_w / (img_w_mm * scale),
            "orig_px_mm_y": img_h / (img_h_mm * scale),
        }

    def update_preview(self):
        self.preview_scene.clear()
        info = self.calculate_layout()

        img_w, img_h = self.pil_image.size
        w_ratio = info["orig_px_per_mm"]
        h_ratio = info["orig_px_mm_y"]

        # Render full image on a canvas at preview resolution
        vp = self.preview_view.viewport()
        max_w = max(vp.width() - 10, 200) if vp else 600
        max_h = max(vp.height() - 10, 200) if vp else 500
        pscale = min(max_w / max(img_w, 1), max_h / max(img_h, 1), 1.0)

        pw = max(int(img_w * pscale), 1)
        ph = max(int(img_h * pscale), 1)
        canvas = self.pil_image.resize((pw, ph), Image.LANCZOS)

        # Draw page grid
        d = ImageDraw.Draw(canvas)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc",
                                      max(11, int(14 * pscale)))
        except Exception:
            font = None

        lw = max(2, int(3 * pscale))
        for p in info["pages"]:
            x1 = p["x_mm"] * w_ratio * pscale
            y1 = p["y_mm"] * h_ratio * pscale
            x2 = (p["x_mm"] + p["w_mm"]) * w_ratio * pscale
            y2 = (p["y_mm"] + p["h_mm"]) * h_ratio * pscale

            cx1 = max(0, int(x1)); cy1 = max(0, int(y1))
            cx2 = min(pw, int(x2)); cy2 = min(ph, int(y2))
            if cx2 <= cx1 or cy2 <= cy1:
                continue

            d.rectangle([cx1, cy1, cx2, cy2], outline=(220, 40, 40), width=lw)

            if font:
                d.text((cx1 + 4, cy1 + 2), f"P{p['index']}", fill=(220, 40, 40), font=font)

        qimg = pil_to_qimage(canvas)
        pixmap = QPixmap.fromImage(qimg)
        item = self.preview_scene.addPixmap(pixmap)
        self.preview_scene.setSceneRect(item.boundingRect())

        # Update info
        pp = info
        total_pages = pp["cols"] * pp["rows"]
        has_img_count = sum(1 for p in pp["pages"] if p["has_image"])
        self.info_label.setText(
            f"原始尺寸: {img_w}x{img_h} px\n"
            f"({pp['img_w_mm']:.0f}x{pp['img_h_mm']:.0f} mm @ {PRINT_DPI} DPI)\n"
            f"列印比例: {pp['scale_pct']:.1f}%\n"
            f"頁數: {pp['cols']} x {pp['rows']} = {total_pages} ({has_img_count} 有效)\n"
            f"每頁: {pp['printable_w_mm']:.0f}x{pp['printable_h_mm']:.0f} mm"
        )

        total = len(pp["pages"])
        self.page_spin.blockSignals(True)
        self.page_spin.setRange(1, max(total, 1))
        self.page_spin.blockSignals(False)
        self.update_page_preview()

    def render_page_pixmap(self, page_info):
        """Render a single page as a QPixmap for preview."""
        info = self.calculate_layout()
        img_w, img_h = self.pil_image.size
        rx = info["orig_px_per_mm"]
        ry = info["orig_px_mm_y"]

        x0 = int(page_info["x_mm"] * rx)
        y0 = int(page_info["y_mm"] * ry)
        cw = int(page_info["w_mm"] * rx)
        ch = int(page_info["h_mm"] * ry)

        x0 = max(0, x0)
        y0 = max(0, y0)
        cw = min(cw, img_w - x0)
        ch = min(ch, img_h - y0)

        if cw <= 0 or ch <= 0:
            return QPixmap()

        crop = self.pil_image.crop((x0, y0, x0 + cw, y0 + ch))
        qimg = pil_to_qimage(crop)
        pm = QPixmap.fromImage(qimg)
        return pm.scaled(
            260, 260,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    def update_page_preview(self):
        info = self.calculate_layout()
        idx = self.page_spin.value() - 1
        if 0 <= idx < len(info["pages"]):
            pm = self.render_page_pixmap(info["pages"][idx])
            self.page_preview_label.setPixmap(pm)

    def do_print(self):
        info = self.calculate_layout()

        printer = QPrinter()
        printer.setFullPage(True)
        printer.setResolution(PRINT_DPI)

        pw, ph = self.get_paper_dims()
        if self.orientation == "landscape":
            size = QPageSize(QSizeF(ph, pw), QPageSize.Unit.Millimeter)
        else:
            size = QPageSize(QSizeF(pw, ph), QPageSize.Unit.Millimeter)
        printer.setPageSize(size)

        dialog = QPrintDialog(printer, self)
        dialog.setWindowTitle("列印分割海報")
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        painter = QPainter()
        painter.begin(printer)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        page_w = printer.width()
        page_h = printer.height()

        printed = 0
        for i, p in enumerate(info["pages"]):
            if not p["has_image"]:
                continue

            # Page region in mm -> crop region in original image pixels
            img_w, img_h = self.pil_image.size
            rx = info["orig_px_per_mm"]
            ry = info["orig_px_mm_y"]
            x0 = int(p["x_mm"] * rx)
            y0 = int(p["y_mm"] * ry)
            cw = int(p["w_mm"] * rx)
            ch = int(p["h_mm"] * ry)

            x0 = max(0, x0)
            y0 = max(0, y0)
            cw = min(cw, img_w - x0)
            ch = min(ch, img_h - y0)

            if cw <= 0 or ch <= 0:
                continue

            crop = self.pil_image.crop((x0, y0, x0 + cw, y0 + ch))
            qimg = pil_to_qimage(crop)
            pm = QPixmap.fromImage(qimg).scaled(
                page_w, page_h,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            x = (page_w - pm.width()) // 2
            y = (page_h - pm.height()) // 2
            painter.drawPixmap(int(x), int(y), pm)

            printed += 1
            if printed < sum(1 for pp in info["pages"] if pp["has_image"]):
                printer.newPage()

        painter.end()
        QMessageBox.information(self, "列印完成",
            f"已傳送 {printed} 頁至印表機。")

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AetherLens")
        self.resize(1024, 768)

        # Setup Splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(self.splitter)

        # Left Panel (File System - Directories Only)
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath("")
        self.file_model.setFilter(QDir.Filter.AllDirs | QDir.Filter.NoDotAndDotDot)

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        
        home_path = QDir.homePath()
        self.tree_view.setRootIndex(self.file_model.index(home_path))
        
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)

        self.tree_view.selectionModel().selectionChanged.connect(self.on_dir_selected)

        # Right Panel (Stacked Widget)
        self.stacked_widget = QStackedWidget()
        
        # 1. Thumbnail/List View
        self.thumbnail_view = QListWidget()
        self.thumbnail_view.setViewMode(QListView.ViewMode.IconMode)
        self.thumbnail_view.setIconSize(QSize(150, 150))
        self.thumbnail_view.setGridSize(QSize(180, 210))
        self.thumbnail_view.setResizeMode(QListView.ResizeMode.Adjust)
        self.thumbnail_view.setSpacing(15)
        self.thumbnail_view.setWordWrap(True)
        self.thumbnail_view.itemDoubleClicked.connect(self.on_thumbnail_double_clicked)
        self.thumbnail_view.itemSelectionChanged.connect(self.update_toolbar_state)
        self.thumbnail_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.thumbnail_view.customContextMenuRequested.connect(self.show_thumbnail_context_menu)

        # 2. Single Image View
        self.scene = QGraphicsScene()
        self.single_view = QGraphicsView(self.scene)
        self.single_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.single_view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.single_view.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.single_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.single_view.customContextMenuRequested.connect(self.show_single_image_context_menu)

        self.stacked_widget.addWidget(self.thumbnail_view) # Index 0
        self.stacked_widget.addWidget(self.single_view)    # Index 1

        self.splitter.addWidget(self.tree_view)
        self.splitter.addWidget(self.stacked_widget)
        self.splitter.setSizes([250, 774])

        self.current_image_path = None
        self.current_image_index = -1
        self.pixmap_item = None
        self.current_scale = 1.0
        
        self.worker = None

        self.setup_toolbar()
        self.update_toolbar_state()

    def setup_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)

        # View Mode Switcher (Grid vs List)
        self.view_mode_combo = QComboBox()
        self.view_mode_combo.addItem("🔲 縮圖")
        self.view_mode_combo.addItem("📄 清單")
        self.view_mode_combo.currentIndexChanged.connect(self.change_view_mode)
        self.view_mode_combo.setToolTip("Switch View Mode")
        toolbar.addWidget(self.view_mode_combo)

        toolbar.addSeparator()

        # Back to Thumbnails
        self.back_action = QAction("⬅️ 返回", self)
        self.back_action.setToolTip("Back to Thumbnails")
        self.back_action.triggered.connect(self.show_thumbnails_mode)
        toolbar.addAction(self.back_action)

        toolbar.addSeparator()

        # Previous Image
        self.prev_action = QAction("◀️", self)
        self.prev_action.setToolTip("Previous Image")
        self.prev_action.triggered.connect(self.prev_image)
        toolbar.addAction(self.prev_action)

        # Next Image
        self.next_action = QAction("▶️", self)
        self.next_action.setToolTip("Next Image")
        self.next_action.triggered.connect(self.next_image)
        toolbar.addAction(self.next_action)

        toolbar.addSeparator()

        # Zoom In
        self.zoom_in_action = QAction("🔍+", self)
        self.zoom_in_action.setToolTip("Zoom In")
        self.zoom_in_action.triggered.connect(self.zoom_in)
        toolbar.addAction(self.zoom_in_action)

        # Zoom Out
        self.zoom_out_action = QAction("🔍-", self)
        self.zoom_out_action.setToolTip("Zoom Out")
        self.zoom_out_action.triggered.connect(self.zoom_out)
        toolbar.addAction(self.zoom_out_action)

        # Rotate
        self.rotate_action = QAction("🔄", self)
        self.rotate_action.setToolTip("Rotate 90°")
        self.rotate_action.triggered.connect(self.rotate_image)
        toolbar.addAction(self.rotate_action)
        
        toolbar.addSeparator()

        # Delete
        self.delete_action = QAction("🗑️", self)
        self.delete_action.setToolTip("Delete Image")
        self.delete_action.triggered.connect(self.delete_image)
        toolbar.addAction(self.delete_action)

        toolbar.addSeparator()

        # Simple Print
        self.simple_print_action = QAction("🖨️", self)
        self.simple_print_action.setToolTip("直接列印")
        self.simple_print_action.triggered.connect(self.on_simple_print)
        toolbar.addAction(self.simple_print_action)

        # Poster Print
        self.split_print_action = QAction("🧩", self)
        self.split_print_action.setToolTip("分割列印 (Poster Print)")
        self.split_print_action.triggered.connect(self.on_split_print)
        toolbar.addAction(self.split_print_action)

        # Status label showing all-AI-local info
        self.status_label = QLabel("  🖥️ 本機 AI 處理 (無需網路)  ")
        self.status_label.setStyleSheet("color: #666; font-size: 11px;")
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        toolbar.addWidget(spacer)
        toolbar.addWidget(self.status_label)

    def change_view_mode(self, index):
        if index == 0: # 縮圖 (Thumbnail Grid)
            self.thumbnail_view.setViewMode(QListView.ViewMode.IconMode)
            self.thumbnail_view.setIconSize(QSize(150, 150))
            self.thumbnail_view.setGridSize(QSize(180, 210))
            self.thumbnail_view.setSpacing(15)
            self.thumbnail_view.setWordWrap(True)
            alignment = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom
        else: # 清單 (List)
            self.thumbnail_view.setViewMode(QListView.ViewMode.ListMode)
            self.thumbnail_view.setIconSize(QSize(64, 64))
            self.thumbnail_view.setGridSize(QSize()) # unset grid
            self.thumbnail_view.setSpacing(4)
            self.thumbnail_view.setWordWrap(False)
            alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            
        for i in range(self.thumbnail_view.count()):
            item = self.thumbnail_view.item(i)
            item.setTextAlignment(alignment)

    def update_toolbar_state(self):
        is_single_view = self.stacked_widget.currentIndex() == 1
        has_selection_in_grid = len(self.thumbnail_view.selectedItems()) > 0

        self.view_mode_combo.setEnabled(not is_single_view)
        self.back_action.setEnabled(is_single_view)
        
        has_prev = is_single_view and self.current_image_index > 0
        has_next = is_single_view and self.current_image_index >= 0 and self.current_image_index < self.thumbnail_view.count() - 1
        
        self.prev_action.setEnabled(has_prev)
        self.next_action.setEnabled(has_next)
        
        self.zoom_in_action.setEnabled(is_single_view)
        self.zoom_out_action.setEnabled(is_single_view)
        self.rotate_action.setEnabled(is_single_view)
        
        # Delete is enabled if in single view, or if an item is selected in grid view
        self.delete_action.setEnabled(is_single_view or (not is_single_view and has_selection_in_grid))

    def on_dir_selected(self, selected, deselected):
        indexes = selected.indexes()
        if indexes:
            index = indexes[0]
            dir_path = self.file_model.filePath(index)
            self.load_directory_thumbnails(dir_path)
            self.show_thumbnails_mode()

    def load_directory_thumbnails(self, dir_path):
        self.thumbnail_view.clear()
        
        valid_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp', '.psd', '.tif', '.tiff'}
        
        try:
            for entry in os.scandir(dir_path):
                if entry.is_file():
                    ext = os.path.splitext(entry.name)[1].lower()
                    if ext in valid_extensions:
                        self.add_thumbnail(entry.path, entry.name)
        except PermissionError:
            pass
            
        self.update_toolbar_state()

    def load_image_as_pixmap(self, path):
        try:
            with Image.open(path) as img:
                img = ImageOps.exif_transpose(img)
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                data = img.tobytes("raw", "RGBA")
                qim = QImage(data, img.width, img.height, QImage.Format.Format_RGBA8888)
                return QPixmap.fromImage(qim.copy())
        except Exception as e:
            print(f"Error loading {path} with Pillow: {e}")
            return QPixmap()

    def add_thumbnail(self, path, name):
        pixmap = self.load_image_as_pixmap(path)
        
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            
            icon = QIcon(scaled_pixmap)
            item = QListWidgetItem(icon, name)
            item.setData(Qt.ItemDataRole.UserRole, path)
            
            if self.view_mode_combo.currentIndex() == 0:
                item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
            else:
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                
            self.thumbnail_view.addItem(item)

    def on_thumbnail_double_clicked(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)
        if path:
            self.current_image_index = self.thumbnail_view.row(item)
            self.load_single_image(path)

    def show_thumbnails_mode(self):
        self.stacked_widget.setCurrentIndex(0)
        self.current_image_path = None
        self.current_image_index = -1
        self.update_toolbar_state()
        
    def load_single_image(self, path):
        self.current_image_path = path
        pixmap = self.load_image_as_pixmap(path)
        
        self.scene.clear()
        self.pixmap_item = self.scene.addPixmap(pixmap)
        self.scene.setSceneRect(self.pixmap_item.boundingRect())
        
        # Reset transformations
        self.current_scale = 1.0
        self.single_view.resetTransform()
        
        # fit to view initially
        self.single_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        
        self.stacked_widget.setCurrentIndex(1)
        self.update_toolbar_state()

    def prev_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            item = self.thumbnail_view.item(self.current_image_index)
            path = item.data(Qt.ItemDataRole.UserRole)
            self.load_single_image(path)

    def next_image(self):
        if self.current_image_index >= 0 and self.current_image_index < self.thumbnail_view.count() - 1:
            self.current_image_index += 1
            item = self.thumbnail_view.item(self.current_image_index)
            path = item.data(Qt.ItemDataRole.UserRole)
            self.load_single_image(path)

    def zoom_in(self):
        if self.current_image_path:
            self.single_view.scale(1.2, 1.2)

    def zoom_out(self):
        if self.current_image_path:
            self.single_view.scale(1 / 1.2, 1 / 1.2)

    def rotate_image(self):
        if self.current_image_path:
            self.single_view.rotate(90)

    def delete_image(self):
        is_single_view = self.stacked_widget.currentIndex() == 1
        
        if is_single_view and self.current_image_path:
            path_to_delete = self.current_image_path
        elif not is_single_view:
            selected_items = self.thumbnail_view.selectedItems()
            if not selected_items:
                return
            path_to_delete = selected_items[0].data(Qt.ItemDataRole.UserRole)
        else:
            return

        reply = QMessageBox.question(self, 'Delete File', 
                                     f"Are you sure you want to delete\n{path_to_delete}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(path_to_delete)
                
                if is_single_view:
                    self.show_thumbnails_mode()
                
                # Refresh thumbnails
                indexes = self.tree_view.selectedIndexes()
                if indexes:
                    dir_path = self.file_model.filePath(indexes[0])
                    self.load_directory_thumbnails(dir_path)
            except Exception as e:
                QMessageBox.warning(self, 'Error', f"Could not delete file:\n{e}")

    def _get_current_path(self):
        if self.stacked_widget.currentIndex() == 1 and self.current_image_path:
            return self.current_image_path
        items = self.thumbnail_view.selectedItems()
        if items:
            return items[0].data(Qt.ItemDataRole.UserRole)
        return None

    def on_split_print(self):
        path = self._get_current_path()
        if path:
            dialog = SplitPrintDialog(path, self)
            dialog.exec()

    def on_simple_print(self):
        self.on_simple_print_from_path(self._get_current_path())

    def on_simple_print_from_path(self, path):
        if not path:
            return
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        dialog.setWindowTitle("列印圖片")
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        from PIL import Image, ImageOps
        pil_img = Image.open(path)
        pil_img = ImageOps.exif_transpose(pil_img)
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")
        qimg = pil_to_qimage(pil_img)
        pixmap = QPixmap.fromImage(qimg)
        painter = QPainter()
        painter.begin(printer)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        page_w = printer.width()
        page_h = printer.height()
        scaled = pixmap.scaled(
            page_w, page_h,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        x = (page_w - scaled.width()) // 2
        y = (page_h - scaled.height()) // 2
        painter.drawPixmap(max(0, x), max(0, y), scaled)
        painter.end()

    def show_thumbnail_context_menu(self, pos):
        item = self.thumbnail_view.itemAt(pos)
        if item:
            item.setSelected(True)
            self.update_toolbar_state()
            
            path = item.data(Qt.ItemDataRole.UserRole)
            self.show_context_menu_for_path(path, self.thumbnail_view.mapToGlobal(pos))

    def show_single_image_context_menu(self, pos):
        if self.current_image_path:
            self.show_context_menu_for_path(self.current_image_path, self.single_view.mapToGlobal(pos))

    def show_context_menu_for_path(self, path, global_pos):
        menu = QMenu(self)

        # Local AI Transformations (fully offline, no API key needed)
        ai_menu = menu.addMenu("🧠 AI 圖片轉換 (本機)")

        upscale_action = ai_menu.addAction("提升解析度 (Upscale)")
        upscale_action.setData(("ai", "upscale"))
        colorize_action = ai_menu.addAction("黑白轉彩色 (Colorize)")
        colorize_action.setData(("ai", "colorize"))

        style_menu = ai_menu.addMenu("🎭 藝術風格轉換 (Neural Style)")

        ai_styles = [
            ("星夜 (Starry Night)", "style_starry_night"),
            ("吶喊 (The Scream)", "style_the_scream"),
            ("神奈川沖浪裏 (The Wave)", "style_the_wave"),
            ("糖果風格 (Candy)", "style_candy"),
            ("繆斯 (La Muse)", "style_la_muse"),
            ("馬賽克 (Mosaic)", "style_mosaic"),
            ("羽毛 (Feathers)", "style_feathers"),
            ("烏德尼 (Udnie)", "style_udnie"),
            ("構圖七號 (Composition VII)", "style_composition_vii"),
        ]

        for label, key in ai_styles:
            action = style_menu.addAction(label)
            action.setData(("ai", key))

        menu.addSeparator()

        # Local Basic Processing (Pillow-based)
        local_menu = menu.addMenu("🎨 本機圖片處理")

        adjust_menu = local_menu.addMenu("調整")
        for label, key in [("亮度/對比度...", "brightness_contrast"), ("色彩平衡...", "color_balance")]:
            action = adjust_menu.addAction(label)
            action.setData(("local_dialog", key))

        filter_menu = local_menu.addMenu("濾鏡效果")
        for label, key in [
            ("銳利化", "sharpen"),
            ("模糊效果", "blur"),
            ("浮雕效果", "emboss"),
            ("邊緣偵測", "edge_detect"),
        ]:
            action = filter_menu.addAction(label)
            action.setData(("local", key))

        color_menu = local_menu.addMenu("色彩效果")
        for label, key in [
            ("轉黑白", "grayscale"),
            ("暖色濾鏡", "warm"),
            ("冷色濾鏡", "cool"),
            ("復古濾鏡 (Sepia)", "sepia"),
        ]:
            action = color_menu.addAction(label)
            action.setData(("local", key))

        menu.addSeparator()
        simple_print_action = menu.addAction("🖨️ 直接列印 (Simple Print)")
        simple_print_action.setData(("simple_print",))
        split_print_action = menu.addAction("🧩 分割列印 (Poster Print)")
        split_print_action.setData(("split_print",))

        menu.addSeparator()
        properties_action = menu.addAction("屬性 (Properties)")

        action = menu.exec(global_pos)

        if action is None:
            return

        if action == properties_action:
            self.show_properties(path)
            return

        if action == split_print_action:
            dialog = SplitPrintDialog(path, self)
            dialog.exec()
            return
        if action == simple_print_action:
            self.on_simple_print_from_path(path)
            return

        data = action.data()
        if isinstance(data, tuple):
            action_type, value = data
            if action_type == "ai":
                self.run_ai_transform(path, value)
            elif action_type == "local":
                self.run_local_transform(path, value)
            elif action_type == "local_dialog":
                self.run_local_transform_with_dialog(path, value)

    def run_ai_transform(self, path, transform_type):
        self.progress_dialog = QProgressDialog("AI 處理中（使用本機 OpenCV DNN）...", None, 0, 0, self)
        self.progress_dialog.setWindowTitle("Local AI Image Processing")
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.show()

        self.ai_worker = AIImageWorker(path, transform_type)
        self.ai_worker.finished.connect(self.on_ai_transform_success)
        self.ai_worker.error.connect(self.on_ai_transform_error)
        self.ai_worker.start()

    def on_ai_transform_success(self, new_path):
        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.close()
        QMessageBox.information(self, "成功", f"轉換完成！已另存新檔於：\n{new_path}")
        indexes = self.tree_view.selectedIndexes()
        if indexes:
            dir_path = self.file_model.filePath(indexes[0])
            self.load_directory_thumbnails(dir_path)

    def on_ai_transform_error(self, error_msg):
        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.close()
        QMessageBox.critical(self, "轉換失敗", f"發生錯誤：\n{error_msg}")

    def run_local_transform(self, path, transform_type, params=None):
        self.progress_dialog = QProgressDialog("本機處理中...", None, 0, 0, self)
        self.progress_dialog.setWindowTitle("Image Processing")
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.show()

        self.local_worker = LocalImageWorker(path, transform_type, params)
        self.local_worker.finished.connect(self.on_local_transform_success)
        self.local_worker.error.connect(self.on_local_transform_error)
        self.local_worker.start()

    def run_local_transform_with_dialog(self, path, transform_type):
        dialog = None
        if transform_type == "brightness_contrast":
            dialog = AdjustmentDialog("亮度/對比度調整", {
                "brightness": {"label": "亮度", "min": 0.0, "max": 2.0, "default": 1.0},
                "contrast": {"label": "對比度", "min": 0.0, "max": 2.0, "default": 1.0},
            }, self)
        elif transform_type == "color_balance":
            dialog = AdjustmentDialog("色彩平衡調整", {
                "red": {"label": "紅色 (R)", "min": 0.0, "max": 2.0, "default": 1.0},
                "green": {"label": "綠色 (G)", "min": 0.0, "max": 2.0, "default": 1.0},
                "blue": {"label": "藍色 (B)", "min": 0.0, "max": 2.0, "default": 1.0},
            }, self)

        if dialog and dialog.exec() == QDialog.DialogCode.Accepted:
            self.run_local_transform(path, transform_type, dialog.get_values())

    def on_local_transform_success(self, new_path):
        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.close()
        QMessageBox.information(self, "成功", f"處理完成！已另存新檔於：\n{new_path}")
        indexes = self.tree_view.selectedIndexes()
        if indexes:
            dir_path = self.file_model.filePath(indexes[0])
            self.load_directory_thumbnails(dir_path)

    def on_local_transform_error(self, error_msg):
        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.close()
        QMessageBox.critical(self, "處理失敗", f"發生錯誤：\n{error_msg}")

    def show_properties(self, path):
        if path:
            file_info = QFileInfo(path)
            size_kb = file_info.size() / 1024
            
            width = 0
            height = 0
            try:
                with Image.open(path) as img:
                    width = img.width
                    height = img.height
            except Exception:
                pass

            details = f"""
            <b>Name:</b> {file_info.fileName()}<br>
            <b>Path:</b> {file_info.absoluteFilePath()}<br>
            <b>Size:</b> {size_kb:.2f} KB<br>
            <b>Dimensions:</b> {width} x {height} pixels<br>
            <b>Created:</b> {file_info.birthTime().toString()}<br>
            <b>Modified:</b> {file_info.lastModified().toString()}<br>
            """

            dialog = QDialog(self)
            dialog.setWindowTitle("Image Properties")
            layout = QVBoxLayout()
            label = QLabel(details)
            label.setTextFormat(Qt.TextFormat.RichText)
            layout.addWidget(label)
            dialog.setLayout(layout)
            dialog.exec()
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec())
