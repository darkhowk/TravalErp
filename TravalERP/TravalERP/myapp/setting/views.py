from django.shortcuts import render
from django.views import generic
# Create your views here.

class firstIndex(generic.ListView):
    def __init__(self):
        self.title_nm       = "설정에 오신것을 환영합니다. "
        self.ogImgUrl       = ""
        self.descript       = ""
        self.template_name  = "index.html"

    def get(self, request, *args, **kwargs):
        self.content = {"descript":self.descript,
                        "title_nm":self.title_nm,
                        "ogImgUrl":self.ogImgUrl,                                               
                        "dataList":""}

        return render(request, self.template_name, self.content)