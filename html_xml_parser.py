from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from simple_colors import *
from docx import Document
from docx.shared import Inches
from docx.enum.style import WD_STYLE_TYPE

time_start = time.time()
os.chdir(r"E:\OneDrive\mekansal_planlama\TUCBS\genisletme\xml\jeoteknik_final\prep")
file = open("jeoteknikEtud.v030.xml", mode="r")

codeListHtml = str()
featureTypeHtml = str()

def ConvertTurkishCharacter(tempString):      
    try:
        tempString = tempString.replace("Ã¼", "ü").replace(';', '')
        tempString = tempString.replace("&#231", "ç").replace(';', '')
        tempString = tempString.replace("Ã¶", "ö").replace(';', '')
        tempString = tempString.replace("&#214", "Ö").replace(';', '')
        tempString = tempString.replace("Ã§", "ç").replace(';', '')
        tempString = tempString.replace('Ä±', 'ı')
        tempString = tempString.replace('ÅŸ', 'ş')
        tempString = tempString.replace('ÄŸ', 'ğ')
        tempString = tempString.replace('Ä°', 'İ')
        tempString = tempString.replace('Ã–', 'Ö')
        tempString = tempString.replace('&#220', 'Ü')
        tempString = tempString.replace('&#226', 'â')    
    except:
        None    
    return tempString

content = file.read()
soup = BeautifulSoup(content, "lxml")
soup.encode("utf-8")


for element in soup.find_all("element", attrs={"xmi:type": "uml:Class"}):
    element_name = element.get("name")
    
    for a in element.find_all("properties", attrs={"stereotype": "codeList"}):
        elementStereotype = a.get("stereotype")
               
        if elementStereotype == "codeList":
           
            
            for properities in element.find_all("properties", attrs={"stereotype": "codeList"}):
        
                element_explanation = properities.get("documentation")
                element_explanation = ConvertTurkishCharacter((element_explanation))

                
                header=f'\n\n## {element_name}\n\
> **Tanım**: {element_explanation}\n\
> **Esneklik**: Açık\n\
> **Tanımlayıcı**: http://cbstr.csb.gov.tr/kodlistesi/...\n\
> **Stereotip**: «codeList»\n'

                html_header = f'<table border="1" class="tucbs-table" id="{element_name}">\n\
<thead>\n\
 <tr>\n\
  <th><a class="Degerler">Değerler</a></th>\n\
 </tr>\n\
</thead>\n\
<tbody>\n'

                codeListHtml += header
                codeListHtml += html_header
                
                for j in element.find_all("attribute"):
                    attribute_name = j.get("name")
                    html_body = f"<tr>\n\
 <td>{attribute_name}</td>\n\
</tr>\n"   
                    codeListHtml += html_body                
                codeListHtml += "</tbody>\n\
</table>"
 
    for a in element.find_all("properties", attrs={"stereotype": "featureType"}):
        elementStereotype = a.get("stereotype")
        print(elementStereotype)
               
        if elementStereotype == "featureType":
            for properities in element.find_all("properties", attrs={"stereotype": "featureType"}):
        
                element_explanation = properities.get("documentation")
                element_explanation = ConvertTurkishCharacter((element_explanation))

                
                header=f'\n## {element_name}\n\
> **Ana paket**: Jeoloji\n\
> **Tanım**: {element_explanation}\n\
> **Stereotip**: «<a class="sozluk">{elementStereotype}</a>»\n'

                html_header =  f'<table border="1" class="tucbs-table" id="{element_name}">\n\
<thead>\n\
 <tr>\n\
  <th><a class="sozluk">Öznitelik</a></th>\n\
  <th><a class="sozluk">Tip</a></th>\n\
  <th><a class="sozluk">Stereotip</a></th>\n\
  <th><a class="sozluk">Çokluk</a></th>\n\
 </tr>\n\
</thead>\n\
<tbody>'

                featureTypeHtml += header
                featureTypeHtml += html_header
                
                for j in element.find_all("attribute"):
                    attribute_name = j.get("name")
                    for c in j.find_all("properties"):
                        attribute_type= c.get("type")
                    for strtype in j.find_all("stereotype"):
                        stereotype = strtype.get("stereotype")
                        if stereotype == None:
                            stereotype =""
                    for bound in j.find_all("bounds"):
                        lowerBound = bound.get("lower")
                        upperBound = bound.get("upper")
                        multiplicity = f"[{lowerBound}..{upperBound}]"                    
                    html_body = f"\n<tr>\n\
 <td>{attribute_name}</td>\n\
 <td>{attribute_type}</td>\n\
 <td>{stereotype}</td>\n\
 <td>{multiplicity}</td>\n\
</tr>"   
                    featureTypeHtml += html_body                
                featureTypeHtml += "\n</tbody>\n\
</table>\n\n"
             
            
                    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
