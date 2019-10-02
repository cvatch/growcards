import os
texttofind = 'no'
texttoreplace = 'yes'
sourcepath = os.listdir('InputFiles/')
for file in sourcepath:
    inputfile = 'Inputfiles/'+ file
    print('Conversion is going for:' +inputfile)
    with open(inputfile,'r') as inputfile:
        filedata = inputfile.read()
        freq = 0
        freq = filedata.count(texttofind)
    destinationpath = 'Outputfile/' + file
    filedata = filedata.replace(texttofind,texttoreplace)
    with open(destinationpath,'w') as file:
        file.write(filedata)
    print ('Total %d Record Replaced' %freq)
