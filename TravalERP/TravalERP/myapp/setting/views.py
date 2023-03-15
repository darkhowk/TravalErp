import math
from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from django.core.paginator import Paginator

import datetime

from ..common.common_models import Menu
from .models import Agent, Manager

# Create your views here.

#################################################
# INDEX
#################################################
class index(generic.ListView):
   def __init__(self):
        self.title_nm = "TON TOUR"
        self.ogImgUrl = ""
        self.descript = "TON TOUR 페이지입니다"
        self.template_name = "index.html"
        self.topMenu = Menu.objects.filter(menu_type="TOP")
        self.leftMenu = Menu.objects.filter(menu_type="LEFT")
      
   def get(self, request, *args, **kwargs):
      self.content = {
                        "descript" : self.descript,
                        "title_nm" : self.title_nm,
                        "ogImgUrl" : self.ogImgUrl,
                        "topMenu"  : self.topMenu,
                        "leftMenu"  : self.leftMenu
                     }

      return render(request, self.template_name, self.content)


#################################################
# SETTING
#################################################
class settingIndex(generic.ListView):
   def __init__(self):
        self.title_nm = "설정"
        self.ogImgUrl = ""
        self.descript = "설정 페이지입니다"
        self.template_name = "setting/index.html"
        self.topMenu = Menu.objects.filter(menu_type="TOP")
        self.leftMenu = Menu.objects.filter(menu_type="LEFT")
      
   def get(self, request, *args, **kwargs):
      self.content = {
                        "descript" : self.descript,
                        "title_nm" : self.title_nm,
                        "ogImgUrl" : self.ogImgUrl,
                        "topMenu"  : self.topMenu,
                        "leftMenu"  : self.leftMenu
                     }

      return render(request, self.template_name, self.content)


#################################################
# MENU
#################################################
class settingMenu(generic.ListView):
   def __init__(self):
      self.title_nm = "메뉴관리"
      self.ogImgUrl = ""
      self.descript = "메뉴관리 페이지입니다"
      self.template_name = "setting/menu.html"
      self.topMenu = Menu.objects.filter(menu_type="TOP")
      self.leftMenu = Menu.objects.filter(menu_type="LEFT")

   def get(self, request, *args, **kwargs):
      ## 페이지에 뿌려질 데이터 
      # 페이지당 보여줄 개수
      self.per_page = int(request.GET.get('perPage', 5))

      # 현재 페이지
      self.current_page = int(request.GET.get('paging', 1))

      # 그려질 페이지 목록
      self.menus = Menu.objects.all()[self.per_page * (self.current_page - 1):self.per_page * self.current_page]

      # 페이지 수
      num_pages = math.ceil(Menu.objects.count() / self.per_page)

      # 페이지 번호 목록
      self.pages = range(1, num_pages + 1)

      # 총 갯수
      # 현재 페이지에 그려지는 항목 범위

      ## 데이터들을 담는다
      self.content = {
                        "descript" : self.descript,
                        "title_nm" : self.title_nm,
                        "ogImgUrl" : self.ogImgUrl,
                        "topMenu"  : self.topMenu,
                        "leftMenu"  : self.leftMenu,
                        "menus" : self.menus,
                        'pages': self.pages,
                        'current_page': int(self.current_page), 
                        'per_page': int(self.per_page),
                     }

      return render(request, self.template_name, self.content)
      

class menuAdd(generic.ListView):
   def __init__(self):
        self.title_nm = "메뉴추가"
        self.ogImgUrl = ""
        self.descript = "메뉴추가 페이지입니다"
        self.template_name = "setting/menuAdd.html"
        self.topMenu = Menu.objects.filter(menu_type="TOP")
        self.leftMenu = Menu.objects.filter(menu_type="LEFT")
      
   def get(self, request, *args, **kwargs):

      if 'pageType' in request.GET:
         pageType = request.GET.get('pageType', None)
         self.perPage = request.GET.get('perPage', None)
         self.paging = request.GET.get('paging', None)
         if pageType == 'I':
            self.content = {
                           "descript" : self.descript,
                           "title_nm" : self.title_nm,
                           "ogImgUrl" : self.ogImgUrl,
                           "topMenu"  : self.topMenu,
                           "leftMenu" : self.leftMenu,
                           "pageType" : pageType,
                           "perPage"  : self.perPage,
                           "paging"   : self.paging
                        }
         elif pageType == 'U':
            id = request.GET.get('id', None)
            self.contentMenu = Menu.objects.filter(menu=id)
            self.content = {
                           "descript"    : self.descript,
                           "title_nm"    : self.title_nm,
                           "ogImgUrl"    : self.ogImgUrl,
                           "topMenu"     : self.topMenu,
                           "leftMenu"    : self.leftMenu,
                           "contentMenu" : self.contentMenu,
                           "pageType"    : pageType,
                           "perPage"     : self.perPage,
                           "paging"      : self.paging
                        }
         

         return render(request, self.template_name, self.content)
      else :
         return render('', '/error', '')

