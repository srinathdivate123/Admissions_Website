from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import pytesseract
from . models import UserData
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import PIL
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras import Sequential
from keras.layers import Dense
from django.shortcuts import render, redirect
import os
import pdb
from django.http import JsonResponse
tesseract_cmd = r'C:\Program Files\Tesseract-OCR'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from django.http import JsonResponse
import pickle

def CollegePredictorView(request):
    if request.method == 'GET':
        return render(request, 'dashboard/CollegePredictor.html', )
    if request.method == "POST":
        gre = request.POST['gre']
        toefl = request.POST['toefl']
        u_rating = request.POST['u_rating']
        sop = request.POST['sop']
        lor = request.POST['lor']
        cgpa = request.POST['cgpa']
        r_exp = request.POST['r_exp']

        df = pd.read_csv(os.path.join('dashboard/Admission_Predict.csv'))
        df.drop(columns=['Serial No.'], inplace=True)
        X = df.iloc[:, 0:-1]
        y = df.iloc[:, -1]
        X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, random_state=1)
        scaler = MinMaxScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        global r2_result
        global model
        global prediction
        model = Sequential()
        model.add(Dense(7, activation='relu', input_dim=7))
        model.add(Dense(7, activation='relu'))
        model.add(Dense(7, activation='relu'))
        model.add(Dense(1, activation='linear'))
        model.compile(loss='mean_squared_error', optimizer='Adam')
        history = model.fit(X_train_scaled, Y_train, epochs=100, validation_split=0.2)
        y_pred = model.predict(X_test_scaled)
        r2_result = r2_score(Y_test, y_pred)

        # Dumping in pickle
        pickle.dump(model,open('model.pkl','wb'))

        input_data = (float(gre), float(toefl), float(u_rating), float(sop), float(lor), float(cgpa), float(r_exp))
        input_data_as_numpy_array = np.asarray(input_data)
        input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
        prediction = model.predict(input_data_reshaped)
        prediction = str(prediction)
        prediction = prediction[2:len(prediction)-2]
        index = prediction.find('.')
        prediction = prediction[:index]
        r = str(r2_result)[2:]
        var = int(r)/100000000000000
        r = str(var)
        print(r)
        res = {'prediction':prediction, 'r2_result': r, 'gre':gre,'toefl':toefl,'u_rating':u_rating,'sop':sop,'lor':lor,'cgpa':cgpa,'r_exp':r_exp}
        return render(request, 'dashboard/predictorresult.html',res)



def chartView(request):
    finalrep = {'answer': 0, 'nochance':0}
    finalrep['answer'] = prediction
    intpre = 100.00 - float(prediction)
    finalrep['nochance'] = intpre
    return JsonResponse({'prediction':finalrep}, safe=False)

