from Converter import Converter
from time import localtime, strftime
from Components.Element import cached

class ClockToText(Converter, object):
	DEFAULT = 0
	WITH_SECONDS = 1
	IN_MINUTES = 2
	DATE = 3
	FORMAT = 4
	AS_LENGTH = 5
	TIMESTAMP = 6
	FULL = 7
	SHORT_DATE = 8
	LONG_DATE = 9
	VFD = 10
	
	# add: date, date as string, weekday, ...
	# (whatever you need!)
	
	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "WithSeconds":
			self.type = self.WITH_SECONDS
		elif type == "InMinutes":
			self.type = self.IN_MINUTES
		elif type == "Date":
			self.type = self.DATE
		elif type == "AsLength":
			self.type = self.AS_LENGTH
		elif type == "Timestamp":	
			self.type = self.TIMESTAMP
		elif type == "Full":
			self.type = self.FULL
		elif type == "ShortDate":
			self.type = self.SHORT_DATE
		elif type == "LongDate":
			self.type = self.LONG_DATE
		elif type == "VFD":
			self.type = self.VFD
		elif "Format" in type:
			self.type = self.FORMAT
			self.fmt_string = type[7:]
		else:
			self.type = self.DEFAULT

	@cached
	def getText(self):
		time = self.source.time
		if time is None:
			return ""

		# handle durations
		if self.type == self.IN_MINUTES:
			return "%d min" % (time / 60)
		elif self.type == self.AS_LENGTH:
			if time < 0:
				return ""
			return "%d:%02d" % (time / 60, time % 60)
		elif self.type == self.TIMESTAMP:
			return str(time)
		
		t = localtime(time)
		
		if self.type == self.WITH_SECONDS:
			return "%2d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec)
		elif self.type == self.DEFAULT:
			return "%2d:%02d" % (t.tm_hour, t.tm_min)
		elif self.type == self.DATE:
			return strftime("%A %e %b %Y", t)
		elif self.type == self.FULL:
			return strftime("%a %e/%m  %-H:%M", t)
		elif self.type == self.SHORT_DATE:
			return strftime("%a %e/%m", t)
		elif self.type == self.LONG_DATE:
			return strftime("%a %e %b", t)
		elif self.type == self.VFD:
			return strftime("%k:%M %e/%m", t)
		elif self.type == self.FORMAT:
			return strftime(self.fmt_string, t)
		else:
			return "???"

	text = property(getText)