def menuInsert(request):
   now = datetime.datetime.now()

   menu = request.POST.get('menu')
   menu_name = request.POST.get('menu_name')
   upper_menu = request.POST.get('upper_menu')
   use_yn = request.POST.get('use_yn')
   icon = request.POST.get('icon')
   menu_type = request.POST.get('menu_type')
   link = request.POST.get('link')
   menu = Menu(
        menu=menu
      , menu_name=menu_name
      , upper_menu=upper_menu
      , use_yn=use_yn
      , icon=icon
      , menu_type=menu_type
      , link=link
      , entry_date = now.strftime('%Y-%m-%d %H:%M:%S')
   )
   menu.save()
   return JsonResponse({'result': 'success'})

def menuModify(request):
   now = datetime.datetime.now()

   menu = request.POST.get('menu')
   menuObject = Menu.objects.get(menu=menu)
   menuObject.menu = request.POST.get('menu')
   menuObject.menu_name = request.POST.get('menu_name')
   menuObject.upper_menu = request.POST.get('upper_menu')
   menuObject.use_yn = request.POST.get('use_yn')
   menuObject.icon = request.POST.get('icon')
   menuObject.menu_type = request.POST.get('menu_type')
   menuObject.link = request.POST.get('link')
   menuObject.updat_date = now.strftime('%Y-%m-%d %H:%M:%S')
   menuObject.save()
   return JsonResponse({'result': 'success'})

def menuDelete(request):
   now = datetime.datetime.now()

   menu = request.POST.get('menu')
   menuObject = Menu.objects.get(menu=menu)
   menuObject.use_yn = 'N'
   menuObject.updat_date = now.strftime('%Y-%m-%d %H:%M:%S')
   menuObject.save()

   return JsonResponse({'result': 'success'})

#################################################
# AGENT
#################################################
class agentIndex(generic.ListView):
   def __init__(self):
        self.title_nm = "여행사"
        self.ogImgUrl = ""
        self.descript = "여행사 등록 페이지입니다"
        self.template_name = "setting/agent.html"
        self.topMenu = Menu.objects.filter(menu_type="TOP")
        self.leftMenu = Menu.objects.filter(menu_type="LEFT")
   def get(self, request, *args, **kwargs):
      self.agent_type = request.GET.get('agent_type', None)
      self.agent = Agent.objects.filter(agent_type = self.agent_type)

      #페이지당 숫자
      perPage = request.GET.get('perPage')
      if perPage and perPage.isdigit():
         self.per_page = int(perPage)
      else:
         self.per_page = 5

      # 현재 페이지
      paging = request.GET.get('paging')
      if paging and paging.isdigit():
         self.current_page = int(paging)
      else:
         self.current_page = 1

      # 그려질 페이지 목록
      self.agents = self.agent[self.per_page * (self.current_page - 1):self.per_page * self.current_page]

      # 페이지 수
      num_pages = math.ceil(self.agent.count() / self.per_page)

      # 페이지 번호 목록
      self.pages = range(1, num_pages + 1)

      if self.agent_type == 'A':
         self.title_nm = "여행사"
         self.descript = "여행사 페이지입니다"
      else :
         self.title_nm = "설정>로컬"
         self.descript = "로컬 페이지입니다"
      self.content = {
                        "descript"      : self.descript,
                        "title_nm"      : self.title_nm,
                        "ogImgUrl"      : self.ogImgUrl,
                        "topMenu"       : self.topMenu,
                        "leftMenu"      : self.leftMenu,
                        "agent_type"    : self.agent_type,
                        "agent"         : self.agents,
                        'current_page': int(self.current_page), 
                        'per_page': int(self.per_page),
                        'pages': self.pages,
                     }

      return render(request, self.template_name, self.content)


