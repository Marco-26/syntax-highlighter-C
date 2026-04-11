from enum import Enum, auto

class LexerStates(Enum):
  NORMAL = "normal",
  NUMBER = "number",
  STRING = "string"
  
class LexerEvents(Enum):
  FOUND_QUOTATION_MARKS = "found_quotation_marks",
  FOUND_NUMBER = "found_number"
  
class LexerDirective(Enum):
  CONTINUE = auto()

class LexerStateMachine:
  def __init__(self) -> None:
    self.current_state = LexerStates.NORMAL
    
  def switch_state(self, new_state: LexerStates) -> None:
    self.current_state = new_state
  
  def on_event(self, event: LexerEvents, action, *actionArgs) -> None:
    match(event):
      case LexerEvents.FOUND_QUOTATION_MARKS:
        
        if self.current_state == LexerStates.STRING:
          self.switch_state(LexerStates.NORMAL)
        else:
          self.switch_state(LexerStates.STRING)
          
        return action(*actionArgs)
      case LexerEvents.FOUND_NUMBER:
        if self.current_state == LexerStates.NUMBER:
          self.switch_state(LexerStates.NUMBER)
          action(*actionArgs)
          return
        
        self.switch_state(LexerStates.NUMBER)
        return
    
  @property
  def state(self) -> LexerStates:
    return self.current_state