import Config

def Log(s: str):
    if Config.WriteLogsToStdout:
        print(s)
    if Config.WriteLogsToFile:
        with open(Config.LogFileName, 'w') as file:
            file.write(s)