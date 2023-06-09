import cv2
from pyzbar.pyzbar import decode
import pyqrcode

cam=cv2.VideoCapture(0)
total=0
cost=0
cam.set(5,640)
cam.set(6,480)
prod_list=[]
prod_dict={}
camera=True
counter=0
flag=None
sub=False


while camera==True:
 #flag=input("Do you want to scan (y/n)?")
 #if flag.lower()=='y':
  if sub==False:
    success,frame=cam.read()
    for i in decode(frame):
        if i.data.decode('utf-8') not in prod_list:
          prod_dict[i.data.decode('utf-8')]=1
          print(i.data.decode('utf-8'))
          prod_list.append(i.data.decode('utf-8'))
        else:
            prod_dict[i.data.decode('utf-8')]=prod_dict[i.data.decode('utf-8')]+1
            prod_list.append(i.data.decode('utf-8'))
  if sub==True:
    success,frame=cam.read()
    for i in decode(frame):
        if i.data.decode('utf-8') not in prod_list or prod_dict[i.data.decode('utf-8')]==0:
          print("No "+i.data.decode('utf-8').split(":")[0] +" to be subracted")
          break
        else:
            prod_dict[i.data.decode('utf-8')]=prod_dict[i.data.decode('utf-8')]-1
            prod_list.append(i.data.decode('utf-8'))
            print(prod_dict)
        #print(prod_dict)
  cv2.imshow("scanner",frame)
  if cv2.waitKey(1)==ord('q'):
     flag=input("Continue shopping press a/ removing items press b/ end shopping press c")
     if flag=='a':
       sub=False
       print("Before prompt: "+ str(prod_dict))
       continue
     elif flag=='b':
       print("Before prompt: "+ str(prod_dict))
       sub=True
       continue
     else:
       break
print(prod_dict)
headercount=0
for key in prod_dict:
  if prod_dict[key]>0:
    cost=int(key.split(":")[1])*prod_dict[key]
    itemlist="Item: "+key.split(":")[0]+ ", Qty: "+str(prod_dict[key])+", Unit price: "+str(key.split(":")[1])+", Cost: "+str(cost)
    print(itemlist)
    total=total+cost
    
if total > 0:
  content="Total amount to be paid is "+str(total)
  print(content)
  amt=pyqrcode.create(total)
  amt.png('payment.png',scale=6)
else:
  print("Cart is empty")
cam.release()