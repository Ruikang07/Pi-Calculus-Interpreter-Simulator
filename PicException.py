# CISC 465 project
# produced by Ruikang Luo
# 2021/04/15

class Error(Exception):
    """Base class for other exceptions"""
    pass

class InvalidPiCalculusSyntax(Error):
    pass

class InvalidPiCalculusCharacter(Error):
    pass