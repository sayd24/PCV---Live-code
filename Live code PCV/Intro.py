import cv2
from matplotlib import pyplot as plt

img= cv2.imread("grha_its.jpg")
[h, w, c]= img.shape

imgMerah= img.copy()
imgHijau= img.copy()
imgBiru= img.copy()

for i in range(h):
    for j in range(w):
        imgMerah[i,j,0]= 0
        imgMerah[i,j,1]= 0
        
        imgHijau[i,j,0]= 0
        imgHijau[i,j,2]= 0
        
        imgBiru[i,j,1]= 0
        imgBiru[i,j,2]= 0

cv2.imshow("Image Asli", img)
cv2.imshow("Image Merah", imgMerah)
cv2.imshow("Image Hijau", imgHijau)
cv2.imshow("Image Biru", imgBiru)

cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    cv2.imshow("Video Asli", frame)
    
    frameMerah = frame.copy()
    frameMerah[:,:,0]= 0
    frameMerah[:,:,1]= 0
    cv2.imshow("Video Merah", frameMerah)
    
    frameHijau = frame.copy()
    frameHijau[:,:,0]= 0
    frameHijau[:,:,2]= 0
    cv2.imshow("Video Hijau", frameHijau)
    
    frameBiru = frame.copy()
    frameBiru[:,:,1]= 0
    frameBiru[:,:,2]= 0
    cv2.imshow("Video Biru", frameBiru)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)