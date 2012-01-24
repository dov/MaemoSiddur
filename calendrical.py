"""
CALENDRICAL CALCULATIONS

This module provides a set of function for date conversion between
different calendars.

Currently the module supports
- Gregorian calendar (the common calendar in the Western world),
- ISO calendar (Gregorian week calendar used in some European 
	countries) and
- Hebrew calendar.

This code is an adaptation of the algorithms provided in the book
\"Calendrical Calculations\" by Reingold and Dershowitz. The functions 
in the module have similar names to the names used in the book.

All calculations are done to or from a fixed day number series. Day 
number 1 is Monday, January 1, 1 (Gregorian calendar).

Examples:
Find the Hebrew date for February 25, 2007:
>>> hebrewFromFixed(fixedFromGregorian(2007, FEBRUARY, 25))
[5767, 12, 7]

Find day and month for Tuesday week 12, 2008:
>>> gregorianFromFixed(fixedFromIso(2008, 12, TUESDAY))
[2008, 3, 18]

References:
E.M. Reingold and N. Dershowitz, Calendrical Calculations: 
	The Millennium Edition, Cambridge, UK, 2001
E.M. Reingold and N. Dershowitz, Errata and Notes for Calendrical 
	Calculations: The Millennium Edition, December 7, 2006, available: 
	http://emr.cs.lit.edu/home/reingold/calendar-book/second-edition/errata.pdf

"""
__author__	= "Jacob Tardell <python@tardell.se>"

import math
import operator

def _amod(x, y):
	"""
	Adjusted remainder function
	
	Arguments:
	x - numerator
	y - denominator
	
	Return value:
	number
	"""
	return y + x % (-y)

# Cycles of Days
SUNDAY = 0
MONDAY = SUNDAY + 1
TUESDAY = SUNDAY + 2
WEDNESDAY = SUNDAY + 3
THURSDAY = SUNDAY + 4
FRIDAY = SUNDAY + 5
SATURDAY = SUNDAY + 6

def dayOfWeekFromFixed(date):
	"""
	Calculate weekday from fixed day number.
	
	Argument:
	date - fixed day number
	
	Return value:
	[0..6] - 0 == Sunday .. 6 == Saturday
	
	Example:
	>>> dayOfWeekFromFixed(fixedFromGregorian(2007, FEBRUARY, 25))
	0
	
	It is a Sunday.

	See:
	N.B. Weekday here different from weekday in isoFromFixed().
	"""
	return date % 7

def _kDayOnOrBefore(date, k):
	"""
	Weekday on or before fixed day number.
	
	Argument:
	date - fixed day number
	k - weekday
	
	Use the constants SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY,
	FRIDAY or SATURDAY for weekday.
	
	Return value:
	number - fixed day number
	"""
	return date - dayOfWeekFromFixed(date - k)

def _kDayOnOrAfter(date, k):
	"""
	Weekday on or after fixed day number.
	
	Argument:
	date - fixed day number
	k - weekday
	
	Use the constants SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY,
	FRIDAY or SATURDAY for weekday.
	
	Return value:
	number - fixed day number
	"""
	return _kDayOnOrBefore(date + 6, k)

def _kDayNearest(date, k):		
	"""
	Weekday nearest fixed day number.
	
	Argument:
	date - fixed day number
	k - weekday
	
	Use the constants SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY,
	FRIDAY or SATURDAY for weekday.
	
	Return value:
	number - fixed day number
	"""
	return _kDayOnOrBefore(date + 3, k)

def _kDayBefore(date, k):
	"""
	Weekday before fixed day number.
	
	Argument:
	date - fixed day number
	k - weekday
	
	Use the constants SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY,
	FRIDAY or SATURDAY for weekday.
	
	Return value:
	number - fixed day number
	"""
	return _kDayOnOrBefore(date - 1, k)

def _kDayAfter(date, k):		
	"""
	Weekday after fixed day number.
	
	Argument:
	date - fixed day number
	k - weekday
	
	Use the constants SUNDAY, MONDAY, TUESDAYTUESDAY, WEDNESDAY, THURSDAY,
	FRIDAY or SATURDAY for weekday.
	
	Return value:
	number - fixed day number
	"""
	return _kDayOnOrBefore(date + 7, k)
	
