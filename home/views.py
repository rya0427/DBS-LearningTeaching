from django.shortcuts import redirect, render
from django.http import HttpResponse, response
import MySQLdb
from django.db import connection

from .forms import loginForm,dangkyForm
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users

current_term = '201'

# Create your views here.

def home(request):
    return render(request, 'home/index.html')

class loginUser(View):
    def get(self,request):
        lF =  loginForm
        return render(request, 'home/login.html',{'lF':lF})

    def post(self,request):
        username  = request.POST['username']
        pasword = request.POST['password']

        user = authenticate(request, username=username, password=pasword)
        if user is not None:
            login(request, user)
            return redirect('home:total')
        else:
            lF =  loginForm
            return render(request, 'home/login.html',{'lF':lF})

@login_required
@allowed_users(['sinhvien','giangvien','pdt','khoa'])
def total(request):
    return render(request, 'home/totalPage.html')

@login_required
@allowed_users(['sinhvien','giangvien','pdt','khoa'])
def logoutUser(request):
    logout(request)
    return render(request, 'home/index.html')

@login_required
@allowed_users(['sinhvien','khoa','pdt'])
def dkmh(request):
    db = MySQLdb.connect(user='root', db='courses_enrollment', passwd='', host='localhost')
    cursor = db.cursor()
    op = 'SELECT hoc_ky, l.ma_mon_hoc,ten_mon_hoc,so_tin_chi FROM lop l join mon_hoc m on l.ma_mon_hoc = m.ma_mon_hoc where hoc_ky ='+ current_term +' group by l.ma_mon_hoc'
    cursor.execute(op)
    columns = [col[0] for col in cursor.description]
    classes = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor1 = db.cursor()
    op = 'SELECT d.MSSV, l.ma_lop_hoc, hoc_ky, sum(so_tin_chi) Tong_tin_chi FROM dang_ky d join sinh_vien s on d.MSSV = s.MSSV join lop l on d.id_lop = l.idlop join mon_hoc m on m.ma_mon_hoc = l.ma_mon_hoc where hoc_ky = '+str(current_term)+' GROUP BY MSSV'   
    cursor1.execute(op)
    columns = [col[0] for col in cursor1.description]
    dangky = [dict(zip(columns, row)) for row in cursor1.fetchall()]

    cursor2 = db.cursor()
    op = 'SELECT s.MSSV,s.Username,ho, ten FROM sinh_vien s join nguoi_dung n on s.Username = n.username'   
    cursor2.execute(op)
    columns = [col[0] for col in cursor2.description]
    lsvUsername = [dict(zip(columns, row)) for row in cursor2.fetchall()]

    db.close()
    return render(request, 'home/dkmh.html',{'current_term':current_term,'classes': classes, 'dangky': dangky,'lsinhvien':lsvUsername})

@login_required
@allowed_users(['sinhvien'])
def dangky(request, mamh):
    db = MySQLdb.connect(user='root', db='courses_enrollment', passwd='', host='localhost')
    cursor = db.cursor()
    op = 'SELECT hoc_ky, l.ma_mon_hoc, ten_mon_hoc, so_tin_chi FROM lop l join mon_hoc m on l.ma_mon_hoc = m.ma_mon_hoc where m.ma_mon_hoc = \''+ mamh + '\''
    cursor.execute(op)
    columns = [col[0] for col in cursor.description]
    courses = [dict(zip(columns, row)) for row in cursor.fetchall()][0]


    cursor0 = db.cursor()
    op = 'SELECT idlop, ma_lop_hoc,hoc_ky, l.ma_mon_hoc,ten_mon_hoc,so_tin_chi FROM lop l join mon_hoc m on l.ma_mon_hoc = m.ma_mon_hoc where hoc_ky ='+ current_term + ' and m.ma_mon_hoc=\''+ mamh + '\''
    cursor0.execute(op)
    columns = [col[0] for col in cursor0.description]
    classes = [dict(zip(columns, row)) for row in cursor0.fetchall()]

    cursor1 = db.cursor()
    op = 'SELECT d.MSSV, l.ma_lop_hoc,l.ma_mon_hoc, hoc_ky, sum(so_tin_chi) Tong_tin_chi FROM dang_ky d join sinh_vien s on d.MSSV = s.MSSV join lop l on d.id_lop = l.idlop join mon_hoc m on m.ma_mon_hoc = l.ma_mon_hoc where hoc_ky = '+current_term+' GROUP BY MSSV'   
    cursor1.execute(op)
    columns = [col[0] for col in cursor1.description]
    dangky = [dict(zip(columns, row)) for row in cursor1.fetchall()]

    cursor2 = db.cursor()
    op = 'SELECT s.MSSV,s.Username,ho, ten FROM sinh_vien s join nguoi_dung n on s.Username = n.username'   
    cursor2.execute(op)
    columns = [col[0] for col in cursor2.description]
    lsvUsername = [dict(zip(columns, row)) for row in cursor2.fetchall()]
    
    
    if request.method == 'POST':
        idlop = request.POST.get('malop','')
        
        cursor3 = db.cursor()
        us = request.user.username
        op = 'SELECT s.MSSV FROM sinh_vien s join nguoi_dung n on s.Username = n.username where s.username= \''+ str(us)+ '\''
        cursor3.execute(op)
        sv = cursor3.fetchall()
        for x in sv: s = x
        for x in s: ss = x

        tong_tin_chi = 0
        
        for y in dangky:
            if y["MSSV"] == ss:
                tong_tin_chi = y["Tong_tin_chi"]

        dadangky=False
        cursor5 = db.cursor()
        cursor5.execute('SELECT d.MSSV, l.ma_mon_hoc, hoc_ky FROM dang_ky d join lop l on d.id_lop = l.idlop where hoc_ky = '+current_term+' '   )
        columns = [col[0] for col in cursor5.description]
        dsdangky = [dict(zip(columns, row)) for row in cursor5.fetchall()]
        for y in dsdangky:
            if y["MSSV"] == ss and y["ma_mon_hoc"] == mamh and y["hoc_ky"] == int(current_term):
                dadangky = True

        cursor4 = db.cursor()
        cursor4.execute('SELECT count(*) siso FROM dang_ky where id_lop='+str(idlop)+' group by id_lop')
        siso = cursor4.fetchall()
        xsiso = 0
        for x in siso: 
            for y in x: xsiso = y
        if xsiso == None: xsiso = 0
        if xsiso < 60 and tong_tin_chi + courses["so_tin_chi"] <= 18 and not dadangky:
            with connection.cursor() as c:
                c.execute('INSERT INTO dang_ky value('+str(ss)+',' +str(idlop) + ')')
            return redirect('/dkmh/')
        else:
            return redirect('/dkerror/')
    context = {
        'courses': courses,
        'lsinhvien': lsvUsername,
        'dangky': dangky,
        'classes':classes,
    }
    return render(request,'home/dkmonhoc.html',context)

@login_required
@allowed_users(['sinhvien'])
def dkerror(request):
    return render(request,'home/dk_error.html')
