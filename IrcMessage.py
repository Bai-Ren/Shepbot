class IrcMessage:
    def __init__(self, tags={}, source="", command="", channel="", data=""):
        self.tags = tags
        self.source = source
        self.command = command
        self.channel = channel
        self.data = data
    def __init__(self, rawMessage):
        i = 0
        dataIndex = 0
        parts = rawMessage.split(" ")
        if parts[i][0] == '@':
            tagsText = parts[i][1:]
            dataIndex += len(parts[i]) + 1
            i += 1
            tagDict = {}
            tags = tagsText.split(";")
            for tag in tags:
                splitTag = tag.split("=")
                tagDict[splitTag[0]] = splitTag[1]
                self.tags = tagDict
        else:
            self.tags = {}
        if parts[i][0] == ':':
            self.source = parts[i][1:].split("!")[0]
            dataIndex += len(parts[i]) + 1
            i += 1
        else:
            self.source = ""
        if parts[i] == "CAP":
            self.command = "CAP"
            self.channel = ""
            self.data = ""
        else:
            self.command = parts[i]
            self.channel = parts[i+1]
            dataIndex += len(parts[i]) + len(parts[i+1]) + 3
            self.data = rawMessage[dataIndex:]