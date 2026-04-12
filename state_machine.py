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
  SAVE_TOKEN = auto()

class LexerStateMachine:
  def __init__(self) -> None:
    self.current_state = LexerStates.NORMAL
    
  def switch_state(self, new_state: LexerStates) -> None:
    self.current_state = new_state
  
  def on_event(self, event: LexerEvents) -> LexerDirective:
    match(event):
      case LexerEvents.FOUND_QUOTATION_MARKS:
        if self.current_state == LexerStates.STRING:
          self.switch_state(LexerStates.NORMAL)
          return LexerDirective.SAVE_TOKEN
        
        self.switch_state(LexerStates.STRING)
        return LexerDirective.CONTINUE
    
  @property
  def state(self) -> LexerStates:
    return self.current_state