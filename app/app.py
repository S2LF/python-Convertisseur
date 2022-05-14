from PySide2 import QtWidgets
import currency_converter

class App(QtWidgets.QWidget):
    def __init__(self):
        """Application to convert currency"""
        super().__init__()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("Convertisseur de devises")
        self.setup_ui()
        self.setup_light_css()
        self.set_default_values()
        self.setup_connections()

    def setup_ui(self):
        """Setup the user interface"""
        self.layout = QtWidgets.QHBoxLayout(self)
        self.cbb_devisesFrom = QtWidgets.QComboBox()
        self.spn_montant = QtWidgets.QSpinBox()
        self.cbb_devisesTo = QtWidgets.QComboBox()
        self.spn_montantConverti = QtWidgets.QSpinBox()
        self.btn_inverse = QtWidgets.QPushButton("Inverser devises")
        self.radio_color = QtWidgets.QButtonGroup()
        self.radio_color_light = QtWidgets.QRadioButton("Thème clair")
        self.radio_color_dark = QtWidgets.QRadioButton("Thème sombre")

        self.layout.addWidget(self.cbb_devisesFrom)
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_inverse)
        self.layout.addWidget(self.radio_color_light)
        self.layout.addWidget(self.radio_color_dark)
        self.radio_color_light.setChecked(True)

    def set_default_values(self):
        """Set default values"""
        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.cbb_devisesTo.setCurrentText("EUR")
        self.spn_montant.setRange(1, 1000000)
        self.spn_montantConverti.setRange(1, 1000000)
        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)
        
        self.radio_color.addButton(self.radio_color_dark)
        self.radio_color.addButton(self.radio_color_light)

    def setup_connections(self):
        """Setup the connections"""
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.cbb_devisesTo.activated.connect(self.compute)
        self.spn_montant.valueChanged.connect(self.compute)
        self.btn_inverse.clicked.connect(self.inverser_devise)
        self.radio_color.buttonClicked.connect(self.change_theme)

    def setup_light_css(self):
        """Setup the light theme"""
        self.setStyleSheet("""
           QWidget {
                background-color: white;
                color: black;
                border:none;
            }
           
            QComboBox {
                width: 100px;
            }

            QSpinBox {
                width: 100%;
            }

            QPushButton {
                width: 100%;
            }

            QLabel {
                width: 100%;
            }
        """)

    def setup_dark_css(self):
        """Setup the dark theme"""
        self.setStyleSheet("""
            QWidget {
                background-color: #202124;
                color: white;
                border:none;
            }
           
            QComboBox {
                width: 100px;
            }

            QSpinBox {
                width: 100%;
            }

            QPushButton {
                width: 100%;
            }

            QLabel {
                width: 100%;
            }
        """)

    def change_theme(self):
        """Change the theme"""
        if self.radio_color_light.isChecked():
            self.setup_light_css()
        else:
            self.setup_dark_css()

    def compute(self):
        """Compute the conversion"""
        montant = self.spn_montant.value()
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        try : 
            montant_converti = self.c.convert(montant, devise_from, devise_to)
        except currency_converter.currency_converter.RateNotFoundError:
            print("Erreur : taux de change non trouvé")
        else:
            self.spn_montantConverti.setValue(montant_converti)

    def inverser_devise(self):
        """Inverse the currencies"""
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()
        self.cbb_devisesFrom.setCurrentText(devise_to)
        self.cbb_devisesTo.setCurrentText(devise_from)
        self.compute()

app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()