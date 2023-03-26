# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 20:40:30 2023

@author: admin
"""

import difflib
import pandas as pd
import multiprocessing
import scraper
import ast

def process(titleOrIsbns,function_name, queue):
    for i, titleOrIsbn in enumerate(titleOrIsbns):        
        my_function = getattr(scraper, function_name)
        data = my_function(titleOrIsbn["value"])
        queue.put((function_name,titleOrIsbn["index"],titleOrIsbn["value"], data))

#Bu fonksiyon verilen aralıkta ve verilen seçime göre aranacak değerleri getiren fonksiyon
def getData(datas, rowName):       
    dataArray = []
    for index, data in datas.iterrows():
        #Bu kısımda herhangi boş bir değer varsa listeye alır.
        if data.isnull().values.any():
            if str(data[rowName]) != "nan":
                dataArray.append({"index":index, "value":data[rowName]})    
        else:
            pass
    return dataArray

#Stringlerin benzerliğini hesaplayan fonksiyon bu şekilde 1 kaç harf hatasından eşleşmayen verileri doğru kabul eder.
def stringSimilar(str1,str2):
    matcher = difflib.SequenceMatcher(None, str1, str2)
    similarity_ratio = matcher.ratio()
    if similarity_ratio > 0.90:
        return True
    else:
        return False

#scraper.py dosyamdaki fonksiyon isimlerini alan fonksiyon ilerde farklı bir site eklenirse 
#app.py dosyasında hiç bir değişiklik yapmadan datanın kaça bölünmesi gerektiği ve kaç fonksiyon çalıştırması gerektiği veren fonsiyon

def scraperFunctions():
    with open("scraper.py") as f:
        source = f.read()

    module = ast.parse(source)
    function_names = [node.name for node in module.body if isinstance(node, ast.FunctionDef)]
    
    return function_names
    
def dataProcessing(datas,data,value):
    totalDataCount = len(data) 
    scraper = scraperFunctions()
    writeData=0
    
    parts = []
    start = 0
    number_of_divisions = len(scraper)
    for i in range(number_of_divisions):
        finish = start + len(data[i::number_of_divisions])
        parts.append(data[start:finish])
        start = finish
    
    
    queue = multiprocessing.Queue()
    queue_list = []  
    
    for index, part in  enumerate(parts):
        newprocess = multiprocessing.Process(target=process, args=(part,scraper[index], queue))
        queue_list.append(newprocess)
        newprocess.start()
      
    """    
    islem1 = multiprocessing.Process(target=process, args=(split_data[1],"search_idefix_by_title_or_isbn", ilerleme))
    ilerleme_listesi.append(islem1)
    islem2 = multiprocessing.Process(target=process, args=(split_data[2],"search_dr_by_title_or_isbn", ilerleme))
    ilerleme_listesi.append(islem2)
    
    islem1.start()
    islem2.start()   
    """
    for i in range(len(data)):
        function_name,index,dataValue,result = queue.get()
        totalDataCount=totalDataCount-1
        
        #print(function_name) datanın döndüğü fonksiyonun adını yazdırma.
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
                writeData=writeData+1                    
        else:
            print("No search results found:",dataValue)
        print("Number of remaining searches: ",totalDataCount)      
        print("Number of Writing Data: ",writeData)
        
    newprocess.join()
    #islem2.join()    
    
if __name__ == "__main__":
    
    start = input("Please enter initial index: ")
    stop = input("Please enter the ending index: ")
    select = input("Please make your selection:\n1 - Title\n2 - ISBN\n")
    
    if select == "1":
        select ="title"
    elif select == "2":      
        select ="isbn13"
    else:
        print("You have made an invalid choice!")
    
    df = pd.read_csv('books.csv', delimiter=';', dtype=str)
    df['page_count'] = pd.Series(dtype=str)
    datas = df.iloc[int(start):int(stop)]   
    data = getData(datas,select)
    #Güncelemiş değerler csv dosyasına kayıt edilir.
    dataProcessing(df, data, select)
    df.to_csv('books.csv',sep=';', index=False)
    
    
