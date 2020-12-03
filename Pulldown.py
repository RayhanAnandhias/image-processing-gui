import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter.filedialog as filedialog
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

class PopupWindow(object):
    def __init__(self,master):
        self.top=tk.Toplevel(master)
        self.top.geometry("300x100")
        self.top.title("Enter Kernel size (nxn)")
        self.l=tk.Label(self.top,text="Enter n : ")
        self.l.pack()
        self.e=tk.Entry(self.top)
        self.e.pack()
        self.b=tk.Button(self.top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()

class Pulldown(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.panel = None
        self.parent = parent
        self.file_menu = None
        self.noise_menu = None
        self.mode_menu = None
        self.img_pil_format = None
        self.img_path = None
        self.imgcv = None
        self.title_base = self.parent.title()
        self.initialize_pulldown()


    def initialize_pulldown(self):
        menubar = tk.Menu(self.parent)

        # Adding File Menu and commands
        self.file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Open', command=self.open_image)
        self.file_menu.add_command(label='Save', command=self.save_image, state="disabled")
        self.file_menu.add_command(label='Save As', command=self.save_as_image, state="disabled")
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.exit)

        self.noise_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Noise', menu=self.noise_menu)
        self.noise_menu.add_command(label='Gaussian Noise', command=self.gaussian_noise, state="disabled")
        self.noise_menu.add_command(label='Salt & Pepper Noise', command=self.snp_noise, state="disabled")
        self.noise_menu.add_command(label='Poisson Noise', command=self.poisson_noise, state="disabled")
        self.noise_menu.add_command(label='Speckle Noise', command=self.speckle_noise, state="disabled")

        # Adding mode color,grayscale
        self.mode_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Filter', menu=self.mode_menu)

        self.mode_menu.add_command(label='Original',
                                   command=lambda: self.open_image_bg(img_path=self.img_path),
                                   state="disabled")
        self.mode_menu.add_command(label='Grayscale',
                                   command=lambda: self.open_image_bg(img_path=self.img_path, mode=cv.COLOR_BGR2GRAY),
                                   state="disabled")
        self.mode_menu.add_command(label='2D Convolution', command=self.twoDConvolution, state="disabled")
        self.mode_menu.add_command(label='Averaging', command=self.averaging, state="disabled")
        self.mode_menu.add_command(label='Gaussian Filtering', command=self.gaussian, state="disabled")
        self.mode_menu.add_command(label='Median Filtering', command=self.median, state="disabled")
        self.mode_menu.add_command(label='Bilateral Filtering', command=self.bilateral, state="disabled")
        self.mode_menu.add_command(label='Image Thresholding', command=self.maskImage, state="disabled")
        self.mode_menu.add_command(label='Morphology', command=self.morphology, state="disabled")
        self.mode_menu.add_command(label='Laplacian Filtering', command=self.laplacian, state="disabled")
        self.mode_menu.add_command(label='Conservative Filtering', command=self.conservative, state="disabled")
        self.mode_menu.add_command(label='Canny Edge Detection', command=self.canny_edge_detection, state="disabled")
        self.mode_menu.add_command(label='Sobel Edge Detection', command=self.sobel_edge_detection, state="disabled")

        # display Menu
        self.parent.config(menu=menubar)

    def open_image(self):
        # Load Image Path
        self.img_path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[('image files', ('.png', '.jpg', '.jpeg'))])

        if len(self.img_path) > 0:
            # load the image from disk
            img = cv.imread(self.img_path)
            self.imgcv = img

            # OpenCV represents images in BGR order; however PIL represents
            # images in RGB order, so we need to swap the channels
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

            # convert the images to PIL format...
            img = Image.fromarray(img)
            self.img_pil_format = img

            # ...and then to ImageTk format
            img = ImageTk.PhotoImage(img)

            # change window size
            self.parent.geometry("{width}x{height}".format(width=img.width(), height=img.height()))

            # if the panels are None, initialize them
            if self.panel is None:
                self.panel = tk.Label(image=img)
                self.panel.image = img
            else:
                self.panel.configure(image=img)
                self.panel.image = img

            self.panel.pack()
            self.file_menu.entryconfig("Save As", state="normal")
            self.file_menu.entryconfig("Save", state="normal")
            self.mode_menu.entryconfig("Original", state="normal")
            self.mode_menu.entryconfig("Grayscale", state="normal")
            self.noise_menu.entryconfig("Gaussian Noise", state="normal")
            self.noise_menu.entryconfig("Salt & Pepper Noise", state="normal")
            self.noise_menu.entryconfig("Poisson Noise", state="normal")
            self.noise_menu.entryconfig("Speckle Noise", state="normal")
            self.mode_menu.entryconfig("2D Convolution", state="normal")
            self.mode_menu.entryconfig("Averaging", state="normal")
            self.mode_menu.entryconfig("Gaussian Filtering", state="normal")
            self.mode_menu.entryconfig("Median Filtering", state="normal")
            self.mode_menu.entryconfig("Bilateral Filtering", state="normal")
            self.mode_menu.entryconfig("Image Thresholding", state="normal")
            self.mode_menu.entryconfig("Morphology", state="normal")
            self.mode_menu.entryconfig("Laplacian Filtering", state="normal")
            self.mode_menu.entryconfig("Conservative Filtering", state="normal")
            self.mode_menu.entryconfig("Canny Edge Detection", state="normal")
            self.mode_menu.entryconfig("Sobel Edge Detection", state="normal")

            self.parent.title(self.title_base + " - " + self.img_path)

    def open_image_bg(self, img_path, mode=cv.COLOR_BGR2RGB):
        # load the image from disk
        img = cv.imread(img_path)
        self.imgcv = img

        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        img = cv.cvtColor(img, mode)

        # convert the images to PIL format...
        img_cv_pil = Image.fromarray(img)
        self.img_pil_format = img_cv_pil

        # ...and then to ImageTk format
        img_cv_pil = ImageTk.PhotoImage(img_cv_pil)

        # change window size
        self.parent.geometry("{width}x{height}".format(width=img_cv_pil.width(), height=img_cv_pil.height()))

        self.panel.configure(image=img_cv_pil)
        self.panel.image = img_cv_pil
        self.panel.pack()
        self.parent.title(self.title_base + " - " + self.img_path)

        if mode == cv.COLOR_BGR2GRAY:
            plt.subplot(121), plt.imshow(cv.cvtColor(self.imgcv, cv.COLOR_BGR2RGB)), plt.title('Original')
            plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(img, cmap="gray"), plt.title('Grayscale')
            plt.xticks([]), plt.yticks([])
            plt.show()

    def save_image(self):
        if self.panel is not None:
            self.img_pil_format.save(self.img_path)
            messagebox.showinfo("showinfo", "Image Saved")
        else:
            return

    def save_as_image(self):
        if self.panel is not None:
            filetypes = [('PNG', '*.png'), ('JPG', '*.jpg'), ('JPEG', '*.jpeg')]
            fname = filedialog.asksaveasfilename(
                title="Save As Image",
                filetypes=filetypes,
                defaultextension=filetypes)
            if not fname:
                return

            self.img_pil_format.save(fname)
            self.img_path = fname
            self.open_image_bg(img_path=self.img_path)
        else:
            return

    def show_to_gui(self, dst):
        # convert the images to PIL format...
        img_cv_pil = Image.fromarray(dst)
        self.img_pil_format = img_cv_pil

        # ...and then to ImageTk format
        img_cv_pil = ImageTk.PhotoImage(img_cv_pil)

        # change window size
        self.parent.geometry("{width}x{height}".format(width=img_cv_pil.width(), height=img_cv_pil.height()))

        self.panel.configure(image=img_cv_pil)
        self.panel.image = img_cv_pil
        self.panel.pack()
        self.parent.title(self.title_base + " - " + self.img_path)

    def plot_to_matplotlib(self, src, dst, mode, color=1):
        if color == 2:
            plt.subplot(121), plt.imshow(src, cmap="gray"), plt.title('Original')
            plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(dst, cmap="gray"), plt.title(mode)
            plt.xticks([]), plt.yticks([])
            plt.show()
        elif color == 1:
            plt.subplot(121), plt.imshow(src), plt.title('Original')
            plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(dst), plt.title(mode)
            plt.xticks([]), plt.yticks([])
            plt.show()
        elif color == 3:
            plt.subplot(121), plt.imshow(src), plt.title('Original')
            plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(dst, cmap="gray"), plt.title(mode)
            plt.xticks([]), plt.yticks([])
            plt.show()

    def printtext(self):
        global e
        string = e.get()
        print(string)

    def twoDConvolution(self):
        img_cv = self.imgcv
        img_cv = cv.cvtColor(img_cv, cv.COLOR_BGR2RGB)
        kernel = np.ones((5, 5), np.float32) / 25
        dst = cv.filter2D(img_cv, -1, kernel)
        self.show_to_gui(dst)
        self.plot_to_matplotlib(img_cv, dst, '2D Convolution')

    def averaging(self):
        img_cv = self.imgcv
        img_cv = cv.cvtColor(img_cv, cv.COLOR_BGR2RGB)
        self.w = PopupWindow(self.parent)
        self.parent.wait_window(self.w.top)
        size = int(self.w.value)
        dst = cv.blur(img_cv, (size, size))
        self.show_to_gui(dst)
        self.plot_to_matplotlib(img_cv, dst, 'Averaging')

    def gaussian(self):
        img_cv = self.imgcv
        img_cv = cv.cvtColor(img_cv, cv.COLOR_BGR2RGB)
        self.w = PopupWindow(self.parent)
        self.parent.wait_window(self.w.top)
        size = int(self.w.value)
        dst = cv.GaussianBlur(img_cv, (size, size), 0)
        self.show_to_gui(dst)
        self.plot_to_matplotlib(img_cv, dst, 'Gaussian Filtering')

    def median(self):
        img_cv = self.imgcv
        img_cv = cv.cvtColor(img_cv, cv.COLOR_BGR2RGB)
        self.w = PopupWindow(self.parent)
        self.parent.wait_window(self.w.top)
        size = int(self.w.value)
        dst = cv.medianBlur(img_cv, size)
        self.show_to_gui(dst)
        self.plot_to_matplotlib(img_cv, dst, 'Median Filtering')

    def bilateral(self):
        img_cv = self.imgcv
        img_cv = cv.cvtColor(img_cv, cv.COLOR_BGR2RGB)
        dst = cv.bilateralFilter(img_cv, 9, 75, 75)
        self.show_to_gui(dst)
        self.plot_to_matplotlib(img_cv, dst, 'Bilateral Filtering')

    def maskImage(self):
        img_cv = self.imgcv
        img_rgb = cv.cvtColor(img_cv, cv.COLOR_BGR2RGB)
        img_cv = cv.cvtColor(img_cv, cv.COLOR_BGR2GRAY)
        ret, th1 = cv.threshold(img_cv, 127, 255, cv.THRESH_BINARY)
        self.show_to_gui(th1)
        self.plot_to_matplotlib(img_rgb, th1, 'Global Thresholding', 3)

    def morphology(self):
        img_cv = self.imgcv
        img_rgb = cv.cvtColor(img_cv, cv.COLOR_BGR2RGB)
        img_cv = cv.cvtColor(img_cv, cv.COLOR_BGR2GRAY)
        ret, th1 = cv.threshold(img_cv, 127, 255, cv.THRESH_BINARY)

        kernel = np.ones((5, 5), np.uint8)
        erosion = cv.erode(th1, kernel, iterations=1)
        dilation = cv.dilate(th1, kernel, iterations=1)
        opening = cv.morphologyEx(th1, cv.MORPH_OPEN, kernel)
        closing = cv.morphologyEx(th1, cv.MORPH_CLOSE, kernel)

        titles = ['Original', 'Mask',
                  'Erosi', 'Dilasi', 'Opening', 'Closing']
        images = [img_rgb, th1, erosion, dilation, opening, closing]
        self.show_to_gui(img_rgb)

        for i in range(6):
            if titles[i] == "Original":
                plt.subplot(2, 3, i + 1), plt.imshow(images[i])
            else:
                plt.subplot(2, 3, i + 1), plt.imshow(images[i], 'gray')
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])
        plt.show()

    def laplacian(self):
        img_cv = self.imgcv
        img_cv = cv.cvtColor(img_cv, cv.COLOR_BGR2GRAY)

        dst = cv.Laplacian(img_cv, cv.CV_64F)
        out = img_cv + dst
        self.show_to_gui(out)

        plt.figure(figsize=(11, 6))
        plt.subplot(131), plt.imshow(img_cv, cmap="gray"), plt.title('Original')
        plt.xticks([]), plt.yticks([])
        plt.subplot(132), plt.imshow(dst, cmap="gray"), plt.title('Laplacian')
        plt.xticks([]), plt.yticks([])
        plt.subplot(133), plt.imshow(out, cmap="gray"), plt.title('Resulting image')
        plt.xticks([]), plt.yticks([])
        plt.show()

    # first a conservative filter for grayscale images will be defined.
    def conservative_smoothing_gray(self, data, filter_size):
        temp = []
        indexer = filter_size // 2
        new_image = data.copy()
        nrow, ncol = data.shape
        for i in range(nrow):
            for j in range(ncol):
                for k in range(i - indexer, i + indexer + 1):
                    for m in range(j - indexer, j + indexer + 1):
                        if (k > -1) and (k < nrow):
                            if (m > -1) and (m < ncol):
                                temp.append(data[k, m])
                temp.remove(data[i, j])
                max_value = max(temp)
                min_value = min(temp)
                if data[i, j] > max_value:
                    new_image[i, j] = max_value
                elif data[i, j] < min_value:
                    new_image[i, j] = min_value
                temp = []
        return new_image.copy()

    def conservative(self):
        img_cv = self.imgcv
        img_cv = cv.cvtColor(img_cv, cv.COLOR_BGR2GRAY)
        dst = self.conservative_smoothing_gray(img_cv, 9)
        self.show_to_gui(dst)
        self.plot_to_matplotlib(img_cv, dst, 'Conservative Filtering', 2)

    def addsalt_pepper(self, image, amount):
        output = image.copy()
        if len(output.shape) == 2:
            black = 0
            white = 255
        else:
            colorspace = output.shape[2]
            if colorspace == 3:  # RGB
                black = np.array([0, 0, 0], dtype='uint8')
                white = np.array([255, 255, 255], dtype='uint8')
            else:  # RGBA
                black = np.array([0, 0, 0, 255], dtype='uint8')
                white = np.array([255, 255, 255, 255], dtype='uint8')
        probs = np.random.random(output.shape[:2])
        output[probs < (amount / 2)] = black
        output[probs > 1 - (amount / 2)] = white
        return output

    def snp_noise(self):
        img_cv = self.imgcv
        img_cv = cv.cvtColor(img_cv, cv.COLOR_BGR2RGB)
        amount = 0.01
        dst = self.addsalt_pepper(img_cv, amount)
        self.show_to_gui(dst)
        self.plot_to_matplotlib(img_cv, dst, 'Salt and Pepper Noise')

    def addgaussian(self, img, mean, var):
        if img.min() < 0:
            low_clip = -1.
        else:
            low_clip = 0.
        noise = np.random.normal(mean, var ** 0.5,
                                 img.shape)
        out = img + noise
        out = np.clip(out, low_clip, 1.0)
        out = np.array(255 * out, dtype='uint8')
        return out

    def gaussian_noise(self):
        img_cv = self.imgcv
        img_cv = cv.cvtColor(img_cv, cv.COLOR_BGR2RGB)
        img_cv = img_cv / 255.0
        mean = 0.
        var = 0.05
        dst = self.addgaussian(img_cv, mean, var)
        self.show_to_gui(dst)
        self.plot_to_matplotlib(img_cv, dst, 'Gaussian Noise')

    def addspeckle(self, image, mean, var):
        if image.min() < 0:
            low_clip = -1.
        else:
            low_clip = 0.
        noise = np.random.normal(mean, var ** 0.5,
                                 image.shape)
        out = image + image * noise
        out = np.clip(out, low_clip, 1.0)
        out = np.array(255 * out, dtype='uint8')
        return out

    def speckle_noise(self):
        img_cv = self.imgcv
        img_cv = cv.cvtColor(img_cv, cv.COLOR_BGR2RGB)
        img_cv = img_cv / 255.0
        mean = 0.
        var = 0.05
        dst = self.addspeckle(img_cv, mean, var)
        self.show_to_gui(dst)
        self.plot_to_matplotlib(img_cv, dst, 'Speckle Noise')

    def addpoisson(self, image):
        if image.min() < 0:
            low_clip = -1.
        else:
            low_clip = 0.
        # Determine unique values in image & calculate the next power of two
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        old_max = 0

        # Ensure image is exclusively positive
        if low_clip == -1.:
            old_max = image.max()
            image = (image + 1.) / (old_max + 1.)

        # Generating noise for each unique value in image.
        out = np.random.poisson(image * vals) / float(vals)

        # Return image to original range if input was signed
        if low_clip == -1.:
            out = out * (old_max + 1.) - 1.

        out = np.clip(out, low_clip, 1.0)
        out = np.array(255 * out, dtype='uint8')
        return out

    def poisson_noise(self):
        img_cv = self.imgcv
        img_cv = cv.cvtColor(img_cv, cv.COLOR_BGR2RGB)
        img_cv = img_cv / 255.0
        dst = self.addpoisson(img_cv)
        self.show_to_gui(dst)
        self.plot_to_matplotlib(img_cv, dst, 'Poisson Noise')

    def canny_edge_detection(self):
        img_cv = self.imgcv
        img_cv = cv.cvtColor(img_cv, cv.COLOR_BGR2GRAY)
        dst = cv.Canny(img_cv, 100, 200)
        self.show_to_gui(dst)
        self.plot_to_matplotlib(img_cv, dst, 'Canny Edge Detection', 2)

    def sobel_edge_detection(self):
        img_cv = self.imgcv
        img_cv = cv.cvtColor(img_cv, cv.COLOR_BGR2GRAY)
        img_gaussian = cv.GaussianBlur(img_cv, (3, 3), 0)
        img_sobelx = cv.Sobel(img_gaussian, cv.CV_8U, 1, 0, ksize=5)
        img_sobely = cv.Sobel(img_gaussian, cv.CV_8U, 0, 1, ksize=5)
        img_sobel = img_sobelx + img_sobely
        self.show_to_gui(img_sobel)
        self.plot_to_matplotlib(img_cv, img_sobel, 'Sobel Edge Detection', 2)

    def exit(self):
        var = messagebox.askyesno("Exit", "Do you want to exit ?")
        if var is True:
            self.parent.destroy()
        else:
            return