class agentAdd(generic.ListView):
   def __init__(self):
        self.title_nm = "여행사 추가"
        self.ogImgUrl = ""
        self.descript = "여행사추가 페이지입니다"
        self.template_name = "setting/agentAdd.html"
        self.topMenu = Menu.objects.filter(menu_type="TOP")
        self.leftMenu = Menu.objects.filter(menu_type="LEFT")
      
   def get(self, request, *args, **kwargs):

      if 'pageType' in request.GET:
         pageType = request.GET.get('pageType', None)
         if pageType == 'I':
            agent_type = request.GET.get('agent_type', None)
            if agent_type == 'A':
               self.title_nm = "여행사 추가"
               self.descript = "여행사추가 페이지입니다"
            else :
               self.title_nm = "로컬 추가"
               self.descript = "로컬추가 페이지입니다"

            self.content = {
                           "descript" : self.descript,
                           "title_nm" : self.title_nm,
                           "ogImgUrl" : self.ogImgUrl,
                           "topMenu"  : self.topMenu,
                           "leftMenu" : self.leftMenu,
                           "pageType" : pageType,
                           "agent_type" : agent_type,
                        }
         elif pageType == 'U':
            agent_type = request.GET.get('agent_type', None)
            if agent_type == 'A':
               self.title_nm = "여행사 수정"
               self.descript = "여행사 수정 페이지입니다"
            else :
               self.title_nm = "로컬 수정"
               self.descript = "로컬 수정 페이지입니다"

            id =  request.GET.get('id', None)
            self.agent = Agent.objects.filter(id=id, agent_type = agent_type)
            self.perPage = request.GET.get('perPage', None)
            self.paging = request.GET.get('paging', None)
            self.content = {
                           "descript"    : self.descript,
                           "title_nm"    : self.title_nm,
                           "ogImgUrl"    : self.ogImgUrl,
                           "topMenu"     : self.topMenu,
                           "leftMenu"    : self.leftMenu,
                           "pageType"    : pageType,
                           "perPage"     : self.perPage,
                           "paging"      : self.paging,
                           "agent_type"  : agent_type,
                           "agent"       : self.agent,

                        }
         return render(request, self.template_name, self.content)
      else :
         return render('', '/error', '')

def agentInsert(request):
   now = datetime.datetime.now()

   agent_name = request.POST.get('agent_name')
   agent_tel = request.POST.get('agent_tel')
   agent_type = request.POST.get('agent_type')
   use_yn = request.POST.get('use_yn')
   agent = Agent(
        agent_name=agent_name
      , agent_tel=agent_tel
      , agent_type=agent_type
      , use_yn=use_yn
      , entry_date = now.strftime('%Y-%m-%d %H:%M:%S')
   )
   agent.save()
   return JsonResponse({'result': 'success'})

def agentModify(request):
   now = datetime.datetime.now()

   id = request.POST.get('id')
   agent_type = request.POST.get('agent_type')
   agentObject = Agent.objects.get(id=id, agent_type=agent_type)
   agentObject.agent_name = request.POST.get('agent_name')
   agentObject.agent_tel = request.POST.get('agent_tel')
   agentObject.use_yn = request.POST.get('use_yn')
   agentObject.updat_date = now.strftime('%Y-%m-%d %H:%M:%S')
   agentObject.save()
   return JsonResponse({'result': 'success'})

def agentDelete(request):
   now = datetime.datetime.now()

   id = request.POST.get('id')
   agent_type = request.POST.get('agent_type')
   agentObject = Agent.objects.get(id=id, agent_type=agent_type)
   agentObject.use_yn = 'N'
   agentObject.updat_date = now.strftime('%Y-%m-%d %H:%M:%S')
   agentObject.save()

   return JsonResponse({'result': 'success'})

#################################################
# MANAGER
#################################################
class managerIndex(generic.ListView):
   def __init__(self):
        self.title_nm = "담당자"
        self.ogImgUrl = ""
        self.descript = "담당자 등록 페이지입니다"
        self.template_name = "setting/manager.html"
        self.topMenu = Menu.objects.filter(menu_type="TOP")
        self.leftMenu = Menu.objects.filter(menu_type="LEFT")
   def get(self, request, *args, **kwargs):
      self.type = request.GET.get('type', None)
      self.manager = Manager.objects.filter(type = self.type)

      #페이지당 숫자
      perPage = request.GET.get('perPage')
      if perPage and perPage.isdigit():
         self.per_page = int(perPage)
      else:
         self.per_page = 5

      # 현재 페이지
      paging = request.GET.get('paging')
      if paging and paging.isdigit():
         self.current_page = int(paging)
      else:
         self.current_page = 1

      # 그려질 페이지 목록
      self.managers = self.manager[self.per_page * (self.current_page - 1):self.per_page * self.current_page]

      # 페이지 수
      num_pages = math.ceil(self.manager.count() / self.per_page)

      # 페이지 번호 목록
      self.pages = range(1, num_pages + 1)

      if self.type == 'M':
         self.title_nm = "담당자"
         self.descript = "담당자 페이지입니다"
      else :
         self.title_nm = "로컬 담당자"
         self.descript = "로컬 담당자 페이지입니다"
      self.content = {
                        "descript"      : self.descript,
                        "title_nm"      : self.title_nm,
                        "ogImgUrl"      : self.ogImgUrl,
                        "topMenu"       : self.topMenu,
                        "leftMenu"      : self.leftMenu,
                        "type"          : self.type,
                        "manager"         : self.managers,
                        'current_page': int(self.current_page), 
                        'per_page': int(self.per_page),
                        'pages': self.pages,
                     }

      return render(request, self.template_name, self.content)


