

def magic(rdm_list):
    s = ''.join(map(str, rdm_list))
    return s

context = []
list_digit = []
result = []

NumOfListValue = 0
currentList = []
waitingList = []
transitionList = []

keyOrContent = 'key'
oldKeyOrContent = []
waitingKey = []
waitingDict = []
NumOfDictValue = 0
currentDictionary = {}
dic = []
dictionaryKey = 0

incr = 0
string_content = []

#with open('torrent.torrent','rb') as torrent:
#with open('torrent_simp.torrent','rb') as torrent:
with open('test_list.torrent','rb') as torrent:
    while True :
        ValByte = torrent.read(1)
        decod_ValByte = ValByte.decode('utf-8','backslashreplace')
        
        if ValByte == b'':
            break
        
        if not context:
            if decod_ValByte == 'i':
                context.append('start_num')
                continue
            if decod_ValByte == 'l':
                context.append('list_value')
                NumOfListValue = context.count('list_value')
                continue
            if decod_ValByte == 'd':
                context.append('dictionary')
                NumOfDictValue = context.count('dictionary')
                continue
        
        if context:
            if context[-1] == 'dictionary' or context[-1] == 'list_value':
                if decod_ValByte == 'i':
                    context.append('start_num')
                    continue
                if decod_ValByte == 'l':
                    if NumOfListValue == 0 :
                        context.append('list_value')
                        NumOfListValue = context.count('list_value')
                        continue
                    else:
                        context.append('list_value')
                        NumOfListValue = context.count('list_value')
                        waitingList.append(currentList)
                        currentList = []
                        continue
                if decod_ValByte == 'd':
                    if NumOfDictValue == 0 :
                        context.append('dictionary')
                        NumOfDictValue = context.count('dictionary')
                        continue
                    else:
                        context.append('dictionary')
                        NumOfDictValue = context.count('dictionary')
                        waitingDict.append(currentDictionary)
                        currentDictionary = {}
                        oldKeyOrContent.append(keyOrContent)
                        keyOrContent = 'key'
                        if dictionaryKey:
                            waitingKey.append(dictionaryKey)
                            dictionaryKey = 0
                            continue
                        continue
                if decod_ValByte.isdigit():
                    context.append('string_length')
                    list_digit.append(decod_ValByte)
                    continue


#traitement d'un dictionnaire ---------------------------------------------------------------------

            if context[-1] == 'dictionary':
                if decod_ValByte == 'e':
                    if NumOfDictValue == 1:
                        context.pop()
                        NumOfDictValue = context.count('dictionary')
                        if not context:
                            result.append(currentDictionary)
                            currentDictionary = {}
                            continue
                        if context[-1] == 'list_value':
                            currentList.append(currentDictionary)
                            currentDictionary = {}
                            continue
                    if NumOfDictValue >= 2 :
                        context.pop()
                        NumOfDictValue = context.count('dictionary')
                        transitionDict = currentDictionary
                        keyOrContent = oldKeyOrContent[-1]
                        if context[-1] == 'list_value':
                            currentList.append(currentDictionary)
                            currentDictionary = {}
                            continue
                        if context[-1] == 'dictionary':
                            dictionaryKey = waitingKey[-1]
                            currentDictionary = waitingDict[-1]
                            currentDictionary[dictionaryKey] = transitionDict
                            dictionaryKey = 0
                            keyOrContent = 'key'
                            continue

#traitement d'une liste de valeurs --------------------------------------------------------------

            if context[-1] == 'list_value':
                if decod_ValByte == 'e':
                    if NumOfListValue == 1 :
                        context.pop()
                        NumOfListValue = context.count('list_value')
                        if not context:
                            result.append(currentList)
                            currentList = []
                            continue
                        if context[-1] == 'dictionary':
                            currentDictionary[dictionaryKey]=currentList
                            dictionaryKey = 0
                            currentList = []
                            keyOrContent = 'key'
                            continue
                    if NumOfListValue >= 2 :
                        context.pop()
                        NumOfListValue = context.count('list_value')
                        transitionList = currentList
                        currentList = waitingList[-1]
                        waitingList.pop()
                        currentList.append(transitionList)
                        if not context:
                            result.append(currentList)
                            currentList = []
                            continue
                        if context[-1] == 'dictionary':
                            currentDictionary[dictionaryKey] = currentList
                            dictionaryKey = 0
                            currentList = []
                            keyOrContent = 'key'
                            continue

#traitement d'information brut ------------------------------------------------------------------
            
            if context[-1] == 'string_length':
                if decod_ValByte.isdigit():
                    list_digit.append(decod_ValByte)
                    continue
                if decod_ValByte == ':':
                    context.pop()
                    context.append('string_content')
                    string_length = int(magic(list_digit))
                    incr = 1
                    list_digit = []
                    continue
            if context[-1] == 'string_content':
                if incr != string_length:
                    string_content.append(decod_ValByte)
                    incr += 1
                    continue
                if incr == string_length:
                    context.pop()
                    string_content.append(decod_ValByte)
                    string = magic(string_content)
                    string_content = []
                    incr = 1
                    if not context:
                        result.append(string)
                        continue
                    if context[-1] == 'list_value' :
                        currentList.append(string)
                        continue
                    if context[-1] == 'dictionary':
                        if keyOrContent == 'key':
                            keyOrContent = 'content'
                            dictionaryKey = string
                            continue
                        if keyOrContent == 'content':
                            currentDictionary[dictionaryKey] = string
                            dictionaryKey = 0
                            keyOrContent = 'key'
                            continue
                    
#traitement de numéros -------------------------------------------------------------------------
            
            if context[-1] == 'start_num':
                if decod_ValByte.isdigit() or decod_ValByte == '-':
                    list_digit.append(decod_ValByte)
                    context.pop()
                    old_term = 0
                    context.append('digit')
                    continue
                
            if context[-1] == 'digit':
                if decod_ValByte.isdigit():
                    list_digit.append(decod_ValByte)
                    continue
                if decod_ValByte == 'e':
                    context.pop()
                    number = int(magic(list_digit))
                    list_digit = []
                    print(number)
                    if not context:
                        result.append(number)
                        continue
                    if context[-1] == 'list_value' :
                        currentList.append(number)
                        continue
                    if context[-1] == 'dictionary':
                        if keyOrContent == 'key':
                            keyOrContent = 'content'
                            dictionaryKey = number
                            continue
                        if keyOrContent == 'content':
                            currentDictionary[dictionaryKey] = number
                            dictionaryKey = 0
                            keyOrContent = 'key'
                            continue
                    
                    
                    
                    

print(result)



        
