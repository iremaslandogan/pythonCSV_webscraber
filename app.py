# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 20:40:30 2023

@author: admin
"""

import difflib
import pandas as pd
import multiprocessing
import scraper

def process(titleOrIsbns,function_name, ilerleme):
    for i, titleOrIsbn in enumerate(titleOrIsbns):        
        my_function = getattr(scraper, function_name)
        data = my_function(titleOrIsbn["value"])
        ilerleme.put((titleOrIsbn["index"],titleOrIsbn["value"], data))
        
def getData(datas, rowName):       
    dataArray = []
    for index, data in datas.iterrows():
        if data.isnull().values.any():
            if str(data[rowName]) != "nan":
                dataArray.append({"index":index, "value":data[rowName]})    
        else:
            pass
    return dataArray

def stringSimilar(str1,str2):
    matcher = difflib.SequenceMatcher(None, str1, str2)
    similarity_ratio = matcher.ratio()
    if similarity_ratio > 0.90:
        return True
    else:
        return False
    
def dataProcessing(datas,data,value):
    totalDataCount = len(data)
    yarim_nokta = len(data) // 2 
    
    #sonuclar = multiprocessing.Queue()    
    ilerleme = multiprocessing.Queue()
    ilerleme_listesi = []    
    
    islem1 = multiprocessing.Process(target=process, args=(data[:yarim_nokta],"search_idefix_by_title_or_isbn", ilerleme))
    ilerleme_listesi.append(islem1)
    islem2 = multiprocessing.Process(target=process, args=(data[yarim_nokta:],"search_dr_by_title_or_isbn", ilerleme))
    ilerleme_listesi.append(islem2)
    
    islem1.start()
    islem2.start()   

    for i in range(len(data)):
        index,dataValue,result = ilerleme.get()
        totalDataCount=totalDataCount-1
        print("Kalan arama sayısı: ",totalDataCount)
        #print(f"Index {index} processed, result: {result}")
        if(result != None):
            if(value == "title"):
                dataValue = datas.iloc[index,1]
                stringControl = stringSimilar(datas.iloc[index,1], result[value])
            elif(value == "isbn13"):
                #print(datas.iloc[index,3],result[value])
                dataValue = datas.iloc[index,3]
                stringControl = datas.iloc[index,3] == str(result[value])
            if stringControl == True:
                datas.loc[index] = result                    
        else:
            print("Bu",dataValue,"için sonuç getirmemiştir")
        
    islem1.join()
    islem2.join()    

if __name__ == "__main__":
    
    start = input("Please enter initial index: ")
    stop = input("Please enter the ending index: ")
    secim = input("Please make your selection:\n1 - Title\n2 - ISBN\n")
    
    if secim == "1":
        secim ="title"
    elif secim == "2":      
        secim ="isbn13"
    else:
        print("Geçersiz bir seçim yaptınız!")
    
    df = pd.read_csv('books.csv', delimiter=';', dtype=str)
    datas = df.iloc[int(start):int(stop)]   
    data = getData(datas,secim)
    #print(data)
    dataProcessing(df, data, secim)
    df.to_csv('books.csv',sep=';', index=False)
    
    
