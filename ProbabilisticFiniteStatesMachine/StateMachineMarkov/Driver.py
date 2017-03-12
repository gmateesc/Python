import random
import string, sys
import numpy as np
import py_mysql

#sys.path += ['./stateMachine', './']

from State        import State
from StateMachine import StateMachine

#
# Time based thresholds
#
turn18 = 2
turn25 = 3
turn65 = 5
turn110 = 7




#
# Check if the age of a person 
# has reached the age threshold
#
def check_age (dob, info, age):
  date = info['date'] 

  m1 = 12 * (date / 100) + date % 100
  m0 = 12 * (dob / 100)  + dob % 100

  months = m1 - m0
  #print("# months = %i" % months)

  years = months/12
  #print("# years = %i" % years)

  if ( years - age ) >= 0:
    return 1
  else:
    return 0


def randomStateChange(info, probs):
  # expects list of state transition probabilities:
  #[p_unemployed,  p_employed, p_student, p_retired]
  dice = random.uniform(0,1)
  if dice < sum(probs[0:1]):
    print("#   graduate to unemployed")
    return Unemployed(info)
  elif dice < sum(probs[0:2]):
    print("#   graduate to employed2")
    return Employed(info)
  elif dice < sum(probs[0:3]):
    print("#   graduate to student")
    return Student(info)
  else :
    print("#   graduate to retired")
    return Retired(info)



class Start(State):


    #
    # Check for time-events
    #

  def next(self, info):
    res = check_age(self.dob, info, turn65)
    if res:      
      print("#   graduate to retired")
      return Retired(info)

    res = check_age(self.dob, info, turn25)
    if res:
      print("#   graduate to employed or unemployed")
      return Employed(info) 

    res = check_age(self.dob,info, turn18)
    if res:
      print("#   graduate to student")
      return Student(info) 

    print("#   graduate to kid")
    return Kid(info)


#
# 1. The states of the driver are subclasses of State, 
#    with a subclass for each possible state
#

class Kid(State):

  p_sideJob = 0.02
  p_unemployed = 0.2
  p_employed = 0.3  
  p_student = 0.5
  p_retired = 0
  #
  # Stuff done in this state
  #



  #
  # Finds next state or change attrs of current state
  #
  def next(self, info):
    
    res = check_age(self.dob, info, turn18)
    if res:
      return randomStateChange(info, [self.p_unemployed, self.p_employed, self.p_student, self.p_retired])
   
    if info['income'] == 0:
      dice = random.uniform(0,1)
      if dice < self.p_sideJob:
        #print("#I have a job now")
        #print(info)
        info['income'] = 400
        info['expense'] = 300
        
	
    # no state change
    print("#   no state change, kid")
    return self(info)



class Student(State):

  p_drop = 0.2/12

  p_sideJob = 0.4

  p_unemployed = 0.2
  p_employed = 0.8
  p_student = 0
  p_retired = 0

  def __init__(self,  info):
    info['income'] = 1000
    info['expense'] = 800
    print info
    State.__init__(self, info)




  #
  # Finds next state or change attrs of current state
  #
  def next(self, info):

    #print("# Student next state: dob = %i" % self.dob)


    #
    # Check for time-events
    #    
    res = check_age(self.dob, info, turn25)
    if res:
      return randomStateChange(info, [self.p_unemployed, self.p_employed, self.p_student, self.p_retired])
    

    #
    # Check for prob events
    #

    # drops out
    dice = random.uniform(0,1)
    if dice < self.p_drop:
      return Unemployed(info)

    if info['income'] <= 1000 :
      dice = random.uniform(0,1)
      if dice < self.p_sideJob:
        #print("#I have a job now")
        #print(info)
        info['income'] = 2000
        info['expense'] = 1600


    # no state change
    print("#   no state change, Student")
    return self(info)



