#!/usr/local/bin/python3


from datetime import datetime


class Log:
    __fileName = None


    def __init__(self):
        self.__fileName = datetime.now().strftime("%Y%m%d") + ".log"


    def __write(self, prmText, prmType="INFO"):
        """
            function that write a specific text in a specific file

            Args:
                prmText: text to write
                prmType: type of log
        """
        nbCharacter = 0
        with open(self.__fileName, 'a', encoding="UTF-8") as file:
            nbCharacter = file.write("[{}] {} {}\n".format(prmType, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), prmText))
        file.closed
        return nbCharacter


    def error(self, prmText):
        return self.__write(prmText=prmText, prmType="ERROR")


    def info(self, prmText):
        return self.__write(prmText=prmText, prmType="INFO")


    def debug(self, prmText):
        return self.__write(prmText=prmText, prmType="DEBUG")


    def warning(self, prmText):
        return self.__write(prmText=prmText, prmType="WARNING")
