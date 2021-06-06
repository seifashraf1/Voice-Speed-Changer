def updateHeader (byteRate, byteNum, factor):
    if byteNum==4:
        nbyteRate = byteRate[6:2]
    elif byteNum==1:
        nbyteRate = byteRate[2:] + byteRate[:2]
    
    byteRate2 = int(nbyteRate, 16)
    byteRate2 = int (byteRate2 * factor)
    byteRate2 = str(byteRate2)

    if len(byteRate2) < byteNum*2:
        i = 0
        while i < byteNum*2 - len(byteRate2):
            byteRate2 = "0" + byteRate2
            i = i + 1
            
    updatedByteRate = byteRate2[6:2]

    return updatedByteRate

def stereo2Mono (header, mono):
    monofile = open(mono, 'wb')
    
    fmtchunk = header.find("666d7420")
    datachunk = header.find("64617461")

    numChannels = header[fmtchunk+22:fmtchunk+23]
    byteRate    = header[fmtchunk+28:fmtchunk+31]   
    blockAlign  = header[fmtchunk+32:fmtchunk+33]    

    updatedNumChannels = updateHeader(numChannels,1,2)
    updatedByteRate    = updateHeader(byteRate,4,2)
    updatedBlockAlign  = updateHeader(blockAlign,2,2)

    subchunk2Size = header[datachunk+4:datachunk+7]
    updatedSubchunk2Size = updateHeader(subchunk2Size,4,2)

    newHeader =  header[:fmtchunk+20]+ updatedNumChannels + header[fmtchunk+24:fmtchunk+27] + updatedByteRate + updatedBlockAlign + header[fmtchunk+44: datachunk+4]+\
                  updatedSubchunk2Size+ header[datachunk+8:]

    stereoHeader = bytearray.fromhex(newHeader)

    monofile.write(stereoHeader)
    return

def stretch (header, stretchedWave, factor):
    stereofile = open(stretchedWave, 'wb')
    
    fmtchunk = header.find("666d74")
    datachunk = header.find("64617461")

    sampleRate  = header[fmtchunk+24:fmtchunk+27]
    byteRate    = header[fmtchunk+28:fmtchunk+31] 

    updatedByteRate    = updateHeader(byteRate, 4, factor)
    updatedSampleRate  = updateHeader(sampleRate,4, factor)

    newHeader = header[:fmtchunk + 24] + updatedSampleRate + updatedByteRate + header[fmtchunk + 40:]

    stereoHeader = bytearray.fromhex(newHeader)

    stereofile.write(stereoHeader)

    return

    wave = open("myvoice.wav", 'rb')

    header = ""
    for chunk in wave:
        hexvalue = chunk.hex()
        header = header + " " + str(hexvalue)

    stereo2Mono (header, "mono.wav")

    wave2 = open("mono.wav", 'rb')

    header2 = ""
    for chunk2 in wave2:
        hexvalue2 = chunk2.hex()
        header2 = header2 + " " + str(hexvalue2)

    stretch("mono.wav", "streched.wav",1)