# Gregorian
GREGORIANEPOCH = 1

JANUARY = 1
FEBRUARY = JANUARY + 1
MARCH = JANUARY + 2
APRIL = JANUARY + 3
MAY = JANUARY + 4
JUNE = JANUARY + 5
JULY = JANUARY + 6
AUGUST = JANUARY + 7
SEPTEMBER = JANUARY + 8
OCTOBER = JANUARY + 9
NOVEMBER = JANUARY + 10
DECEMBER = JANUARY + 11

def _nthKDay(n, k, year, month, day):
	"""
	Fixed day number for n:th k-weekday before or after a Gregorian date.
	
	Arguments:
	n - days before or after
	k - weekday
	year - Gregorian year
	month - Gregorian month
	day - Gregorian day
	
	Use the constants SUNDAY, MONDAY, TUESDAY, WEDNESDAY,
	FRIDAY or SATURDAY for weekday.
	
	Use the constants JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE, JULY, 
	AUGUST, SEPTEMBER, OCTOBER, NOVEMBER or DECEMBER for Gregorian month.
	
	Return value:
	integer - fixed day number
	
	Fixed date of n:th k-day after Gregorian date.  If
	n > 0, return the n:th k-day on or after date.
	If n < 0, return the n:th k-day on or before date.
	"""
	if n > 0:
		return 7*n + _kDayBefore(fixedFromGregorian(year, month, day), k)
	else:
		return 7*n + _kDayAfter(fixedFromGregorian(year, month, day), k)

def _isGregorianLeapYear(year):
	"""
	Test if year is a leap year in the Gregorian calendar.
	
	Argument:
	year - Gregorian year

	Return value:
	[True, False]
	"""
	return (year % 4) == 0 and not ((year % 400) in [100, 200, 300])

def fixedFromGregorian(year, month, day):
	"""
	Convert Gregorian date to fixed day number.
	
	Argument:
	year - Gregorian year
	month - Gregorian month
	day - Gregorian day
	
	Use the constants JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE, JULY, 
	AUGUST, SEPTEMBER, OCTOBER, NOVEMBER or DECEMBER for Gregorian month.

	Return value:
	integer - fixed day number
	
	Example:
	>>> fixedFromGregorian(2007, JULY, 20)
	732877
	"""
	m = _amod((month - 2), 12)
	y = year + math.floor((month + 9)/12)
	return int(GREGORIANEPOCH - 1 - 306 + 365 *(y - 1) + math.floor((y - 1)/4) - math.floor((y - 1)/100) + math.floor((y - 1)/400) + math.floor((3*m - 1)/5) + 30*(m - 1) + day)

def gregorianYearFromFixed(date):
	"""
	Convert fixed day number to Gregorian year.

	Argument:
	date - fixed day number
	
	Return value:
	integer - Gregorian year
	
	Examples:
	>>> gregorianYearFromFixed(728714)
	1996
	
	A more elaborate example. On what weekday is Passover in the spring of 2009?
	Let's solve it steps:
	
	First find the Hebrew year of spring 2009.
	>>> 2009 - gregorianYearFromFixed(HEBREWEPOCH)
	5769
	
	Then use it to look up Passover, Nisan 15, that year.
	>>> fixedFromHebrew(2009 - gregorianYearFromFixed(HEBREWEPOCH), NISAN, 15)
	733506
	
	And find weekday of that fixed day number.
	>>> dayOfWeekFromFixed(fixedFromHebrew(2009 - gregorianYearFromFixed(HEBREWEPOCH), NISAN, 15))
	4

	Passover is on a Thursday (4). So Passover starts on a Wednesday evening.
	"""
	approx = math.floor((date - GREGORIANEPOCH + 2) * 400 / 146097)
	start = GREGORIANEPOCH + 365 * approx + math.floor(approx/4) - math.floor(approx/100) + math.floor(approx/400)
	if date < start:
		return int(approx)
	else:
		return int(approx + 1)

