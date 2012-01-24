"""
JHolidays.py is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

JHolidays.py is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Jewish holiday flags.

Dov Grobgeld

Reference:
   - http://www.david-greve.de/luach-code/holidays.html
"""
import calendrical

# Enums
class Pesach:
  pass
class LagBOmer:
  pass
class YomYerushalayim:
  pass
class Sukkot:
  pass
class Shavuot:
  pass
class TuBeAv:
  pass
class YomKippur:
  pass
class RoshHashana:
  pass
class ShminiAtzeret:
  pass
class SimchatTorah:
  pass
class ZomTamuz:
  pass
class ZomAv:
  pass
class ZomGedaliya:
  pass
class ZomEsther:
  pass
class HoshanaRaba:
  pass
class Hannuka:
  pass
class TuBeshvat:
  pass
class Purim:
  pass
class ShushanPurim:
  pass
class YomHazikaron:
  pass
class YomHaatzmaut:
  pass

def getWeekdayOfHebrewDate(hebYear, hebMonth, hebDay):
  fixed = calendrical.fixedFromHebrew(hebYear, hebMonth, hebDay)
  return calendrical.dayOfWeekFromFixed(fixed)

def buildHolidays(hebYear,isDiaspora=False):
  """Build a dictionary of all Jewish holidays of the given year"""
  if calendrical._isHebrewLeapYear(hebYear):
    monPurim = 13
  else:
    monPurim = 12

  holidays = {
    (1,15) : [Pesach],
    (1,16) : [Pesach],
    (1,17) : [Pesach],
    (1,18) : [Pesach],
    (1,19) : [Pesach],
    (1,20) : [Pesach],
    (1,21) : [Pesach],
    (2,18) : [LagBOmer],
    (2,28) : [YomYerushalayim],
    (3,6): [Shavuot],
    (4,17+(getWeekdayOfHebrewDate(hebYear,4,17)==6)) : [ZomTamuz],
    (5,9+(getWeekdayOfHebrewDate(hebYear,5,9)==6)) : [ZomAv],
    (5,15) : [TuBeAv],
    (7,1) : [RoshHashana],
    (7,2) : [RoshHashana],
    (7,3+(getWeekdayOfHebrewDate(hebYear,7,3)==6)) : [ZomGedaliya],
    (7,10) : [YomKippur],
    (7,15) : [Sukkot],
    (7,16) : [Sukkot],
    (7,17) : [Sukkot],
    (7,18) : [Sukkot],
    (7,19) : [Sukkot],
    (7,20) : [Sukkot],
    (7,21) : [HoshanaRaba],
    (7,22) : [ShminiAtzeret,SimchatTorah],
    (9,25) : [Hannuka],
    (9,26) : [Hannuka],
    (9,27) : [Hannuka],
    (9,28) : [Hannuka],
    (9,29) : [Hannuka],
    (10,1) : [Hannuka],
    (10,2) : [Hannuka],
    (11,15) : [TuBeshvat],
    (monPurim,11+2*(getWeekdayOfHebrewDate(hebYear,monPurim,13)!=6)):[ZomEsther],
    (monPurim,14) : [Purim],
    (monPurim,15) : [ShushanPurim],
    }
  
  if calendrical._lastDayOfHebrewMonth(hebYear, 9) == 30:
    holidays.update({(9,30):[Hannuka]})
  else:
    holidays.update({(10,3):[Hannuka]})

  if isDiaspora:
    # ShminiAtzeret will override the table above
    holidays.update({(1,22) : [Pesach],
                     (3,7) : [Shavuot],
                     (7,22) : [ShminiAtzeret],
                     (7,23) : [SimchatTorah],
                     })
    

  # Yom Hazikaron and Yom Haatzmaut are complicated
  WDay_2_4=getWeekdayOfHebrewDate(4, 2, hebYear)
  if WDay_2_4 == 5: # Thursday
    YZDay=2
  elif WDay_2_4 == 4:
    YZDay=3
  elif hebYear >= 5764 and WDay_2_4 == 0:
    YZDay=5
  else:
    YZDay=4
  holidays.update({(2,YZDay): YomHazikaron,
                   (2,YZDay+1): YomHaatzmaut})
  
  return holidays
  
def getJHolidayList(date, isDiaspora=False, isNightFall=False):
  fixed = calendrical.fixedFromGregorian(date.year, date.month, date.day)
  if isNightFall:
    fixed+=1
  hebDate = calendrical.hebrewFromFixed(fixed)
  hebYear, hebMonth, hebDay = hebDate

  holidays = buildHolidays(hebYear,isDiaspora)
  key = (hebMonth,hebDay)
  if key in holidays:
    return holidays[key]
  else:
    return []

def getCalendarFlags(date, isDiaspora, isNightFall):
    """Get a regexp match for the date"""
    holidays = getJHolidayList(date, isDiaspora, isNightFall)

    flags = []
    if Pesach in holidays:
      flags += ['pesah']
    elif Shavuot in holidays:
      flags += ['shavuot']
    elif ShminiAtzeret in holidays:
      flags += ['shemini']
    elif Purim in holidays:
      flags += ['purim']
    elif Hannuka in holidays:
      flags += ['hanukka']

    # Check for rosh chodesh
    fixed = calendrical.fixedFromGregorian(date.year, date.month, date.day)
    hebrew_date = calendrical.hebrewFromFixed(fixed)
    hebYear, hebMonth, hebDay = hebrew_date[0], hebrew_date[1], hebrew_date[2]
    if hebDay == 1 or hebDay == 30:
      flags += ['rosh-hodesh']

    # Other flags. TBD - Add more

    # Omer
    if ((hebMonth == 1 and hebDay>15) 
        or hebMonth == 2
        or (hebMonth == 3 and hebDay < 6)):
        flags += ['Omer']

    # LeDavid
    if (hebMonth == 6
        or (hebMonth == 7 and hebDay < 22)):
        flags += ['LeDavid']

    # tshuva
    if (hebMonth == 7 and hebDay < 10):
        flags += ['tshuva']

    return "|".join(flags)

if __name__=='__main__':
  import datetime
  print getJHolidayList(datetime.date(2012,7,29))
