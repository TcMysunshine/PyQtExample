from LoggerPyQt.Logger import loggerFile, loggerTimeRotate


if __name__ =='__main__':
    loggerFile = loggerFile("LoggerFile")
    loggerTimeRotate = loggerTimeRotate("LoggerTimeRotate")
    
    fileLogger = loggerFile.getLogger()
    timeRotateLogger = loggerTimeRotate.getLogger()
    
    fileLogger.info("hi")
    timeRotateLogger.info("hh")