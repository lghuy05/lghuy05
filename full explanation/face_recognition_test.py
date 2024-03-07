#từ sklearn.neighbors nhập KNeighborsClasifier
from sklearn.neighbors import KNeighborsClassifier
import cv2 #thư viện xử lý hình ảnh cho computer vision(opencv)
import pickle #thư viện dùng để chuyển đổi đối tượng sang binary hoặc ngược lại
import numpy as num #thư viện toán học sử dụng để làm việc với ma trận và mảng(arrays)
import os #module cho phép thao tác với tệp và thư mục
import csv #một loại tệp văn bản, mục đích chính trong dự án này để xuất ra file exel nhằm điểm danh
import time #thư viện thời gian 
from datetime import datetime #datetime được kết hợp từ date(ngày) và time(thời gian)
#từ từ win32.client nhập Dispatch
from win32com.client import Dispatch
#định nghĩa funtion tên speak, 'str1' dùng để nối chuỗi vào speak
def speak(str1):
      #phân phối 'SAPI.SpVoice', đây là tính năng chuyển văn bản thành giọng nói đc tích hợp trong Windows
      speak=Dispatch("SAPI.SpVoice")
      #nói string 
      speak.Speak(str1)
#xác định đối tượng quay video, mở camera
video=cv2.VideoCapture(0)
#Khởi tạo phát hiện khuôn mặt cách sử dụng hàm OpenCV CascadeClassifier() bằng cách chuyển XML thành đối số
facedetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#mở name.pkl từ thư mục data, 'rb' cho phép mở file binary
with open('data/names.pkl', 'rb') as f:
        #LABELS là những gì được truy xuất từ name.pkl
        LABELS=pickle.load(f)
#mở faces_data.pkl từ thư mục data, 'rb' cho phép mở file binary
with open('data/faces_data.pkl', 'rb') as f:
        #FACES là những gì được truy xuất từ faces_data.pkl
        FACES=pickle.load(f)
#KNeighborsClassfier tìm kiếm 10 hàng xóm gần nhất
knn=KNeighborsClassifier(n_neighbors=10)
#lắp FACES VÀ LABELS vào knn để lưu trữ cho huấn luyện
knn.fit(FACES, LABELS)
#xuất background.png 
imgBackground=cv2.imread("background.png")
#danh sách điểm danh gồm họ và tên, thời gian
ATTENDANCENAMES= ['HOVATEN','THOIGIAN']
#khởi tạo vòng lặp while chạy vô hạn
while True:
    #Khởi tạo phát hiện khuôn mặt cách sử dụng hàm OpenCV CascadeClassifier() bằng cách chuyển XML thành đối số
    ret,frame=video.read()
    #chuyển đổi khung thành thang độ xám
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #sử dụng hàm detector để phân loại khuôn mặt, trả về tọa độ (x,y,w,h) của khuôn mặt
    faces=facedetect.detectMultiScale(gray, 1.3 ,5)
    #sử dụng vòng lặp for cho tất cả khuôn mặt được phát hiện 
    for (x,y,w,h) in faces:
        #crop_img là ảnh khuôn mặt được cắt ra từ frame
        crop_img=frame[y:y+h, x:x+w, :]
        #thay đổi kích thước ảnh khuôn mặt theo tỉ lệ x=50,y=50
        resized_img=cv2.resize(crop_img, (50,50)).flatten().reshape(1, -1)
        #knn sẽ dự đoán ảnh đã thay đổi kích thước và cho ra output
        output=knn.predict(resized_img)      
        #trả về thời gian
        ts=time.time()
        #lấy thời gian hiện tại và trả về chuỗi biễn diễn giá trị ngày-tháng-năm 
        date=datetime.now().strftime("%d-%m-%Y")
        #lấy thời gian hiện tại và trả về chuỗi biễn diễn giá trị giờ-phút-giây 
        times=datetime.now().strftime("%H:%M:%S")
        #kiểm tra sự tồn tại của file với cú pháp ,Ví dụ: diemdanh_27-07-2023.csv
        ex=os.path.isfile("diemdanh/diemdanh_" + date + ".csv")
        #decor khung khuôn mặt
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
        cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1)
        #hiển thị tên của đối tượng được nhận dạng
        cv2.putText(frame, str(output[0]), (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2) 
        #danh sách string tên được nhận dạng và thời gian       
        attendance=[str(output[0]), str(times)] 
    #vị trí ảnh nền hiển thị như frame
    imgBackground[162:162 + 480, 55:55 +640] = frame
    #hiển thị ảnh nền
    cv2.imshow("Frame",imgBackground)
    #khi bấm 'a'
    k=cv2.waitKey(1)
    if k == ord('a'):
        #máy tính phát âm thanh 'Attendance Taken'
        speak("Attendance Taken..")
        #nếu đã có file với cú pháp ở line 61
        if ex:
                #mở file diemdanh trong thư mục điểm danh dưới dạng csvfile
                with open("diemdanh/diemdanh_" + date + ".csv", "+a") as csvfile: 
                        writer=csv.writer(csvfile)
                        #viết tên và thời gian điểm danh vào file csv
                        writer.writerow(attendance)
                #đóng csvfile
                csvfile.close()
        #hoặc không
        else:
                #mở file diemdanh trong thư mục điểm danh dưới dạng csvfile
                with open("diemdanh/diemdanh_" + date + ".csv", "+a") as csvfile: 
                        writer=csv.writer(csvfile)
                        #viết ATTENDANCENAMES, ATTENDANCENAMES cụ thể là HOVATEN và THOIGIAN từ line 37
                        writer.writerow(ATTENDANCENAMES) 
                        #viết tên và thời gian điểm danh vào file csv
                        writer.writerow(attendance)
                #đóng csvfile        
                csvfile.close()
    #bấm 'q' để thoát            
    if k==ord('q'):     
        break
#Giải phóng đối tượng quay video  
video.release()
cv2.destroyAllWindows()

