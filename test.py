'''
Coded by: Abhishek Sen Amit Dubey Himanshu Agarwal
Language: Python 2.7
Library: Kivy 1.9.1
'''
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.switch import Switch
from kivy.uix.gridlayout import GridLayout
from functools import partial
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.lang import Builder
import time

dataset = raw_input("Enter dataframe to be sent : ")
dataset_length = len(dataset)
timer_max_value = int(raw_input("Enter timer duration : "))

class TimerProt(BoxLayout):
	time = NumericProperty(0)
	datas = list(dataset)
	datar = [' ' for i in range(dataset_length)]
	datasize = dataset_length
	dataindex = dataset_length
	timerval = timer_max_value
	ackflag = True

	def tick(self, *_):
		if self.time > 0:
			self.time -= 1
		elif self.time == 0:
			slog = self.ids['sloglabel']
			slog.text = 'Sender timer timed out\nYou need to reset the timer'
			rst = self.ids['timerreset']
			rst.disabled = False
			recb = self.ids['recbutton']
			recb.disabled = True
		else:
			pass

	def start(self, *_):
		switch = self.ids['switchlabel']
		slog = self.ids['sloglabel']
		rlog = self.ids['rloglabel']
		send_button = self.ids['sendbutton']
		rec_button = self.ids['recbutton']
		slog.text = 'Trying to send frame...'
		if self.dataindex>=1 and switch.active:
			send_button.disabled = True
			rec_button.disabled = False
			self.cb = Clock.schedule_interval(self.tick,1)
			self.datar[self.datasize - self.dataindex] = self.datas[self.datasize - self.dataindex]
			label = self.ids['rframelabel']
			label.text = self.prtr()
			rlog.text = rlog.text + '\nFrame received'
			self.ackflag = True

	def pause(self):
		Clock.unschedule(self.cb)

	def reset(self, *_):
		switch = self.ids['switchlabel']
		slog = self.ids['sloglabel']
		rlog = self.ids['rloglabel']
		rlog.text = 'Trying to send ACK...'
		if self.dataindex>=1 and switch.active and self.ackflag:
			self.time = self.timerval
			Clock.unschedule(self.cb)
			self.dataindex -= 1
			slog.text = slog.text + '\nACK received'
			send_button = self.ids['sendbutton']
			send_button.disabled = False
			self.ackflag = False
		if self.dataindex == 0:
			clog = self.ids['cloglabel']
			clog.text = clog.text + '\nDemo over'
			'''
			time.sleep(3)
			exit()
			'''

	def sreset(self, *_):
		switch = self.ids['switchlabel']
		slog = self.ids['sloglabel']
		rlog = self.ids['rloglabel']
		rlog.text = 'Trying to send ACK...'
		self.time = self.timerval
		Clock.unschedule(self.cb)
		slog.text = 'Timer reset\nTrying to send frame again...'
		if self.dataindex>=1 and switch.active:
			self.cb = Clock.schedule_interval(self.tick,1)
			self.datar[self.datasize - self.dataindex] = self.datas[self.datasize - self.dataindex]
			label = self.ids['rframelabel']
			label.text = self.prtr()
			rlog.text = rlog.text + '\nFrame received'
			recb = self.ids['recbutton']
			recb.disabled = False
			self.ackflag = True

	def prts(self,*args):
		return '\n'.join(self.datas)
	
	def prtr(self,*args):
		return '\n'.join(self.datar)

	def update(self,*args):
		log = self.ids['cloglabel']
		switch = self.ids['switchlabel']
		if switch.active == True:
			log.text = 'The connection is OFF'
		else:
			log.text = 'The connection is ON'


class TestApp(App):
    def build(self):
        return TimerProt(time=timer_max_value)

if __name__ == '__main__':
	#Window.fullscreen = 'auto'
	TestApp().run()