def gregorianFromFixed(date):
	"""
	Convert fixed day number to Gregorian date.
	
	Argument:
	date - fixed day number
	
	Return value:
	[integer, [1..12], [1..31]] - [year, month, day]
	
	Examples:
	>>> gregorianFromFixed(732877)
	[2007, 7, 20]
	"""
	y = gregorianYearFromFixed(GREGORIANEPOCH - 1 + date + 306)
	priorDays = date - fixedFromGregorian(y - 1, 3, 1)
	month = int(_amod(math.floor((5*priorDays + 155)/153) + 2, 12))
	year = int(y - math.floor((month + 9)/12))
	day = int(date - fixedFromGregorian(year, month, 1) + 1)
	return [year, month, day]

# ISO

SUNDAY7 = SUNDAY + 7

def fixedFromIso(year, week, day):
	"""
	Convert an ISO date to fixed day number.

	Argument:
	year - ISO year
	week - ISO week
	day - ISO weekday
	
	Use the constants MONDAY, TUESDAY, WEDNESDAY, THURSDAY,
	FRIDAY, SATURDAY, SUNDAY7 for ISO weekday.
	
	Return value:
	integer - fixed day number
	
	Example:
	>>> fixedFromIso(2007, 29, 5)
	732877
	
	N.B. ISO weekday is different from weekday in dayOfWeekFromFixed().
	"""
	return _nthKDay(week, SUNDAY, year - 1, DECEMBER, 28) + day

def isoFromFixed(date):
	"""
	Convert fixed day number to ISO date.
	
	Argument:
	date - fixed day number
	
	Return value:
	[integer, [1..53], [1..7]] - [year, week, ISO weekday]
	
	Examples:
	>>> isoFromFixed(732877)
	[2007, 29, 5]
	
	N.B. ISO weekday different from day in dayOfWeekFromFixed().
	"""
	approx = gregorianYearFromFixed(date - 3)
	if date >= fixedFromIso(approx + 1, 1, 1):
		year = approx + 1
	else:
		year = approx
	week = int(math.floor((date - fixedFromIso(year, 1, 1))/7) + 1)
	day = _amod(date, 7)
	return [year, week, day]

# Hebrew
HEBREWEPOCH = -1373427

NISAN = 1
IYYAR = NISAN + 1
SIVAN = NISAN + 2
TAMMUZ = NISAN + 3
AV = NISAN + 4
ELUL = NISAN + 5
TISHRI = NISAN + 6
MARHESHVAN = NISAN + 7
KISLEV = NISAN + 8
TEVET = NISAN + 9
SHEVAT = NISAN + 10
ADAR = NISAN + 11
ADARI = NISAN + 11
ADARII = NISAN + 12

def _isHebrewLeapYear(year):
	"""
	True if year is a Hebrew leap year
	
	Argument:
	year - Hebrew year
	
	Return value:
	[True, False]
	"""
	return ((7*year + 1) % 19) < 7

def _lastMonthOfHebrewYear(year):
	"""
	Number of months in a Hebrew year
	
	Argument:
	year - Hebrew year
	
	Return value:
	[12, 13]
	"""
	if _isHebrewLeapYear(year):
		return 13
	else:
		return 12

def _molad(month, year):
	"""
	The fixed moment of the mean conjunction
	
	Bug, see note 158 in Errata.
	
	Arguments:
	year - Hebrew year
	month - Hebrew month
	
	Return value:
	number (FIXME - should be integer?)
	"""
	if month < TISHRI:
		y = year + 1
	else:
		y = year
	monthsElapsed = month - tischri + int(math.floor((235*y - 234)/19.0))
	return HEBREWEPOCH - (876.0/25920) + monthsElapsed*(29 + 0.5 + (793.0/25920))

def _hebrewCalendarElapsedDays(year):
	"""
	Elapsed days since start of epoch
	
	Argument:
	year - Hebrew year
	
	Return value:
	integer - days
	"""
	monthsElapsed = int(math.floor((235*year - 234)/19.0))
	partsElapsed = 12084 + 13753*monthsElapsed
	day = 29 * monthsElapsed + int(math.floor(partsElapsed/25920.0))
	if (3*(day + 1) % 7) < 3:
		return day + 1
	else:
		return day

