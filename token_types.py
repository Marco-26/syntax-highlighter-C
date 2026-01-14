from enum import Enum

class TokenType(Enum):
  PREPOC = "prepoc", # #include, #define, #if, etc.
  KEYWORD = "keyword" # if, return, while, typedef,
  TYPE = "type" #int, char, float, void,
  IDENT = "ident" # names
  NUMBER = "number"
  STRING_LITERAL = "string_literal", # everything inside double quote ""
  CHAR = "char" # everything inside ''
  COMMENT = "commment" # everything followed by // or /* */
  OP = "operators" # + -
  WHITESPACE = "whitespace" # /n
  PUNCTUATORS = "punctuators" # ; ( ) [ ] { }
  UNKNOWN = "unknown" # unknown tokens