def CollegeRecommenderView(request):
    if request.method == 'GET':
        return render(request, 'dashboard/collegerecommender.html')
    if request.method == 'POST':
        greV = request.POST['GREV']
        greQ = request.POST['GREQ']
        greW = request.POST['GREW']
        cgpa = request.POST['CGPA']
        data = pd.read_csv(os.path.join('dashboard/Processed_data.csv'))
        data.drop(data.columns[data.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
        testSet = [[greV, greQ, greW, cgpa]]
        test = pd.DataFrame(testSet)
        k = 10
        distances = {}
        length = test.shape[1]
        for x in range(len(data)):
            dist = 0
            for y in range(length):
                dist += np.square(float(test[y]) - data.iloc[x][y])
            distance = np.sqrt(dist)
            distances[x] = distance
        sorted_distances = sorted(distances.items(), key=lambda x: x[1])
        neighbors_list = []
        for x in range(k):
            neighbors_list.append(sorted_distances[x][0])
        duplicateNeighbors = {}
        for x in range(len(neighbors_list)):
            responses = data.iloc[neighbors_list[x]][-1]
            if responses in duplicateNeighbors:
                duplicateNeighbors[responses] += 1
            else:
                duplicateNeighbors[responses] = 1
        sortedNeighbors = sorted(duplicateNeighbors.items(), key=lambda x: x[1], reverse=True)
        result = sortedNeighbors
        list1 = []
        list2 = []
        for i in result:
            list1.append(i[0])
        for i in result:
            list2.append(i[1])
        for i in list1:
            print(i)
        try:
            res = {'result1': list1[0]}
        except Exception as s:
            pass
        try:
            res = {'result1': list1[0], 'result2': list1[1]}
        except Exception as s:
            pass
        try:
            res = {'result1': list1[0], 'result2': list1[1], 'result3': list1[2]}
        except Exception as s:
            pass
        try:
            res = {'result1': list1[0], 'result2': list1[1], 'result3': list1[2], 'result4': list1[3]}
        except Exception as s:
            pass
        try:
            res = {'result1': list1[0], 'result2': list1[1], 'result3': list1[2], 'result4': list1[3], 'result5': list1[4]}
        except Exception as s:
            pass
        try:
            res = {'result1': list1[0], 'result2': list1[1], 'result3': list1[2], 'result4': list1[3], 'result5': list1[4],
               'result6': list1[5]}
        except Exception as s:
            pass
        try:
            res = {'result1': list1[0], 'result2': list1[1], 'result3': list1[2], 'result4': list1[3], 'result5': list1[4],
               'result6': list1[5], 'result7': list1[6]}
        except Exception as s:
            pass
        try:
            res = {'result1': list1[0], 'result2': list1[1], 'result3': list1[2], 'result4': list1[3], 'result5': list1[4],
               'result6': list1[5], 'result7': list1[6], 'result8': list1[7]}
        except Exception as s:
            pass
        try:
            res = {'result1': list1[0], 'result2': list1[1], 'result3': list1[2], 'result4': list1[3], 'result5': list1[4],
               'result6': list1[5], 'result7': list1[6], 'result8': list1[7], 'result9': list1[8]}
        except Exception as s:
            pass
        try:
            res = {'result1': list1[0], 'result2': list1[1], 'result3': list1[2], 'result4': list1[3], 'result5': list1[4],
               'result6': list1[5], 'result7': list1[6], 'result8': list1[7], 'result9': list1[8], 'result10': list1[9]}
        except Exception as s:
            pass
        return render(request, 'dashboard/recommenderresult.html', res)






def DashboardView(request):
    if request.method == 'GET':
        if UserData.objects.filter(owner=request.user).exists():
            user = UserData.objects.get(owner=request.user)
            user.email = request.user.email
        else:
            user = UserData.objects.create(owner=request.user)
            user.email = request.user.email
        user.save()
        return render(request, 'dashboard/dashboard.html', {'user':user})
        #data = pd.read_csv(os.path.join('dashboard/Processed_data.csv'))


def ReportCardUploadView(request):
    if request.method == "POST":
        fs = FileSystemStorage()
        image = request.FILES['image']
        user = UserData.objects.get(owner=request.user)
        user.reportcardcount = user.reportcardcount + 1
        image_name = 'r'+request.user.username + \
            str(user.reportcardcount)+'.jpeg'
        filename = fs.save(image_name, image)
        url = fs.url(filename)
        user.reportcard = url
        user.save()
        messages.success(
            request, 'Your report card was uploaded successfully!')
        return redirect('collegepredictor')

def ApplicationView(request):
    if request.method == "GET":
        if UserData.objects.filter(owner=request.user).exists():
            user = UserData.objects.get(owner=request.user)
            user.email = request.user.email
        else:
            user = UserData.objects.create(owner=request.user)
            user.email = request.user.email
        user.save()
        if user.markscard:
            membershipRadios = user.radio
            image_path = 'D:\\3rd_SEMESTER\\EDI\\Admissions_Website' + user.markscard
            try:
                result = pytesseract.image_to_string(PIL.Image.open(image_path))
            except Exception as a:
                messages.error(
                    request, 'We couldn\'t digitally process the marks card you uploaded. Please upload it in jpg/jpeg format only.')
                return render(request, 'dashboard/Application.html')
            first_name = ''
            last_name = ''
            middle_name = ''
            print(result)
            if membershipRadios == 'ICSE':
                n_name = result.find('Name')
                c = result[n_name+5:].find(' ')
                first_name = result[n_name+5:n_name+5+c]
                d = result[n_name+6+c:].find(' ')
                middle_name = result[n_name+6+c:n_name+6+d+c]
                e = result[n_name+7+d+c:].find(' ')
                last_name = result[n_name+7+d+c:n_name+4+d+c+e]

                f1 = result.find('Shri')
                f2 = result[f1+5:].find(' ')
                f3 = result[f1+5+f2+1:].find(' ')
                f4 = result[f1+5+f2+f3+1:].find(' ')
                father_name = result[f1+5:f1+5+f2+f3+f4+2]
                print('f-'+father_name+'-')
                m1 = result.find('Smt')
                m2 = result[m1+4:].find(' ')
                mother_name = result[m1+4:m1+4+m2]
                u = result.find('Unique')
                uid = result[u+9:u+11+7]
                b1 = result.find('res)')
                birth_date = result[b1+5:b1+5+10]
                print('b-'+birth_date+'-b')
            universities = User.objects.filter(is_staff=True)
            res = { 'user':user, 'first_name': first_name, 'middle_name': middle_name,
                   'last_name': last_name, 'father_name':father_name, 'mother_name':mother_name, 'uid': uid, 'birth_date':birth_date, 'universities': universities}
            return render(request, 'dashboard/Application.html', res)
        universities = User.objects.filter(is_staff=True)
        return render(request, 'dashboard/Application.html', { 'user':user, 'universities': universities})
    if request.method == "POST":
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        father_name = request.POST['father_name']
        mother_name = request.POST['mother_name']
        roll_no = request.POST['roll_no']
        birth_date = request.POST['birth_date']
        mob_no = request.POST['mob_no']
        course = request.POST['course']
        if len(str(mob_no)) <10:
            messages.error(request, 'Enter mobile number having 10 digits!')
            return redirect ('application')
        data = UserData.objects.get(owner=request.user)
        data.first_name = first_name
        data.middle_name = middle_name
        data.last_name = last_name
        data.father_name = father_name
        data.mother_name = mother_name
        data.roll_no = roll_no
        data.birth_date = birth_date
        data.mob_no = mob_no
        data.course = course
        data.submitted = True
        data.save()
        messages.success(request, 'Your application was submitted successfully!')
        return redirect('application')

def MarksCardUploadView(request):
    if request.method == "POST":
        fs = FileSystemStorage()
        image = request.FILES['image']
        membershipRadios = request.POST['membershipRadios']
        user = UserData.objects.get(owner=request.user)
        user.count = user.count + 1
        user.radio = membershipRadios
        image_name = request.user.username+str(user.count)+'.jpeg'
        filename = fs.save(image_name, image)
        url = fs.url(filename)
        user.markscard = url
        user.save()
        messages.success(request, 'Your marks card was uploaded successfully!')
        return redirect('application')

def ProfileView(request):
    if request.method == 'GET':
        username = request.user.username
        email = request.user.email
        return render(request, 'dashboard/profile.html', {'username': username, 'email': email})
    if request.method == 'POST':
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1 != pass2:
            messages.error(request, 'The passwords don\'t match!')
            return redirect('profile')
        user = User.objects.get(username=request.user.username)
        user.set_password(pass1)
        user.save()
        messages.success(
            request, 'Password changed successfully! Please login again for security reasons!')
        return redirect('login')