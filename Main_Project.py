import calendar
import kivy
from datetime import datetime
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder 
from kivy.uix.dropdown import DropDown 
from kivy.base import runTouchApp
from kivy.uix.popup import Popup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

day = datetime.now().day
mm = datetime.now().month
yy = datetime.now().year



scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json',scope)
client = gspread.authorize(creds)
sheet = client.open('PythonWorkoutLog').sheet1



shoulders = ['OHP', 'Shrugs', 'Z Press']
triceps = ['CGBP']
biceps = ['Curl']
chest = ['Bench Press']
back = ['Row']
legs = ['Squat']
ab = ['Ab Wheel']
cardio = ['Prowler']
exerciseGroups = {'Shoulders':shoulders,'Triceps':triceps,'Biceps':biceps,'Chest':chest,'Back':back,'Legs':legs,'Abs':ab,'Cardio':cardio}
exerciseGroupsList = ['Shoulders','Triceps','Biceps','Chest','Back','Legs','Abs','Cardio']

class MainPage(GridLayout):
	def __init__(self, **kwargs):
		super(MainPage, self).__init__(**kwargs)

		self.cols = 1
		

		self.todaysDate = Label(text =str(mm) +'/'+ str(day) +'/' + str(yy))
		self.add_widget(self.todaysDate)
		self.exerciseButton = Button(text = 'Exercise')
		self.exerciseCategoryButton = Button(text = 'Category')
		self.add_widget(self.exerciseButton)
		self.add_widget(self.exerciseCategoryButton)
		self.exerciseButton.bind(on_press=self.pressed)

		self.exerciseCategoryButton.bind(on_press=self.pressedCategory)

		self.inside = GridLayout()
		self.inside.cols = 2

		self.inside.add_widget(Label(text = 'Sets'))
		self.sets = TextInput(multiline = False)
		self.inside.add_widget(self.sets)


		self.inside.add_widget(Label(text = 'Reps'))
		self.reps = TextInput(multiline= False)
		self.inside.add_widget(self.reps)

		self.inside.add_widget(Label(text = 'Weight'))
		self.weight = TextInput(multiline = False)
		self.inside.add_widget(self.weight)

		self.add_widget(self.inside)

		self.submit = Button(text = 'Submit')
		self.add_widget(self.submit)
		self.submit.bind(on_press = self.submited)

	def pressed(self, instance):
		dropdown = DropDown(dismiss_on_select = True)
		for i in range(len(exerciseGroupsList)):
			btn =  Button(text = exerciseGroupsList[i],size_hint_y = None, height = 44)
			btn.bind(on_release = lambda btn: dropdown.select(btn.text))
			dropdown.add_widget(btn)
		self.exerciseButton.bind(on_release = dropdown.open)
		dropdown.bind(on_select = lambda instance, x:setattr(self.exerciseButton, 'text', x))

	def pressedCategory(self, instance):
		dropdownOne = DropDown(dismiss_on_select = True)
		for b in range(len(exerciseGroupsList)):
			if self.exerciseButton.text == exerciseGroupsList[b]:
				newList = exerciseGroupsList[b]
				secondList = exerciseGroups.get(exerciseGroupsList[b])
				for i in range(len(secondList)):
					btnOne =  Button(text =secondList[i],size_hint_y = None, height = 44)
					btnOne.bind(on_release = lambda btn: dropdownOne.select(btn.text))
					dropdownOne.add_widget(btnOne)
				self.exerciseCategoryButton.bind(on_release = dropdownOne.open)
				dropdownOne.bind(on_select = lambda instance, x:setattr(self.exerciseCategoryButton, 'text', x))
			continue



	def submited(self, instance):
		savedValues = [self.exerciseButton.text,self.exerciseCategoryButton.text,self.sets.text,self.reps.text,self.weight.text,day,mm,yy]
		max_row = len(sheet.get_all_values())
		if len(savedValues) == 8:
			for i in range(0,8):
				sheet.update_cell(max_row+1,i+1,savedValues[i])
		else:
			popup = Popup(title = 'Popup',
							content = Label(text='You need to fill out all values'), size = (100,300), size_hint_y = None)
			popup.open()
		

class MyApp(App):
	def build(self):
		return MainPage()

if __name__ == '__main__':
	MyApp().run()