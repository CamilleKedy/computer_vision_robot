import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge() 
command_pub = rospy.Publisher("motor_commands", String)

def is_white(val):
  return val > 100

def plan(left, right):
  command = "STOP"
  if is_white(left) and is_white(right):
    command = "GO"
  if is_white(left) and not is_white(right):
    command = "LEFT"
  if not is_white(left) and is_white(right):
    command = "RIGHT"
  print(left, right, command)

  command_pub.publish(command)

def imgCallback(data):
  cv_image = bridge.imgmsg_to_cv2(data, "bgr8") #dim [800, 800, 3]

  # conversion de l'image en N&B pour ne pas avoir à manipuler 3 valeurs en RGB
  # ici on aura qu'une seule valeur de 0 à 255
  gray_image =  cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
  
  # valeur du niveau de gris des pixels (700, 300) et (700, 500)
  # print(gray_image[700][300], gray_image[700][500])

  plan(gray_image[700][300], gray_image[700][500])

  gray_image = cv2.line(gray_image, (300,700), (500, 700), 0, 5)
  cv2.imshow("Apercu camera", gray_image)
  cv2.waitKey(3)

def main():
  print("Hey Universe!")
  rospy.init_node('my_planner_node')
  img_sub = rospy.Subscriber("/camera/image_raw", Image, imgCallback)
  rospy.spin()

if __name__ == "__main__":
  main()


