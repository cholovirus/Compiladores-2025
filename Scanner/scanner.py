# gramtica:, comentarios, al menos 2 tipos de datos,
# rango de enteros y flotantes
# ids
# 1 forma de iterar
# una forma de iterar, operadores basicos, operadores de comparacion doble caracter
# palabras reservadas
# lenguaje, abrir video, componer videos, componer videos, 
# delimitadores
#parser top down con tabla,
class Scan:
    def __init__(self,codigo):
        self.code = codigo
        self.pos = 0
        self.newline = 0
        self.len = len(codigo)
        self.tokens = []
        self.operator_ = {
            "+": "+",
            "-": "-",
            "*": "*",
            "/": "/",
            "%": "%",
            "=": "=",
            "==": "==",
            "!=": "!=",
            "<": "<",
            ">": ">",
            "<=": "<=",
            ">=": ">=",
        }
        self.delimiter_ = {
            "(": "(",
            ")": ")",
            "{": "{",
            "}": "}",
            "[": "[",
            "]": "]",
            ",": ",",
            ";": ";"
        }
        self.keyword_ = {
            "if": "if",
            "else": "else",
            "for": "for",
            "input": "input",
            "print": "print",
            "vid": "vid",
            "img": "img",
            "save": "save",
            "concat": "concat"
        }
        self.type_ = {
            "int": "int",
            "float": "float",
            "string": "string",
            "image": "image",
            "video": "video"
        }
        
    def getchar(self):
        if self.pos < self.len:
            char = self.code[self.pos]
            self.pos += 1
            return char
        return None  

    def peekchar(self):
        if self.pos < self.len:
            return self.code[self.pos]
        return None

    def line(self,char):
        if char == "\n":
            self.newline +=1

    def number(self,char):
        posIni = self.pos
        if char.isdigit():
            number = char
            while self.peekchar() and self.peekchar().isdigit():
                number += self.getchar()
                if( len(number) > 20 ):
                    self.tokens.append((number, "🔴 ERROR Overflow int",posIni,self.pos,self.newline))
                    return True 
            
            if self.peekchar() == ".":  
                number += self.getchar()
                if self.peekchar() and self.peekchar().isdigit():
                    while self.peekchar() and self.peekchar().isdigit():
                        number += self.getchar()
                        if( len(number) > 20 ):
                            self.tokens.append((number, "🔴 ERROR Overflow float",posIni,self.pos,self.newline))
                            return True 
                    self.tokens.append((number, "NUMBER",posIni,self.pos,self.newline))
                else:
                    number += self.getchar()
                    self.tokens.append((number, "🔴 ERROR no decimal",posIni,self.pos,self.newline))
                    return True  
                
            else:
                self.tokens.append((number, "NUMBER",posIni,self.pos,self.newline))
            return True
        else:
            return False
    
    def id_keyword(self,char):
        posIni = self.pos
        if char.isalpha():
            identifier = char
            
            while self.peekchar() and (self.peekchar().isalnum() or self.peekchar() == "_"):
                identifier += self.getchar()
            if identifier in self.keyword_ :
                self.tokens.append((identifier, self.keyword_[identifier],posIni,self.pos,self.newline))
            elif identifier in self.type_ :
                self.tokens.append((identifier, self.type_[identifier],posIni,self.pos,self.newline))
            else:
                self.tokens.append((identifier, "IDENTIFIER",posIni,self.pos,self.newline))
            return True
    
        else :
            return False

    def comment(self,char):
        posIni=self.pos
        if char == "#":
            if self.peekchar() == "#":
                self.getchar() 
                comment = "##"
                while self.peekchar():
                    char = self.getchar()
                    comment += char
                    self.line(char)
                    if comment.endswith("##"):
                        break
                self.tokens.append((comment, "COMMENT",posIni,self.pos,self.newline))
            else: 
                comment = "#"
                while self.peekchar():
                    char = self.getchar()
                    comment += char
                    if comment.endswith("\n"):
                        break 
                self.tokens.append((comment, "COMMENT",posIni,self.pos,self.newline))
            return True
        else :
            return False
    
    def string(self,char):
        posIni = self.pos
        if char == '"':
            string = char
            while self.peekchar() and self.peekchar() != '"':
                char =  self.getchar()
                string += char
                self.line(char)
            if self.peekchar() == '"':
                string += self.getchar()  
            self.tokens.append((string, "STRING",posIni,self.pos,self.newline))
            return True
        else :
            return False

    def operator(self, char):
        posIni = self.pos
        lookahead = char + (self.peekchar() or "")

        if lookahead in self.operator_:
            self.tokens.append((lookahead, self.operator_[lookahead], posIni, self.pos, self.newline))
            self.getchar()  # Consumir el segundo carácter
            return True
        elif char in self.operator_:
            self.tokens.append((char, self.operator_[char], posIni, self.pos, self.newline))
            return True
        else:
            return False
            
    def delimiter(self, char):
        posIni = self.pos
        if char in self.delimiter_:
            self.tokens.append((char, self.delimiter_[char], posIni, self.pos, self.newline))
            return True
        else:
            return False

    def gettoken(self):
        while (self.pos < self.len):
            char= self.getchar()
            
            if char.isspace():
                if char == "\n":
                    self.newline +=1
                continue
            
            if self.string(char):
                continue
            elif self.id_keyword(char):
                continue
            elif self.number(char):
                continue
            elif self.comment(char):
                continue
                
            elif self.operator(char):
                continue
            elif self.delimiter(char):
                continue
            else :
                try:
                    afterPos = self.pos-1
                    self.tokens.append((char,"ERROR no Gramatica",afterPos,afterPos,self.newline))
                except IndexError:
                    self.tokens.append((char, "ERROR",0,0,self.newline))
        return self.tokens

