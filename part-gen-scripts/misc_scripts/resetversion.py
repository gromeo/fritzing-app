#	TODO:
#		check for incomplete parts (missing views)
#       check if svgs are plain copies of already existing ones and link them instead?
#       check for conflicting names

# lots of borrowing from http://code.activestate.com/recipes/252508-file-unzip/

import getopt, sys, os, os.path, re, zipfile, shutil
    
def usage():
    print """
usage:
    resetversion.py -f [from directory] -t [to directory]

Change the version number of the fz file in the fzz files in from directory and save to to directory.
"""
           
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:t:", ["help", "from", "to"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        return
    
    inputdir = None
    outputdir = None
    
    for o, a in opts:
        #print o
        #print a
        if o in ("-f", "--from"):
            inputdir = a
        elif o in ("-t", "--to"):
            outputdir = a
        else:
            print "unhandled option",o
            usage()
            return
    
    if not(inputdir):
        print "missing 'from' argument"
        usage()
        return
        
    if not(outputdir):
        print "missing 'to' argument"
        usage()
        return
        
    try:
        import zlib
        compression = zipfile.ZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED

    for fzz in os.listdir(inputdir):
        if not fzz.endswith('.fzz'):
            continue
            
        print fzz
        fzzpath = os.path.join(inputdir, fzz)
        
        tempDir = inputdir + os.sep + "___temp___"
        shutil.rmtree(tempDir, 1)
        os.mkdir(tempDir)

        zf = zipfile.ZipFile(fzzpath)
        zf.extractall(tempDir)
        zf.close()
        
        for fz in os.listdir(tempDir):
            if not fz.endswith(".fz"):
                continue
                
            try: 
                fzpath = os.path.join(tempDir, fz)
                infile = open(fzpath, "rb")
                #print "opened", fzpath
                xml = infile.read()
                infile.close()
                os.remove(fzpath)
                outfile = open(fzpath, 'wb')
                outfile.write( xml.replace('fritzingVersion="0.8.6', 'fritzingVersion="0.8.5'))
                outfile.close()   
            except:
                print "exception", fzpath, sys.exc_info()[0]
                pass    

        # helpful examples in http://www.doughellmann.com/PyMOTW/zipfile/

        zf = zipfile.ZipFile(os.path.join(outputdir, fzz), mode='w')
        for fn in os.listdir(tempDir):
            zf.write(os.path.join(tempDir, fn), fn, compression)
        zf.close()

        shutil.rmtree(tempDir, 1)

if __name__ == "__main__":
    main()


