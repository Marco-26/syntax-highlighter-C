class Reader:
  def __init__(self, content:str):
    self.current_index = 0
    self.content = content
    self.content_length = len(content)
  
  def peek(self):
    return self.content[self.current_index]
  
  def advance(self):
    self.current_index += 1
  
  def at_end(self) -> bool:
    return self.current_index >= self.content_length
  