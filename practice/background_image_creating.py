#
# import tkinter
# from PIL import Image, ImageTk
#
# root = tkinter.Tk()
# root.title("My Image")
# root.geometry("300x168")
#
# # Use Pillow to load the image
# image_path = "/Users/khizar/Documents/images.jpeg"
# img = Image.open(image_path)
# # # Convert the PIL image to a format Tkinter can use
#
# image = ImageTk.PhotoImage(img)
#
# # # Create a Label widget to display the image
# bg_path = tkinter.Label(root, image=image)
# bg_path.place(relheight=1, relwidth=1)
#
#
# bg_text = tkinter.Label(root, text="Welcome to Page", font=('Georgia', 24))
# bg_text.pack()
#
# # # Run the Tkinter event loop
# root.mainloop()


# root = tkinter.Tk()
# root.title("My Image")
# root.geometry("960x960")
#
# # Use Pillow to load the image
# image_path = "/Users/khizar/Downloads/car_image.png"
# img = Image.open(image_path)
# # # Convert the PIL image to a format Tkinter can use
#
# image = ImageTk.PhotoImage(img)
#
# # # Create a Label widget to display the image
# bg_path = tkinter.Label(root, image=image)
# bg_path.place(relheight=1, relwidth=1)
#
#
# bg_text = tkinter.Label(root, text="Welcome to Page", font=('Georgia', 24))
# bg_text.pack()
#
# # # Run the Tkinter event loop
# root.mainloop()

from PIL import Image
img = Image.open('/Users/khizar/Documents/ggj.PNG')  # Load the image

# Example of resizing the image (optional)
# img = img.resize((800, 600))


# Display the image
img.show()

import os

file_path = '/Users/khizar/Documents/ggj.PNG'
if os.path.exists(file_path):
    print("File found")
else:
    print("File not found")
