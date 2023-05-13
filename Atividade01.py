from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import sqlite3
import os

path_data_base = os.path.expanduser('~') + '\\AppData\\Local\\QSMPList'

def verif_num(element):
    try:
        num = int(element)
        return True
    except:
        return False
    
def create_db():
    if not os.path.exists(path_data_base):
        lista = [["Agatha",'F',25], ["Alexandre",'M',32], ["Camila",'F',30], ["Esther",'F',18], 
                ["Nathan",'M',24], ["Isis",'F',42], ["Amanda",'F',32], ["Antônio",'M',21],
                ["Maria",'F',22], ["Pietro",'M',30], ["Henry",'M',45], ["Laís",'F',26], ["Ian",'M',31],
                ["Carolina",'F',29], ["Vicente",'M',30]]
        os.mkdir(path_data_base)
        conn = sqlite3.connect(path_data_base + "\\ListaDeCadastros.db")
        conn.execute("CREATE TABLE IF NOT EXISTS Cadastros"
                        "(name TEXT,"
                        "sexo TEXT,"
                        "age INTEGER);")
        for i in lista:
            conn.execute(f"INSERT INTO Cadastros VALUES('{i[0]}','{i[1]}',{i[2]})")
        conn.commit()
        conn.close()

def Pesquisar_db(pesquisar_sexo, min_age, max_age):
    conn = sqlite3.connect(path_data_base + "\\ListaDeCadastros.db")
    lista = conn.execute("SELECT * FROM Cadastros").fetchall()
    return_list = []
    for i in lista:
        if pesquisar_sexo is not "Q":
            if i[1] == pesquisar_sexo and (i[2] < max_age and i[2] > min_age):
                return_list.append(i)
        elif (i[2] < max_age and i[2] > min_age):
            return_list.append(i)
    conn.close()
    return return_list
    

def Cadastrar_db(nome, sexo, idade):
    conn = sqlite3.connect(path_data_base + "\\ListaDeCadastros.db")
    conn.execute(f"INSERT INTO Cadastros VALUES ('{nome}','{sexo}',{idade})")
    conn.commit()
    conn.close()

class Main(Screen):
    pass


class Cadastro(Screen):
    def verif_sexo(self):
        if self.ids.tgb_F.state == "normal":
            return "M"
        elif self.ids.tgb_M.state == "normal":
            return "F"

    def verif_age(self):
        if verif_num(self.ids.input_age.text):
            return int(self.ids.input_age.text)
        else:
            self.ids.input_age.text = ""
            self.ids.input_age.background_color = 1,0,0,1
            return None

    def verif_name(self):
        prior = self.ids.input_name.text
        if prior != "":
            return prior
        else:
            self.ids.input_name.text = ""
            self.ids.input_name.background_color = 1,0,0,1
            return None
    
    def click(self):
        name = self.verif_name()
        sexo = self.verif_sexo()
        age = self.verif_age()
        if name != None and sexo != None and age != None:
            pupup = Popup(title='Cadastro feito',
                          content=Label(text='Informações cadastradas\ncom sucesso! :)',
                                        font_size=20),
                          size_hint=(None, None), size=(400, 400))
            pupup.open()
            self.ids.input_age.text = ""
            self.ids.input_name.text = ""
            self.cadastrar(name, sexo, age)

    def cadastrar(self, name, sexo, age):
        Cadastrar_db(name, sexo, age)
        self.ids.input_age.background_color = 75/255, 219/255, 219/255,1
        self.ids.input_name.background_color = 75/255, 219/255, 219/255,1


class Pesquisar(Screen):
    def verif_sexo_pesquisa(self):
        if self.ids.tgb_pesquisa_M.state == 'down':
            return 'M'
        elif self.ids.tgb_pesquisa_F.state == 'down':
            return 'F'
        else:
            return 'Q'

    

    def pesquisar(self):
        separar_sexo = self.verif_sexo_pesquisa()
        minn = 0
        maxx = 130
        if verif_num(self.ids.input_min_age.text):
            minn = int(self.ids.input_min_age.text)
        if verif_num(self.ids.input_max_age.text):
            maxx = int(self.ids.input_max_age.text)
        listar_retornar = Pesquisar_db(separar_sexo, minn, maxx)
        self.mostrar(listar_retornar)

    def mostrar(self, lista):
        self.ids.mostrar_lista.clear_widgets()
        box = BoxLayout(orientation='vertical',size_hint=(1,None))
        for i in lista:
            box.add_widget(Label(text=f"{i[0]} - {i[1]} - {i[2]}", size_hint=(1, None), size=(100,50)))
        box.height = 50*len(lista)
        self.ids.mostrar_lista.add_widget(box)
    
    def click(self):
        self.pesquisar()
            


class Tela(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        self.title = "Tela de Cadastro QSMP"
        return kv_file

kv_file = Builder.load_file("tela.kv")

if __name__ == '__main__':
    create_db()
    MyApp().run()
