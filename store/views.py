from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup

# Create your views here.


def home(request):
    return render(request,"index.html")


def search(request):
    try:
        
        store=request.GET['store']
        
        if store=='apple':
            appname = request.GET['appname']
            appID = request.GET['appID']

            app_store_url= 'https://apps.apple.com/in/app/'+appname+'/id'+appID

            res=requests.get(app_store_url)
            soup = BeautifulSoup(res.text, 'lxml')

            appName=soup.find_all("h1", class_="product-header__title app-header__title")
            appIcon= soup.find_all("img")
            appDevs=soup.find_all("h2", class_="product-header__identity app-header__identity")
            appDesc=soup.find_all("div", class_="we-truncate we-truncate--multi-line we-truncate--interactive ember-view l-column small-12 medium-9 large-8")
            appInstall="N/A"
            appRating=soup.find_all("div", class_="we-customer-ratings__averages")
            appRatingCount=soup.find_all("div", class_="we-customer-ratings__count small-hide medium-show")


            appDesc_str=""
            for desc in appDesc:
                appDesc_str=appDesc_str+desc.text
            
            if len(appDesc_str)>200:
                appDesc_str=appDesc_str[:200]
                appDesc_str=appDesc_str+"..."



            appIcon=appIcon[0].attrs['src']
            appName=appName[0].getText().strip().splitlines()[0]
            appDevs=appDevs[0].text.strip()
            appDesc_str=appDesc_str.strip()
            appRating=appRating[0].text
            appRatingCount=appRatingCount[0].text

            
        else:
            packagename= request.GET['packagename']
            play_store_url='https://play.google.com/store/apps/details?id='+packagename


            res=requests.get(play_store_url)
            soup = BeautifulSoup(res.text, 'lxml')
            
            appName= soup.find_all("h1")
            appIcon= soup.find_all("img")
            appDevs=soup.find_all("a", class_="hrTbp R8zArc")
            appDesc=soup.find_all("div", class_="DWPxHb")
            appInstall=soup.find_all("span", class_="htlgb")
            appRating=soup.find_all("div", class_="BHMmbe")
            appRatingCount=soup.find_all("span", class_="EymY4b")
            
        
        
            appDesc_str=""
            for desc in appDesc:
                appDesc_str=appDesc_str+desc.text
            
            if len(appDesc_str)>200:
                appDesc_str=appDesc_str[:200]
                appDesc_str=appDesc_str+"..."

                
            
            appIcon=appIcon[0].attrs['src']
            appName=appName[0].getText()
            appDevs=appDevs[0].text
            appDesc_str=appDesc_str
            appInstall=appInstall[5].text
            appRating=appRating[0].text
            appRatingCount=appRatingCount[0].text



            # response = requests.get(appIcon[0].attrs['src'])

            # file = open("sample_image.png", "wb")
            # file.write(response.content)
            # file.close()

        print(appIcon)
        print(appName)
        print(appDevs)
        print(appDesc_str)
        print(appInstall)
        print(appRating)
        print(appRatingCount)


        return render(request, 'summary.html',{'appIcon':appIcon, 'appName':appName,'appDevs':appDevs, 'appDesc_str':appDesc_str,'appInstall':appInstall,'appRating':appRating,'appRatingCount':appRatingCount})
        # return HttpResponse({appIcon, appName, appDevs, appDesc_str, appInstall, appRating, appRatingCount})
        # return HttpResponse(appName)
    except:
        return HttpResponse("<h1>Error! Please enter valid Inputs</h1>")