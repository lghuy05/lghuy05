import cv2 #thư viện xử lý hình ảnh cho computer vision(opencv)
import pickle #thư viện dùng để chuyển đổi đối tượng sang binary hoặc ngược lại
import numpy as num #thư viện toán học sử dụng để làm việc với ma trận và mảng(arrays)
import os #module cho phép thao tác với tệp và thư mục
#xác định đối tượng quay video, mở camera
video=cv2.VideoCapture(0) 
#Khởi tạo phát hiện khuôn mặt cách sử dụng hàm OpenCV CascadeClassifier() bằng cách chuyển XML thành đối số
facedetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
#tạo danh sách dữ liệu khuôn mặt
faces_data=[] 

i=0
#nhập tên đối tượng
name=input("Nhap ten theo cu phap'Luong Gia Huy_11.1': ") 
#khởi tạo vòng lặp while chạy vô hạn
while True: 
    #Khởi tạo phát hiện khuôn mặt cách sử dụng hàm OpenCV CascadeClassifier() bằng cách chuyển XML thành đối số
    ret,frame=video.read() 
    #chuyển đổi khung thành thang độ xám
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #sử dụng hàm detector để phân loại khuôn mặt, trả về tọa độ (x,y,w,h) của khuôn mặt
    cv2.putText(frame,"Du lieu can 100 anh", (50,50),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
    faces=facedetect.detectMultiScale(gray, 1.3 ,5) 
    #sử dụng vòng lặp for cho tất cả khuôn mặt được phát hiện 
    for (x,y,w,h) in faces: 
        #crop_img là ảnh khuôn mặt được cắt ra từ frame
        crop_img=frame[y:y+h, x:x+w, :] 
        #thay đổi kích thước ảnh khuôn mặt theo tỉ lệ x=50,y=50
        resized_img=cv2.resize(crop_img, (50,50)) 
        #nếu danh sách dữ liệu khuôn mặt nhỏ hơn 100 và i chia hết cho 10 
        if len(faces_data)<=100 and i%10==0:
            #chèn ảnh khuôn mặt đã thay đổi kích thước vào danh sách dữ liệu khuôn mặt 
            faces_data.append(resized_img)
        #cộng 1 cho i    
        i=i+1
        #hiện số ảnh đã chụp vào danh sách dữ liệu khuôn mặt
        cv2.putText(frame,str(len(faces_data)), (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        #đặt hộp giới hạn xung quanh khuôn mặt
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1) 
    #hiển thị khung kết quả    
    cv2.imshow("Frame",frame)
    #bấm 'q' để thoát hoặc dữ liệu khuôn mặt của đối tượng bằng 100 sẽ tự động thoát
    k=cv2.waitKey(1)
    if k==ord('q') or len(faces_data)==100: 
        break
#Giải phóng đối tượng quay video    
video.release()
cv2.destroyAllWindows()

#chuyển đổi danh sách dữ liệu khuôn mặt từ list thành numpy.array
faces_data=num.asarray(faces_data)
#chuyển danh sách dữ liệu từ mảng 1 chiều thành 2 chiều
faces_data=faces_data.reshape(100, -1)

#nếu names.pkl không có trong danh sách chứa tên trong thư mục 'data'
if 'names.pkl' not in os.listdir('data/'):
    #names bằng string name nhân 100
    names=[name]*100
    #mở file names.pkl trong thư mục data
    with open('data/names.pkl', 'wb') as f:
        #lưu trữ names vào names.pkl
        pickle.dump(names, f)
#hoặc không
else:
    #mở file name.pkl trong thư mục data, 'rb' cho phép mở file binary
    with open('data/names.pkl', 'rb') as f:
        #names sẽ được truy xuất từ names.pkl
        names=pickle.load(f)
    #names bằng chính nó công thêm cho string name nhân 100
    names=names+[name]*100
    #mở file names.pkl trong thư mục data, 'wb' chỉ ra file được mở để ghi dưới dạng binary
    with open('data/names.pkl', 'wb') as f:
        #lưu trữ names vào name.pkl
        pickle.dump(names, f)
#nếu faces_data.pkl không có trong danh sách chứa tên của thư mục data
if 'faces_data.pkl' not in os.listdir('data/'):
    #mở file faces_data.pkl trong thư mục data
    with open('data/faces_data.pkl', 'wb') as f:
        #lưu trữ faces_data vào face_data.pkl
        pickle.dump(faces_data, f)
#hoặc không
else:
    #mở faces_data.pkl trong thư mục data
    with open('data/faces_data.pkl', 'rb') as f:
        #faces bằng truy xuất faces_data.pkl
        faces=pickle.load(f)
    #chèn faces_data vào cuối faces, dữ liệu được làm phẳng do trục không được cho
    faces=num.append(faces, faces_data, axis=0)
    #mở faces_data.pkl trong thư mục data
    with open('data/faces_data.pkl', 'wb') as f:
        #lưu trữ faces vào faces_data.pkl
        pickle.dump(faces, f)