class managerAdd(generic.ListView):
   def __init__(self):
        self.title_nm = "담당자 추가"
        self.ogImgUrl = ""
        self.descript = "담당자추가 페이지입니다"
        self.template_name = "setting/managerAdd.html"
        self.topMenu = Menu.objects.filter(menu_type="TOP")
        self.leftMenu = Menu.objects.filter(menu_type="LEFT")
      
   def get(self, request, *args, **kwargs):
      

      if 'pageType' in request.GET:
         pageType = request.GET.get('pageType', None)
         if pageType == 'I':
            type = request.GET.get('type', None)
            if type == 'M':
               self.title_nm = "담당자 추가"
               self.descript = "담당자추가 페이지입니다"
               agent = Agent.objects.filter(agent_type="A", use_yn='Y', )
            else :
               self.title_nm = "로컬 담당자 추가"
               self.descript = "로컬 담당자 추가 페이지입니다"
               agent = Agent.objects.filter(agent_type="L", use_yn='Y', )

            self.content = {
                           "descript" : self.descript,
                           "title_nm" : self.title_nm,
                           "ogImgUrl" : self.ogImgUrl,
                           "topMenu"  : self.topMenu,
                           "leftMenu" : self.leftMenu,
                           "pageType" : pageType,
                           "type" : type,
                           "agent": agent,
                        }
         elif pageType == 'U':
            type = request.GET.get('type', None)
            if type == 'M':
               self.title_nm = "담당자 수정"
               self.descript = "담당자 수정 페이지입니다"
               agent = Agent.objects.filter(agent_type="A", use_yn='Y', )
            else :
               self.title_nm = "로컬 담당자 수정"
               self.descript = "로컬 담당자 수정 페이지입니다"
               agent = Agent.objects.filter(agent_type="L", use_yn='Y', )

            id =  request.GET.get('id', None)
            self.manager = Manager.objects.filter(id=id, type = type)
            self.perPage = request.GET.get('perPage', None)
            self.paging = request.GET.get('paging', None)
            self.content = {
                           "descript"    : self.descript,
                           "title_nm"    : self.title_nm,
                           "ogImgUrl"    : self.ogImgUrl,
                           "topMenu"     : self.topMenu,
                           "leftMenu"    : self.leftMenu,
                           "pageType"    : pageType,
                           "perPage"     : self.perPage,
                           "paging"      : self.paging,
                           "type"        : type,
                           "manager"     : self.manager,
                           "agent": agent,
                        }
         return render(request, self.template_name, self.content)
      else :
         return render('', '/error', '')

def managerInsert(request):
   now = datetime.datetime.now()

   agent_name = request.POST.get('agent_name')
   manager_name = request.POST.get('manager_name')
   manager_tel = request.POST.get('manager_tel')
   type = request.POST.get('type')
   manager_hp = request.POST.get('manager_hp')
   manager_messenger = request.POST.get('manager_messenger')
   manager_email = request.POST.get('manager_email')
   manager_remark = request.POST.get('manager_remark')
   use_yn = request.POST.get('use_yn')
   manager = Manager(
        agent_name=agent_name
      , manager_name=manager_name
      , manager_tel=manager_tel
      , type=type
      , manager_hp=manager_hp
      , manager_messenger=manager_messenger
      , manager_email=manager_email
      , manager_remark=manager_remark
      , use_yn=use_yn
      , entry_date = now.strftime('%Y-%m-%d %H:%M:%S')
   )
   manager.save()
   return JsonResponse({'result': 'success'})

def managerModify(request):
   now = datetime.datetime.now()

   id = request.POST.get('id')
   type = request.POST.get('type')
   managerObject = Manager.objects.get(id=id, type=type)
   managerObject.agent_name = request.POST.get('agent_name')
   managerObject.manager_name = request.POST.get('manager_name')
   managerObject.manager_tel = request.POST.get('manager_tel')
   managerObject.manager_hp = request.POST.get('manager_hp')
   managerObject.manager_messenger = request.POST.get('manager_messenger')
   managerObject.manager_email = request.POST.get('manager_email')
   managerObject.manager_remark = request.POST.get('manager_remark')
   managerObject.use_yn = request.POST.get('use_yn')
   managerObject.updat_date = now.strftime('%Y-%m-%d %H:%M:%S')
   managerObject.save()
   return JsonResponse({'result': 'success'})

def managerDelete(request):
   now = datetime.datetime.now()

   id = request.POST.get('id')
   type = request.POST.get('type')
   managerObject = Manager.objects.get(id=id, type=type)
   managerObject.use_yn = 'N'
   managerObject.updat_date = now.strftime('%Y-%m-%d %H:%M:%S')
   managerObject.save()

   return JsonResponse({'result': 'success'})