class Employed(State):


  p_unemployed = 0.03
  p_employed = 0.97
  p_student = 0
  p_retired = 0

  income_avg = 3000
  income_std = 500

  def __init__(self,  info):
    #info['income']  = int(round(np.random.normal(self.income_avg, self.income_std)))
    tmp1 = int(round(np.random.normal(self.income_avg, self.income_std)))
    info['income']  = tmp1
    print (" avg    = ",  self.income_avg )
    print (" std    =  ", self.income_std )
    print (" income =  ", tmp1 )

    #info['expense'] = round( self.income_avg-200, self.income_std)
    #tmp2 = round( self.income_avg-200, self.income_std)
    tmp2 =  self.income_avg - 200
    info['expense'] = tmp2
    print (" avg     = ",  self.income_avg - 200 )
    print (" std     =  ", self.income_std )
    print (" expense =  ", tmp2 )

    print info
    State.__init__(self, info)





  #
  # Find next state or change attrs of current state
  #
  def next(self, info):

    #print("# Employed next state: dob = %i" % self.dob)

    #
    # Check for time-events
    #
    res = check_age(self.dob, info, turn65)
    if res:
      print("#   graduate to retired")
      return Retired(info)


    #
    # Check for prob events
    #

    # fired

    dice = random.uniform(0,1)
    if dice < self.p_unemployed:
      print("#   graduate to Unemployed")
      return Unemployed(info)
    print("#   no state change, Employed")
    return self(info)





class Unemployed(State):

  p_unemployed = 0.9
  p_employed = 0.07
  p_student = 0.03
  p_retired = 0

  income_avg = 3000
  income_std = 500

  def __init__(self,  info):
    info['income'] = info['income']*0.5
    info['expense'] = info['expense']*0.75
    print info
    State.__init__(self, info)

 


  #
  # Find next state or change attrs of current state
  #
  def next(self, info):

    #print("# Unemployed next state: dob = %i" % self.dob)

    #
    # Check for time-events
    #
    res = check_age(self.dob, info, turn65)
    if res:
      print("#   graduate to retired")
      return Retired(info)

    dice = random.uniform(0,1)
    if dice < self.p_employed:
      print("#   graduate to employed1")
      return Employed(info)
    if dice < self.p_employed + self.p_student:
      print("#   graduate to student")
      return Student(info)
    print("#   no state change, Unemployed")
    return self(info)




class Retired(State):


  def __init__(self,  info):
    info['income'] = info['income']*0.7
    info['expense'] = info['expense']*0.75
    print info
    State.__init__(self, info)



  #
  # Find next state or change attrs of current state
  #

  def next(self, info):

    #print("# Retired next state: dob = %i" % self.dob)

    # no state change
    res = check_age(self.dob, info, turn110)
    if res:
      print("#   graduate to dead")
      info['alive'] = False

    print("#   no state change, Retired")
    return self(info)
    




#
# 2. Then Driver class is a subclass of StateMachine
#
class Driver(StateMachine):

  def __init__(self):
    # Initial state is kid
    StateMachine.__init__(self, Driver.start)





#
# 3. Create a sequence of months to pass to the Driver
#

# Map months to int 
#months = map(string.strip, open("./timeline/months.txt").readlines())
#mm = [ mo for mo in months if mo != '']
#months = map(int, mm)
num_months  = 12 * 8


# 
# 4. Possible states of the Driver, are defined as 
#    Static members of the MouseDriver class initializated 
#    with the states defined at 1 above.
#

# month of birth
mob  = 199901

# start date of simulation
#date = months[0]
date = 200001



#
# 5. Get connection to DB
#
con = py_mysql.get_connection( "172.16.0.82", "one_ng")


#
# 6. Create initial state of Driver
#
Driver.start      = Start( {'dob':mob ,'date':date, 'income':0, 'expense':0, 'con': con} )
#Driver.kid       = Kid(mob, date)
#Driver.student   = Student(mob, date)





#
#  5. Run the state machine through the timelines 
#

n_customers = 1;
for customer_id in range(1, n_customers+1):
  Driver().runAll( date,  num_months, customer_id )



#
# Utilities
#

# Example
#res = check_age(201101, 201511, 5)
#print("# Check age %i" % res)

# Example
#res = gen_timeline (201501, 3)
#print res