def _hebrewNewYearDelay(year):
	"""
	Delay New Year 0, 1 or 2 days if the year otherwise will be of a illegal length
	
	Argument:
	year - Hebrew year
	
	Return value:
	[0, 1, 2]
	"""
	ny0 = _hebrewCalendarElapsedDays(year - 1)
	ny1 = _hebrewCalendarElapsedDays(year)
	ny2 = _hebrewCalendarElapsedDays(year + 1)
	if (ny2 - ny1) == 356:
		return 2
	elif (ny1 - ny0) == 382:
		return 1
	else:
		return 0

def _hebrewNewYear(year):
	"""
	Fixed day number for Hebrew New Year.
	
	Argument:
	year - Hebrew year
	
	Return value:
	integer - fixed day number
	"""
	return HEBREWEPOCH + _hebrewCalendarElapsedDays(year) + _hebrewNewYearDelay(year)

def _daysInHebrewYear(year):
	"""
	Number of days in a Hebrew year
	
	Argument:
	year - Hebrew year
	
	Return value:
	integer - days
	"""
	return _hebrewNewYear(year + 1) - _hebrewNewYear(year)

def _isLongMarheshvan(year):
	"""
	Test if marheshvan is long this year
	
	Argument:
	year - Hebrew year
	
	Return value:
	[True, False]
	"""
	return _daysInHebrewYear(year) in [355, 385]

def _isShortKislev(year):
	"""
	Test if kislev is short this year
	
	Argument:
	year - Hebrew year
	
	Return value:
	[True, False]
	"""
	return _daysInHebrewYear(year) in [353, 383]

def _lastDayOfHebrewMonth(year, month):
	"""
	Number of days in month this year.
	
	Bug, see note 164 in Errata.
	
	Arguments:
	year - Hebrew year
	month - Hebrew month
	
	Return value:
	[29, 30]
	"""
	if month in [2, 4, 6, 10, 13] or \
		(month == 12 and not _isHebrewLeapYear(year)) or \
		(month == 8 and not _isLongMarheshvan(year)) or \
		(month == 9 and _isShortKislev(year)):
		return 29
	else:
		return 30

def fixedFromHebrew(year, month, day):
	"""
	Convert an Hebrew date to fixed day number.

	Arguments:
	year - Hebrew year
	month - Hebrew month
	day - Hebrew day
	
	Use the constants NISAN, SIVAN, TAMMUZ, AV, ELUL, TISHRI, MARHESHVAN,
	KISLEV, TEVET, SHEVAT, ADAR, ADARI or ADARII for Hebrew month.
	
	Return value:
	integer - fixed day number
	
	Example:
	>>> fixedFromHebrew(5756, SHEVAT, 15)
	728694
	"""
	if month < TISHRI:
		ms = range(TISHRI, _lastMonthOfHebrewYear(year) + 1) + range(NISAN, month)
	else:
		ms = range(TISHRI, month)
	return _hebrewNewYear(year) + day - 1 + sum(map((lambda x: _lastDayOfHebrewMonth(year, x)), ms))

def hebrewFromFixed(date):
	"""
	Convert fixed day number to Hebrew date.
	
	Argument:
	date - fixed day number
	
	Return value:
	[integer, [1..13], [1..30]] - [year, month, day]
	
	Examples:
	>>> hebrewFromFixed(728694)
	[5756, 11, 15]
	"""
	approx = int(math.floor((date - HEBREWEPOCH)/(35975351.0/98496))) + 1
	y = approx - 1
	while _hebrewNewYear(y) <= date:
		y = y + 1
	year = int(y - 1)
	if date < fixedFromHebrew(year, NISAN, 1):
		start = TISHRI
	else:
		start = NISAN
	m = start
	while not date <= fixedFromHebrew(year, m, _lastDayOfHebrewMonth(year, m)):
		m = m + 1
	month = m
	day = date - fixedFromHebrew(year, month, 1) + 1
	return [year, month, day]

# test functions
def _test():
	import doctest
	doctest.testmod()

if __name__ == "__main__":
	_test()
### EOF