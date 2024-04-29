from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import *
import os, sys 
import sqlite3
import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow
from telaLogin import Ui_Dialog1
from telaMainFrame import  Ui_MainWindow
import imgimport
from redefinirSenha import Ui_Dialog


class JanelaLogin(QMainWindow):
    def __init__(self):
        super(JanelaLogin, self).__init__()
        self.ui = Ui_Dialog1()
        self.ui.setupUi(self)

        self.setWindowTitle("Sistema de Supermercado")

        # Conectando os botões aos métodos correspondentes
        self.ui.pushButton.clicked.connect(self.butao_entrar)
        self.ui.pushButton_2.clicked.connect(self.butao_sair_app)
        self.ui.label_4.mousePressEvent = self.abrir_recuperacao_senha

      
    def butao_entrar(self):
        # Obter o login e a senha inseridos
        login = self.ui.lineEdit.text()
        senha = self.ui.lineEdit_2.text()

        # Conectar ao banco de dados PostgreSQL
        try:
            connection = psycopg2.connect(
                user="postgres",
                password="bungas10",
                host="localhost",
                port="5432",
                database="supermercado_db"
            )

            cursor = connection.cursor()

            # Consultar o banco de dados para verificar as credenciais
            query = "SELECT * FROM usuarios WHERE login = %s AND senha = %s"
            cursor.execute(query, (login, senha))
            user = cursor.fetchone()

            if user:
                QMessageBox.information(self, "Login", "Login bem-sucedido!")
                self.abrir_menu()

            else:
                QMessageBox.warning(self, "Incorreto", "Credenciais inválidas.")

        except psycopg2.Error as error:
            QMessageBox.critical(self, "Erro", f"Erro ao conectar ao PostgreSQL: {error}")
        finally:
            cursor.close()
            connection.close()

    def abrir_menu(self):
        self.menu_window = JanelaMenu()
        self.menu_window.show()
        self.close()

    def abrir_recuperacao_senha(self, event):
        self.recuperacao_senha_window = JanelaRedefinirSenha()
        self.recuperacao_senha_window.show() 
    
    

    def butao_sair_app(self):
        QApplication.quit()

class JanelaMenu(QMainWindow):
    def __init__(self):
        super(JanelaMenu, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Sistema de caixa")

class JanelaRedefinirSenha(QMainWindow):
    def __init__(self):
        super(JanelaRedefinirSenha, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Redefinição de Senha")

        # Ocultar o campo de senha inicialmente
        self.ui.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        # Conectar botão para alternar entre mostrar/ocultar senha
        self.ui.pushButton.clicked.connect(self.mostrar_ocultar_senha)

    def mostrar_ocultar_senha(self):
        if self.ui.lineEdit.echoMode() == QtWidgets.QLineEdit.Password:
            self.ui.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)  # Mostrar senha
        else:
            self.ui.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)  # Ocultar senha 

            
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    janela = JanelaLogin()
    janela.show()
    sys.exit(app.exec_())





