from Tkinter import *
from tkFileDialog import askdirectory
from tkMessageBox import askyesno
import os, fnmatch, shutil, subprocess, psycopg2, glob, sys
from ESM_dictionaries import dict
import tkMessageBox

class collect_tif:
    def getpath(self):
        Tk().withdraw()
    
        options = {}
        options['initialdir'] = "B:\DTP DEPARTMENT\_Projects MOCA"
        options['title'] = 'ESM Files Investigation'
    
        fp = askdirectory(**options)
        filePath = fp + "/_Illustration investigation/"
        return filePath
    
    def collect(self, filePath):
        all_list = filePath + "all.txt"
        f = open(all_list, 'r')
        file_list = []
        with open(all_list, 'r') as f:
            for line in f:
                file_list.append(line.rstrip('\n'))
        return file_list

    def fetch_files(self, filePath):
        if askyesno("ESM Investigation", "Is this the correct path?\n%s" %filePath):
            global langauges
            languages = x.selected_languages()
            x.check_in_libraries(path, languages)
        else:
            pass
        
    def selected_languages(self):
        cmd = "python tk_check.py"
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        result = out.split('\n')
        strlan = ''.join(result)
        a = strlan.replace("', '", " ")
        a = a.replace(a[-3:],'')
        a = a.replace(a[:2], '')
        a = a.split()
        return a
    
    def illustfolder(self, language):
        illustfolders = dict["illustfolders"]
        dictlist = []
        for key, value in illustfolders.iteritems():
            dictlist.append(value)
        for value in dictlist:
            if value[0] == language:
                lang = value[1]
            else:
                pass
        return lang
    
    def check_in_libraries(self, filePath, languages):
#        print languages
        for language in languages:
            table = language
            print "=" * 150
            print "Checking in %s language" %table
            print "=" * 150
            files_not_found = []
            for file in x.collect(filePath):
                lang = x.illustfolder(language)
                df = os.path.join(filePath, "Illust_%s" %lang)
                try:
                    os.stat(df)
                except:
                    os.mkdir(df)
                if x.search_file(table, file):
                    sf = x.get_file_path(table, file)
                    print "--> Copying file %s..." %file
                    shutil.copy2(sf, df)
                else:
                    files_not_found.append(file)
            x.copy_default_files(filePath, df)
            if files_not_found:
                print "The following files are missing from %s library:" %table
                for file in files_not_found:
                    print file
#            print files_not_found

    def search_file(self, table, filename):
        conn = esm_invest().establishConnection('filelist')
        cur = conn.cursor()
        cur.execute("""SELECT exists (SELECT 1 FROM %s WHERE filename ~* '%s' LIMIT 1);""" %(table, filename))
        exists = cur.fetchone()[0]
#        print filename, exists
        return exists

    def copy_default_files(self, filePath, df):
        zz_folder = os.path.join(filePath, "__ZZ")
#        print zz_folder
        jc_jr_folder = os.path.join(filePath, "__JC_JR")
#        print jc_jr_folder
        notext = os.path.join(filePath, "_NEW/NoTEXT")
        numbers = os.path.join(filePath, "_NEW/NUMBERS")
        for file in os.listdir(zz_folder):
            if not file.endswith(".db"):
                zz = os.path.join(zz_folder, file)
                shutil.copy2(zz, df)
        for file in os.listdir(jc_jr_folder):
            if not file.endswith(".db"):
                jc_jr = os.path.join(jc_jr_folder, file)
                shutil.copy2(jc_jr, df)
        for file in os.listdir(notext):
            if not file.endswith(".db"):
                nt = os.path.join(notext, file)
                shutil.copy2(nt, df)
        for file in os.listdir(numbers):
            if not file.endswith(".db"):
                nr = os.path.join(numbers, file)
                shutil.copy2(nr, df)
        
    
    def get_file_path(self, table, filename):
        conn = x.establishConnection('filelist')
        cur = conn.cursor()
        cur.execute("""SELECT filepath FROM %s WHERE filename ~* '%s' LIMIT 1;""" %(table, filename))
        fp = os.path.join(cur.fetchone()[0], filename)
        return fp
            
    def search_file(self, table, filename):
        conn = x.establishConnection('filelist')
        cur = conn.cursor()
        print table, filename
        cur.execute("""SELECT exists (SELECT 1 FROM %s WHERE filename ~* '%s' LIMIT 1);""" %(table, filename))
        exists = cur.fetchone()[0]
        print filename, exists
        return exists
    
    def establishConnection(self, db):
        conn = psycopg2.connect("dbname='%s' user='postgres' host='10.0.1.200' password='123456'" %db)
        return conn
        

x = collect_tif()
path = x.getpath()
print x.fetch_files(path)

print "=" * 100
print "TASK COMPLETED"