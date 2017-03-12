

#  The StateMachine keeps track of the current state, which is
#  is initialized by the constructor. 
#
#  The runAll( ) method takes a list of Input objects ("actions"), 
#  and for each action:
#
#   o moves to the next state invoking the next() method 
#     on the State object;
#
#   o invokes run() on the new state.
#

def gen_timeline (start_date, num_months):


  time_line = [ start_date ]

  start_year  = start_date / 100
  start_month = start_date % 100

  #print("# Start %i:%i" % (start_year, start_month) )
  month = start_month
  year = start_year
  for i in range(1, num_months):

    month += 1
    #print("# Process month %i " % (month ))

    if ( month == 13 ):
      month = 1
      year += 1

    res = 100*year + month

    #print("#   result = %i " % res)

    time_line.append(res)

  return time_line
  #return map(str, time_line)



class StateMachine:

  def __init__(self, initialState):

    # This is a State object
    self.currentState = initialState

    # Invoke State.run()
    #self.currentState.run()


  def runAll(self, date_, num_months_, customer_id_):

    timeline = gen_timeline(date_, num_months_)

    
    for date in timeline:
      if not self.currentState.alive:
        break

      m1 = 12 * (date / 100) + date % 100
      m0 = 12 * (self.currentState.dob / 100)  + self.currentState.dob % 100

      months = m1 - m0
      #print("# months = %i" % months)

      years = months/12

      print("#---")
      print("# Time stamp %i, Income %i, Expense %i, Age %i" % (date, self.currentState.income, self.currentState.expense, years))
      self.currentState = self.currentState.next({'dob':self.currentState.dob, 'date':date, 'income':self.currentState.income, 'expense':self.currentState.expense, 'alive':self.currentState.alive, 'con': self.currentState.con})
      self.currentState.run(customer_id_)



